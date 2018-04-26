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

%% Configuration


ip_address = 'http://127.0.0.1:8000';
r = RequestMessage;
uri = URI(ip_address);
%%

% Goto MiniVIE equivalent
% my_dir = pwd;
% cd('C:\git\minivie') 
% MiniVIE.configurePath();
% cd(my_dir)

% Load robotics toolbox model
mdl_cyton

% Initialize the MATLAB UDP object
% udp_connection = PnetClass(8889, 8888, '127.0.0.1');
% udp_connection.initialize();
udp_connection = '';

% Initialize robot arm
robot = KitchenatorArm(udp_connection, cyton);
robot.T_goal = SE3(transl(0.3, 0.3, 0.05));
robot.update(qr);
stop_cmd = 0; goal_cmd = 0;
goal_msg = [0 0 0];

while (1)
    goal_msg = input('goal_msg');
    goal_cmd = length(goal_msg);
    
    % Check for new goalpoints
    resp = send(r,uri);
    goal_msg = jsondecode(resp);
    status = resp.StatusCode
    
    if (goal_cmd)
        robot.T_goal = SE3(transl(goal_msg.goal)*rotz(goal_msg.yaw,'deg'));
        robot.mode = RobotMode.PLAN;
    end
    % Check for stop signal
    if (stop_cmd)
        robot.mode = RobotMode.STOP;
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
            robot.T_traj = ctraj(robot.T_current, robot.T_goal, N_steps);
            robot.q_traj = cyton.ikine(robot.T_traj);
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
            robot.mode = RobotMode.MOVE;
            robot.t_current = 1;
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
            error('Invalid next position')
            robot.mode = RobotMode.IDLE;
        else
            robot.sim(q_desired);
            confirm = input('confirm? y/n', 's');
            
            % Send to robot
            if (confirm == 'y')
                disp('sent joints')
                robot.move(q_desired, robot.open_gripper);
                done = robot.update(q_desired);
                if (done)
                    robot.mode = RobotMode.IDLE;
                end
            end
        end
    end
    
     pause(0.01);
end