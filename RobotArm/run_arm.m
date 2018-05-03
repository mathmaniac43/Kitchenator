%% Script to move arm based on given goal points
% HOW TO RUN
% 1) start cyton viewer
% 2) Plugins > Load Plugin > select remoteCommandServerPlugin.ecp
% 3? Plugins > Load Plugin > select manipulationActionMangerPlugin.ecp

clc; clear all; close all;

import matlab.net.*
import matlab.net.http.*

%% Options
use_velocity = 0;
use_cartesian_traj = 1;
use_joint_traj = 0;
N_steps = 30;
use_connection = 0;
use_robot = 0;

%% Configuration

tcp_ip = 'localhost';
tcp_port = 5000;
%%
if (use_connection)
    tcp_socket = tcpclient(tcp_ip, tcp_port);
    fopen(tcp_socket);
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

    goal_cmd = 0;
    % Check for new goalpoints
    if (use_connection)
        if (tcp_socket.BytesAvailable)
            bytes = read(tcp_socket)
            goal_msg = jsondecode(bytes);
        end
        status = resp.StatusCode
    elseif (robot.mode == RobotMode.IDLE);
        goal_raw = input('goal_msg: (e.g. {"x":0.3,"y":0.3,"z":0.1,"yaw":0,"mode":"go","mask":[1,1,1,1,1,1]})\n');
        if (~isempty(goal_raw))
            goal_msg = jsondecode(goal_raw);
            goal_cmd = length(goal_msg);
        end
    end
    
    if (goal_cmd)
        % Check for stop signal
        if (goal_msg.mode == "stop")
            robot.mode = RobotMode.STOP;
        elseif (goal_msg.mode == "go")
            robot.T_goal = SE3(transl([goal_msg.x, goal_msg.y, goal_msg.z])*trotz(deg2rad(goal_msg.yaw)));
            robot.mode = RobotMode.PLAN;
            tic
        end
    end
    
    % Move (or not)
    if (robot.mode == RobotMode.STOP)
        disp('stop');
    elseif (robot.mode == RobotMode.IDLE)
        disp('idle');
    elseif (robot.mode == RobotMode.PLAN)
        disp('plan')
        
        if (use_cartesian_traj)
            %% Using cartesian trajectory
            current = robot.T_world*robot.T_current;
            goal = robot.T_world*robot.T_goal;
            p = findpath(prm, current.t(1:2)',goal.t(1:2)');
            figure(2)
            show(prm)
            robot.T_traj = ctraj(robot.T_current, robot.T_goal, N_steps);
            mask = [1;1;1;0;0;0];
            robot.q_traj = cyton.ikine(robot.T_traj,'q0',robot.q_current,'pinv', 'mask', mask);
        elseif (use_joint_traj)
            %% Using joint trajectory
            robot.q_traj = jtraj(robot.q_current, robot.q_goal, N_steps);
        else
            robot.q_traj = [robot.q_current];
        end
        if isempty(robot.q_traj)
            warning('Failed to converge')
            robot.mode = RobotMode.IDLE;
        else
            disp('Planning succeeded!');
            robot.mode = RobotMode.MOVE;
            robot.t_current = 1;
            robot.update(robot.q_current);
        end
    elseif (robot.mode == RobotMode.MOVE)
        disp('move')
        dt = toc;
        tic;
        
        if (use_velocity)
            %% Using velocity
            v_goal = robot.T_current.t - robot.goal.t;
            q_dot = pinv(cyton.jacob0(robot.q_current))*[v_goal; 0; 0; 0];
            robot.q_next = robot.q_next * (1 + q_dot);
        end
        
        disp(robot.q_next)
       
        if isempty(robot.q_next)
            warning('Invalid next position')
            robot.mode = RobotMode.IDLE;
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
                        robot.mode = RobotMode.IDLE;
                    end
                end
            else
                done = robot.update(robot.q_next);
                if (done)
                    robot.mode = RobotMode.IDLE;
                end
            end
        end
    end
    
     pause(0.01);
end