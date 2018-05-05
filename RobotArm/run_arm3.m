%% Script to move arm based on given goal points
clc; clear all; close all;

%% Options
N_steps = 30;           % number of steps in trajectory
use_connection = 0;     % set to 1 to connect to kitchenNET server
use_virtual = 0;
use_robot = 0;          % set to 1 to connect to Cyton viewer

trajectories_computed = 0;

%% Configuration
ip_address = 'http://127.0.0.1:12345/';
url_goals = [ip_address, 'getArmGoals'];
url_poses = [ip_address, 'getAllPoses'];
url_state = [ip_address, 'setCurrentArmState'];
options = weboptions('RequestMethod', 'get');


% minivie_path = 'C:\git\minivie';
minivie_path = '/Users/yehby1/Documents/MATLAB/Human Robot Interaction/minivie';

%% Initialization
% Load robotics toolbox model & initial poses
cyton_poses

% Goto MiniVIE equivalent
my_dir = pwd;
cd(minivie_path)
MiniVIE.configurePath();
cd(my_dir)

if (use_robot)
    % Initialize the MATLAB UDP object
    udp_connection = PnetClass(8889, 8888, '127.0.0.1');
%     udp_connection = PnetClass(8889, 12005, '192.168.1.153');
    udp_connection.initialize();
else
    udp_connection = '';
end

if (~use_connection)
   fid = fopen('test_points3.txt');
   fid_poses = fopen('test_poses.txt');
end

% Initialize robot arm
pose_manager = PoseManager();
robot = KitchenatorArm(udp_connection, cyton);
robot.state = 'idle';
robot.location = 'standby';
robot.mode = 'go';
robot.T_goal = SE3(transl(0,0,0));
robot.gripper_current = 'open';
robot.gripper_goal = 'open';
robot.use_virtual = use_virtual;
robot.q_neutral = get_pose_by_name('neutral_pose', cyton_joint_map);
robot.T_neutral = get_pose_by_name('neutral_pose', cyton_T_map);

if (use_robot)
    count = 0;
    while (isempty(robot.q_measured))
        [reached, qdiff] = robot.measure();
        disp('Waiting for robot angles');
        count = count + 1
        if (count > 50)
            robot.q_measured = zeros(1,8);
            disp('Get position timeout');
        end
    end
    robot.update(robot.q_measured(1:7));
else
    
    robot.update(robot.q_neutral);
    robot.move(robot.q_neutral, robot.gripper_current);
end

while (1)

    % Clear out goal info
    goal_msg = '';
    
    % Check for new goalpoints from server
    if (use_connection) 
        % Send current state information
        if (mod(send_state_count, send_state_threshold) == 0)
            state_msg = jsonencode(containers.Map({'state','location'},{robot.state, robot.location}));
            response = webwrite(url_state, state_msg, options);
        end
        
        % Get positions
        data = webread(url_poses, options);
        pose_msg = jsondecode(data);
        
        % Get latest goal
        data = webread(url_goals, options);
        goal_msg = jsondecode(data);
    
    % Test with other points
    else
        disp(jsonencode(containers.Map({'state','location'},{robot.state, robot.location})));
        goal_raw = fgetl(fid);
        pose_raw = fgetl(fid_poses);
        % Poses from file
        if (pose_raw ~= -1)
            pose_msg = jsondecode(pose_raw);
        end
        % Points from file
        if (goal_raw ~= -1)
            goal_msg = jsondecode(goal_raw);
        end
    end
    
    
    % Update precomputed trajectories
    if (~isempty(pose_msg))
        pose_manager.parse_poses(pose_msg);
        robot.state = 'plan';
        
        if (use_connection)
            state_msg = jsonencode(containers.Map({'state','location'},{robot.state, robot.location}));
            response = webwrite(url_state, state_msg, options);
        end
        if (~trajectories_computed)
            disp('Computing trajectories...');
            pose_manager.compute_all_trajectories(robot);
            trajectories_computed = 1;
            disp('Finished computing. Ready for commands.');
        end 
        robot.state = 'idle';
    end
    
    % Handle new messages
    if (~isempty(goal_msg))
        % Update state
        if strcmp(goal_msg.armGoalState,'stop')
            robot.mode = 'stop';
            % keep updating gripper
            robot.move(robot.q_current, goal_msg.gripperState);
        elseif (strcmp(goal_msg.armGoalState,'go') && strcmp(robot.mode, 'idle'))
            robot.mode = 'go';
            q = pose_manager.get_trajectory(goal_msg.color);
            if (strcmp(goal_msg.armGoalState,'go'))
               robot.idx = 1;
               robot.location = 'landingpad';
            elseif (strcmp(goal_msg.armGoalState, 'dump'))
               robot.idx = 2;
               robot.location = 'bowl';
            elseif (strcmp(goal_msg.armGoalState, 'undump'))
               robot.idx = 4;
               robot.location = 'standby';
            end
            robot.q_traj = q{robot.idx};
            robot.t_step = 1;
            robot.mode = 'go';
        end
    end    
    if strcmp(robot.mode, 'go')
       robot.state = 'go';
        if isempty(robot.q_next)
            warning('Invalid next position')
            robot.mode = 'idle';
        else
            [done, qdiff] = robot.update();
            if (sum(robot.q_next >= cyton.qlim(:,1)') ~= 7)
                disp('commanded joint out of min range')
            elseif (sum(robot.q_next <= cyton.qlim(:,2)') ~= 7)
                disp('commanded joint out of max range')
            end
            
            % Send to Cyton
            if (use_robot)
                disp('sent joints')
                robot.move(robot.q_next, robot.gripper_current);
                disp(robot.gripper_current);
            else
                robot.sim(robot.q_next);
            end
            
            % Check if trajectory is complete
            if (done)
                % Update gripper position without moving
                robot.move(robot.q_current, robot.gripper_goal);
                disp('Completed trajectory');
                qdiff
                robot.q_current
                robot.T_current
                tr2rpy(robot.T_current)
                robot.mode = 'idle';
            end
        end
    end
    
    pause(0.01);
end