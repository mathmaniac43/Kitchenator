classdef PoseManager < handle
    properties
        purple_goal = [];
        purple_approach = [];
        purple_traj = cell(4,1);
        
        blue_goal = [];
        blue_approach = [];
        blue_traj = cell(4,1);
        
        T_bowl = [];
        N_steps = 30;
        last_color = 'blue';
    end
    
    methods
        function obj = PoseManager()
        end
        
        function parse_poses(obj, poses_msg)
            if (isfield(poses_msg, 'purple'))
                [obj.purple_goal, obj.purple_approach] = obj.decode_pose(poses_msg.purple);
            end
            if (isfield(poses_msg, 'blue'))
                [obj.blue_goal, obj.blue_approach] = obj.decode_pose(poses_msg.blue);
            end
            if (isfield(poses_msg, 'orange'))
                obj.T_bowl = obj.decode_pose(poses_msg.orange);
            end
        end
        
        function [T, Ta] = decode_pose(obj, pose_msg)
            T = [];
            Ta = [];
            if(isfield(pose_msg, 'x') && isfield(pose_msg, 'y') && isfield(pose_msg, 'z') && isfield(pose_msg, 'yaw'))
                x = double(pose_msg.x);
                y = double(pose_msg.y);
                z = double(pose_msg.z);
                yaw = double(pose_msg.yaw);
                T = SE3(transl(x, y, z))*SE3.oa([0,0,1],rotz(yaw)*[1,0,0]');
                Ta = T*SE3(transl(T.R*[0 -0.03 0]'));
            end
        end
        
        function [T, Ta] = get_pose(obj, name)
            Ta = [];
            T = [];
            if strcmp(name,'purple')
                T = obj.purple_goal;
                Ta = obj.purple_approach;
            elseif strcmp(name,'blue')
                T = obj.blue_goal;
                Ta = obj.blue_approach;
            elseif strcmp(name, 'orange')
                T = obj.bowl_goal;
            end
        end
        
        function [q] = get_trajectory(obj, name)
            if strcmp(name, 'orange')
                name = obj.last_color;
            end
            if strcmp(name,'purple')
                q = obj.purple_traj;
                obj.last_color = 'purple';
            elseif strcmp(name,'blue')
                q = obj.blue_traj;
                obj.last_color = 'blue';
            end
        end
        
        function compute_all_trajectories(obj, robot)
           obj.purple_traj = obj.compute_trajectory('purple', robot);
           obj.blue_traj = obj.compute_trajectory('blue', robot);
        end
        
        function [q] = compute_trajectory(obj, color, robot)
            [T,Ta] = obj.get_pose(color);
if (0)
            neutral2approach = ctraj(robot.T_neutral, Ta, obj.N_steps);
            [q0,n,T0] = get_best_guess(Ta.t);
            q1a = robot.sim_robot.ikcon(neutral2approach,'q0', q0);

            approach2goal = ctraj(Ta, T, obj.N_steps);
            [q0,n,T0] = get_best_guess(T.t);
            q1b = robot.sim_robot.ikcon(approach2goal, 'q0', q0);
            if (~isempty(q1b))
                q1ab = jtraj(q1a(end,:),q1b(1,:), obj.N_steps);
            else
                q1ab = [];
            end
            q1 = [q1a; q1ab; q1b];

            goal2bowl = robot.sim_robot.ctraj(T, obj.T_bowl, obj.N_steps);
            [q0,n,T0] = get_best_guess(obj.T_bowl.t);
            q2 = robot.sim_robot.ikcon(goal2bowl,q0);

            % TODO: fix this orientation
            q_dump = [q2(end,1:6) 0];
            q3 = jtraj(q2(end,:),q_dump,10);
            
            q12 = jtraj(q1(end,:), q2(1,:),10);
end            
%             q = cell(1,4);
%             % Go to landingpad
%             q{1} = q1;
%             % Go to bowl
%             q{2} = [q12;q2];
%             % Dump bowl
%             q{3} = q3;
%             % Undump & standby
%             q{4} = [flipud(q{3}); flipud(q{2}); flipud(q{1})];
            q = {zeros(1,7), zeros(1,7), zeros(1,7), zeros(1,7)};
            
        end
    end
end