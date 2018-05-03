%% Script to move arm based on given goal points
% 
%  PREFORMATTED
%  TEXT
% 
% HOW TO RUN
% 1) start cyton viewer
% 2) Plugins > Load Plugin > select remoteCommandServerPlugin.ecp
% 3? Plugins > Load Plugin > select manipulationActionMangerPlugin.ecp

clc; clear all; close all;

%% Options
N_steps = 30;           % number of steps in trajectory
use_connection = 1;     % set to 1 to connect to kitchenNET server
use_robot = 1;          % set to 1 to connect to Cyton viewer

use_simple = 0;         % find ik of single goal point and send to cyton
use_joint_traj = 0;     % compute joint space trajectory
use_cartesian_traj = 1; % compute cartesian trajectory

%% Configuration
send_state_threshold = 20;
send_state_count = 1;
url = 'http://127.0.0.1:12345/getArmGoals';
options = weboptions('RequestMethod', 'get'); % could also be 'post'

%% Initialization
% Load robotics toolbox model & initial poses
cyton_poses

if (use_robot)
    % Goto MiniVIE equivalent
    my_dir = pwd;
    cd('C:\git\minivie') 
    MiniVIE.configurePath();
    cd(my_dir)
    
    % Initialize the MATLAB UDP object
    udp_connection = PnetClass(8889, 8888, '127.0.0.1');
    udp_connection.initialize();
else
    udp_connection = '';
end

if (~use_connection)
   fid = fopen('test_points2.txt');
end

% Initialize robot arm
robot = KitchenatorArm(udp_connection, cyton);
robot.T_goal = SE3(transl(0,0,0));
if (use_robot)
    while (isempty(robot.q_measured))
        [reached, qdiff] = robot.measure();
    end
    disp('got current position')
    robot.update(robot.q_measured(1:7));
else
    robot.update(qz);
    robot.move(qz, robot.open_gripper);
end

goal_msg.x = 0.3;
goal_msg.y = 0.3;
goal_msg.yaw = 0;
goal_msg.mode = 'go';
goal_msg.mask = [1 1 1 0 0 0];

while (1)

    % Clear out goal info
    goal_cmd = 0; goal_msg = '';
    
    % Check for new goalpoints from server
    if (use_connection)
        
        % Send current state information
        if (mod(send_state_count, send_state_threshold) == 0)
            state_msg = jsonencode(struct('state',robot.mode));
            response = webwrite(url, state_msg, options);
        end
        
        % Get latest goal point
        data = webread(url, options);
        if strcmp(robot.mode,'idle')
            goal_msg = jsondecode(data);
            goal_cmd = length(goal_msg);
        end
    
    % Test with other points
    elseif strcmp(robot.mode,'idle')
        goal_raw = fgetl(fid);
        % Points from file
        if (goal_raw ~= -1)
            goal_msg = jsondecode(goal_raw);
        % Points from  user
        else
            goal_raw = input('goal_msg: (e.g. {"x":0.3,"y":0.3,"z":0.1,"yaw":0,"mode":"go","mask":[1,1,1,1,1,1]})\n');
            if (~isempty(goal_raw))
                goal_msg = jsondecode(goal_raw);
            end
        end
        goal_cmd = ~isempty(goal_msg);
    end
    
    % Handle new messages
    if (goal_cmd)
        % Check for stop signal
        if strcmp(goal_msg.armGoalState,'pause')
            robot.mode = 'stop';
        elseif strcmp(goal_msg.armGoalState,'go')
            pose = goal_msg.armGoalPose;
            robot.T_goal = SE3(trotz(deg2rad(double(pose.yaw)))*transl(double(pose.x), double(pose.y), double(pose.z)));
            robot.mask = [1 1 1 0 0 0]; %goal_msg.mask;
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
        
        % Figure out closest known position
        [q0,n,T0] = get_best_guess(robot.T_goal.t);
        robot.q_goal = cyton.ikine(robot.T_goal, 'q0', q0, 'mask', robot.mask);
%         robot.q_goal = cyton.ikine(robot.T_goal, 'mask', [1 1 1 0 0 0]);
        
        if (isempty(robot.q_goal))
            disp('IK on goal position failed');
            robot.q_traj = [];
        % Plan single point
        elseif (use_simple)
            robot.q_traj = [robot.q_current; robot.q_goal];
        % Plan Cartesian trajectory
        elseif (use_cartesian_traj)
            robot.T_current = cyton.fkine(robot.q_current);
            robot.T_traj = ctraj(robot.T_current, robot.T_goal, N_steps);
            % Clear previous trajectory
            robot.q_traj = zeros(N_steps, 7);
            % Plan backwards from end goal
            robot.q_traj(N_steps,:) = robot.q_goal;
            q0 = robot.q_goal;
            for i = N_steps-1:-1:1
                 q = cyton.ikine(robot.T_traj(i),'q0',q0, 'mask', robot.mask);
%                 q = cyton.ikcon(robot.T_traj(i),'q0',q0, 'mask', robot.mask);
                if isempty(q)
                    robot.q_traj = [];
                    break;
                end
                robot.q_traj(i,:) = q;
                q0 = q;
            end
        % Plan joint trajectory
        elseif (use_joint_traj)
            robot.q_goal = cyton.ikine(robot.T_goal,'q0', q0);
            robot.q_traj = jtraj(robot.q_current, robot.q_goal, N_steps);
        end
        
        if isempty(robot.q_traj)
            warning('Failed to plan')
            robot.mode = 'replan';
        else
            disp('Planning succeeded!');
            robot.mode = 'move';
            robot.t_step = 1;
            robot.update(robot.q_current);
            tic;
        end
        
    elseif strcmp(robot.mode,'replan')
        disp('replan')
        robot.mode = 'idle';
    elseif strcmp(robot.mode,'move')
        disp('move')
        dt = toc;
        
        disp(robot.q_next)
        
        if isempty(robot.q_next)
            
            warning('Invalid next position')
            robot.mode = 'idle';
            
        else
            
            % Visualize in MATLAB first
            robot.sim(robot.q_next);
            disp('sim')
            % Send to Cyton
            if (use_robot)
%                 confirm = input('confirm? y/n', 's');
                confirm = 'y';
                % Send to robot
                if (confirm == 'y')
                    disp('sent joints')
                    robot.move(robot.q_next, robot.open_gripper);
                end
            end
            
            [done, qdiff] = robot.update();
            
            % Check if trajectory is complete
            if (done)
                disp('Completed trajectory');
                qdiff
                robot.T_current
                robot.mode = 'idle';
            end
        end
    else
        disp('Uknown state')
        robot.mode
    end
    
     pause(0.01);
end