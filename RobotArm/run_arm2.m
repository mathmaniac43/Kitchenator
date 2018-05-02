%% Script to move arm based on given goal points
% HOW TO RUN
% 1) start cyton viewer
% 2) Plugins > Load Plugin > select remoteCommandServerPlugin.ecp
% 3? Plugins > Load Plugin > select manipulationActionMangerPlugin.ecp

clc; clear all; close all;

import matlab.net.*
import matlab.net.http.*

%% Options
N_steps = 30;
use_connection = 0;
use_robot = 0;
use_joint_traj = 1;
use_cartesian_traj = 0;

%% Configuration
send_state_threshold = 20;
send_state_count = 1;
tcp_ip = 'localhost';
tcp_port = 5000;
%%
if (use_connection)
    tcp_socket = tcpclient(tcp_ip, tcp_port);
    fopen(tcp_socket);
else
    fid = fopen('test_points.txt');
end
if (use_robot)
    Goto MiniVIE equivalent
    my_dir = pwd;
    cd('C:\git\minivie') 
    MiniVIE.configurePath();
    cd(my_dir)
end

% Load robotics toolbox model
mdl_cyton

% Initialize the MATLAB UDP object
% udp_connection = PnetClass(8889, 8888, '127.0.0.1');
% udp_connection.initialize();
udp_connection = '';

% Initialize occupancy grid
base_radius = 0.15;
resolution = 100;
world_x = 1;
world_y = 1;

map = robotics.BinaryOccupancyGrid(world_x,world_y,resolution);
setOccupancy(map, [0 world_y/2], 1);
inflate(map, base_radius);
y = 0:1/resolution:world_y;
x = zeros(size(y));
setOccupancy(map, [x' y'], 1);

prm = robotics.PRM;
prm.Map = map;
prm.NumNodes = 100;

% Initialize robot arm
robot = KitchenatorArm(udp_connection, cyton);
robot.T_goal = SE3(transl(0.3, 0.3, 0.05));
robot.update(qr);
stop_cmd = 0; goal_cmd = 0;
goal_msg = [0 0 0];
robot.T_world = SE3(transl(0, world_y/2,0));

while (1)
    
    if (mod(send_state_count, send_state_threshold) == 0)
        keys = {'state'};
        
        state = robot.state_string;
        value = [state];
        state_msg = jsonencode(table(keys,values));
        bytes1 = unicode2native(state_msg,'UTF-8');
        write(tcp_socket, bytes1)
    end

    goal_cmd = 0;
    % Check for new goalpoints
    if (use_connection)
        if (tcp_socket.BytesAvailable)
            bytes = read(tcp_socket);
            string = native2unicode(bytes);
            goal_msg = jsondecode(string);
        end
        status = resp.StatusCode
    elseif strcmp(robot.mode,'idle')
        goal_raw = fgetl(fid);
        if (goal_raw ~= -1)
        %goal_raw = input('goal_msg: (e.g. {'x':0.3,'y':0.3,'z':0.1,'yaw':0,'mode':'go','mask':[1,1,1,1,1,1]})\n');
        %if (~isempty(goal_raw))
            goal_msg = jsondecode(goal_raw);
            goal_cmd = length(goal_msg);
        end
    end
    
    if (goal_cmd)
        % Check for stop signal
        if strcmp(goal_msg.mode,'stop')
            robot.mode = 'stop';
        elseif strcmp(goal_msg.mode,'go')
            robot.T_goal = SE3(transl([goal_msg.x, goal_msg.y, goal_msg.z])*trotz(deg2rad(goal_msg.yaw)));
            robot.mask = goal_msg.mask;
            robot.mode = 'plan';
            tic
        end
    end
    
    % Move (or not)
    if strcmp(robot.mode,'stop')
        disp('stop');
    elseif strcmp(robot.mode,'idle')
        disp('idle');
    elseif strcmp(robot.mode,'plan')
        disp('plan')
        
        
        if (use_cartesian_traj)
            %% Using cartesian trajectory
            guess = deg2rad([-4.1459, -37.64229, -106.2836, -58.348412, -50.386816, 74.048011, 80.18664]);
            robot.T_traj = ctraj(robot.T_current, robot.T_goal, N_steps);
            robot.q_traj = cyton.ikine(robot.T_traj,'q0',guess,'pinv', 'mask', robot.mask);
        elseif (use_joint_traj)
            %% Using joint trajectory
            guess = deg2rad([-4.1459, -37.64229, -106.2836, -58.348412, -50.386816, 74.048011, 80.18664]);
            robot.q_goal = cyton.ikine(robot.T_goal,'q0', guess);
            robot.q_traj = jtraj(robot.q_current, robot.q_goal, N_steps);
        end
        if isempty(robot.q_traj)
            warning('Failed to plan')
            robot.mode = 'replan';
        else
            disp('Planning succeeded!');
            robot.mode = 'move';
            robot.t_current = 1;
            robot.update(robot.q_current);
            robot.sim(robot.q_traj);
        end
    elseif strcmp(robot.mode,'replan')
        disp('replan')
        current = robot.T_world*robot.T_current;
        goal = robot.T_world*robot.T_goal;
        p = findpath(prm, current.t(1:2)',goal.t(1:2)');
        figure(2)
        show(prm)
        T_start = robot.T_current;
        z = robot.T_goal.t(3);
        robot.T_traj = [];
        for i = 1:size(p,1)
            T_next = inv(robot.T_world) * SE3(rt2tr(robot.T_current.R,[p(i,1), p(i,2), z]));
            robot.T_traj = [robot.T_traj ctraj(T_start, T_next, N_steps)];
            T_next = T_start;
        end
        
        robot.q_traj = cyton.ikine(robot.T_traj,'q0',robot.q_current,'pinv', 'mask', robot.mask);
        if isempty(robot.q_traj)
            disp('!!! Failed to replan')
            robot.mode = 'idle';
        else
            disp('Re-planning succeeded!');
            robot.mode = 'move';
            robot.t_current = 1;
            robot.update(robot.q_current);
        end
    elseif strcmp(robot.mode,'move')
        disp('move')
        dt = toc;
        tic;
        
        disp(robot.q_next)
       
        if isempty(robot.q_next)
            warning('Invalid next position')
            robot.mode = 'idle';
        else
            robot.sim(robot.q_next);
            if (use_robot)
                confirm = input('confirm? y/n', 's');

                % Send to robot
                if (confirm == 'y')
                    disp('sent joints')
                    robot.move(robot.q_next, robot.open_gripper);
                    done = robot.update(robot.q_next);
                    if (done)
                        robot.mode = 'idle';
                    end
                end
            else
                done = robot.update(robot.q_next);
                if (done)
                    robot.mode = 'idle';
                end
            end
        end
    else
        disp('Uknown state')
        robot.mode
    end
    
     pause(0.01);
end