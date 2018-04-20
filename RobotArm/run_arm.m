%% Script to move arm based on given goal points
% HOW TO RUN
% 1) start cyton viewer
% 2) Plugins > Load Plugin > select remoteCommandServerPlugin.ecp

clc; clear all; close all;

% Goto MiniVIE equivalent
my_dir = pwd;
cd('C:\git\minivie') 
MiniVIE.configurePath();
cd(my_dir)

% Load robotics toolbox model
mdl_cyton

% Initialize the MATLAB UDP object
udp = PnetClass(8889, 8888, '127.0.0.1');
udp.initialize();

% Initialize robot arm
robot = KitchenatorArm(udp, cyton);
robot.goal = transl(0.3, 0.3, 0.05);
q_current = qr;
q_desired = qr;
stop_cmd = 0; goal_cmd = 0;
goal_msg = [0 0 0];

while (1)
    % Check for new goalpoints
    % TODO: connect to main controller
    if (goal_cmd)
        robot.set_goal(transl(goal_msg));
    end
    % Check for stop signal
    if (stop_cmd)
        robot.mode = RobotMode.STOP;
    end
        
    % Move (or not)
    if (robot.mode == RobotMode.STOP)
        robot.stop();
    elseif (robot.mode == RobotMode.IDLE)
        %display('Waiting...')
    elseif (robot.mode == RobotMode.GOAL)
        q_desired = q_desired + .01;
        if isempty(q_desired)
            error('Failed to converge')
        else
            robot.mode = RobotMode.MOVE;
        end
    elseif (robot.mode == RobotMode.MOVE)
        display(q_desired)
        robot.sim(q_desired);
        robot.move(q_desired, robot.open_gripper);
        robot.mode = RobotMode.IDLE;
        q_current = q_desired;
    end
    
     pause(0.01);
end