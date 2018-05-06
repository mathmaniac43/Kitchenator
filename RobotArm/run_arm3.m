%% Script to move arm based on given goal points
clc; clear all; close all;

%% Options
N_steps = 30;           % number of steps in trajectory
use_connection = 1;     % set to 1 to connect to kitchenNET server
use_virtual = 0;
use_robot = 0;          % set to 1 to connect to Cyton viewer

trajectories_computed = 0;

test_count = 0;

%% Configuration
% ip_address = 'http://192.168.0.10:12345/';
ip_address = 'http://127.0.0.1:12345/';
url_goals = [ip_address, 'getArmCurrentStatus'];
url_poses = [ip_address, 'getAllPoses'];
url_state = [ip_address, 'setArmCurrentState'];
options = weboptions('RequestMethod', 'get');
options.Timeout = 1e3;
options_post = weboptions('RequestMethod', 'post');
options_post.Timeout = 1e3;

% minivie_path = 'C:\git\minivie';
% minivie_path = 'C:\Users\Nick\repos\minivie';
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
robot.current_state = 'standby';
robot.target_state = 'standby';
robot.stopgo = 'go';
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
        response = webwrite(url_state, string(['"',robot.current_state,'"']), options_post);
        
        % Get positions
        data = webread(url_poses, options);
        pose_msg = jsondecode(data);
        
        % Get latest goal
        data = webread(url_goals, options);
        goal_msg = jsondecode(data);
    
    % Test with other points
    else
        disp(robot.current_state);
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
    end
    
    % Handle new messages
    if (~isempty(goal_msg))
        robot.target_state = goal_msg.targetState;
        robot.target_color = string(goal_msg.color);
        robot.stopgo = goal_msg.stopgo;
    end
    
    % 
    if strcmp(robot.target_state,'standby')
        disp('Standby...');
    elseif strcmp(robot.target_state,'planning')
        disp('Planning...');
        if ~isempty(robot.target_color)
            if strcmp(robot.target_color, 'blue')
                pose_manager.blue_traj = pose_manager.compute_trajectory(robot.target_color);
                disp('Finished computing trajectory to blue.');
                robot.current_state = 'planning';
            elseif strcmp(robot.target_color, 'purple')
                pose_manager.purple_traj = pose_manager.compute_trajectory(robot.target_color);
                disp('Finished computing trajectory to blue.');
                robot.current_state = 'planning';
            end
        else
            disp('Waiting on color goal...');
        end
    else
        % Get current trajectory
        q = pose_manager.get_trajectory(robot.target_color);
        
        if strcmp(robot.target_state,'grab')
            q_idx = 1;
        elseif strcmp(robot.target_state,'pre_dump')
            q_idx = 2;
        elseif strcmp(robot.target_state,'dump')
            q_idx = 3;
        else
            warning(['Unknown state ', robot.target_state]);
        end
        
        if (~isempty(q))
            % Pick appropriate segment
            robot.q_traj = q{q_idx};
        else
            robot.q_traj = zeros(1,7);
        end
        robot.t_step = 1;
    end
    
    if strcmp(robot.stopgo, 'go')
        % MOVE ARM
        [done, qdiff] = robot.update();
        if (test_count > 20) || strcmp(robot.target_state,'planning')
            done = 1;
        else
            done = 0;
            test_count = test_count+1
        end
        if (done)
            test_count = 0;
            % Update gripper position without moving
            robot.move(robot.q_current, robot.gripper_goal);
            disp('Completed trajectory');
            qdiff
            robot.q_current
            robot.T_current
            tr2rpy(robot.T_current)
            if (~strcmp(robot.target_state, 'planning'))
                robot.current_state = robot.target_state;
            end
        elseif isempty(robot.q_next)
            warning('Empty trajectory');
        else
            % check if next move exists
            if (sum(robot.q_next >= cyton.qlim(:,1)') ~= 7)
                disp('commanded joint out of min range')
            elseif (sum(robot.q_next <= cyton.qlim(:,2)') ~= 7)
                disp('commanded joint out of max range')
            else
                % valid command
                if (use_robot)
                    disp('sent joints')
                    robot.move(robot.q_next, robot.gripper_current);
                    disp(robot.gripper_current);
                else
                    robot.sim(robot.q_next);
                end
            end
        end
        
    else
        % STOP!!!!
        warning('Stopping!!!');
        test_count = 0;
    end
    
    disp(['Target state: ', robot.target_state])
    disp(['Target color: ', robot.target_color])
    disp(['Current state: ', robot.current_state])
    
    pause(1);
end