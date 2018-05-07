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
            q = [];
            if strcmp(name, 'orange')
                name_local = obj.last_color;
            else
                name_local = name;
            end
            if strcmp(name_local,'purple')
                q = obj.purple_traj;
                obj.last_color = 'purple';
            elseif strcmp(name_local,'blue')
                q = obj.blue_traj;
                obj.last_color = 'blue';
            end
        end
        
        function compute_all_trajectories(obj, robot)
           obj.purple_traj = obj.compute_trajectory('purple', robot);
           obj.blue_traj = obj.compute_trajectory('blue', robot);
        end
        
        function [q] = compute_trajectory(obj, robot)
            color = robot.target_color;
            [T,Ta] = obj.get_pose(color);
            q1 = [];
            q2 = [];
            q3 = [];
            q12 = [];
            tic
%             options = optimoptions('fmincon');
%             options.ConstraintTolerance = 1e-4;
%              standby2approach = ctraj(robot.T_neutral, Ta, obj.N_steps);
              [q0,n,T0] = get_best_guess(Ta.t);
%             q1a = robot.sim_robot.ikcon(standby2approach,q0);
%              q1a = robot.sim_robot.ikine(standby2approach,'q0',q0);
             q1a = robot.sim_robot.jtraj(robot.T_neutral,Ta,obj.N_steps,'q0',q0);

             approach2grab = ctraj(Ta, T, obj.N_steps);
%              [q0,n,T0] = get_best_guess(T.t);
             q0 = q1a(end,:);
             q1b = robot.sim_robot.ikcon(approach2grab,q0);
%             q1b = robot.sim_robot.ikine(approach2grab,'q0',q0);
%             q1b = robot.sim_robot.jtraj(Ta,T,obj.N_steps);
            
            if (~isempty(q1b))
                T1a = robot.sim_robot.fkine(q1a(end,:));
                T1b = robot.sim_robot.fkine(q1b(1,:));
                q1ab = robot.sim_robot.jtraj(T1a,T1b, 5,'q0',q0);
            else
                q1ab = [];
            end
            
            q_neutral = jtraj(robot.q_neutral,q1a(1,:),5);
            q1 = [q_neutral;q1a; q1ab; q1b];

%             goal2predump = ctraj(T, obj.T_bowl, obj.N_steps);
%              [q0,n,T0] = get_best_guess(obj.T_bowl.t);
            q0 = q1(end,:);
%             q2 = robot.sim_robot.ikcon(goal2predump,q0);
%             q2 = robot.sim_robot.ikcon(goal2predump,'q0',q0);
            q2 = robot.sim_robot.jtraj(T,obj.T_bowl,obj.N_steps,'q0',q0);
            
            % TODO: fix this orientation
%             q_dump = [q2(end,1:6) 0];
%             q3 = jtraj(q2(end,:),q_dump,10);
            q7_angle = q2(end,7);
            if strcmp(robot.target_color, 'blue')
%                 T_dump = obj.T_bowl*SE3(trotz(pi/2));
                q_dump = [q2(end,1:6) q7_angle+pi/2];
            elseif strcmp(robot.target_color,'purple')
%                 T_dump = obj.T_bowl;
                q_dump = [q2(end,1:6) q7_angle-pi/2];
            end
%             q3 = robot.sim_robot.jtraj(obj.T_bowl,T_dump,obj.N_steps,'q0',q2(end,:));
            q3 = jtraj(q2(end,:), q_dump,10);
            
            q12 = jtraj(q1(end,:), q2(1,:),10);
            
            if (isempty(q1))
                q1 = zeros(1,7);
            elseif (isempty(q12))
                q12 = zeros(1,7);
            elseif (isempty(q2))
                q2 = zeros(1,7);
            elseif (isempty(q3))
                q3 = zeros(1,7);
            end
            
            q = cell(1,4);
            % Go to landingpad - open -> close
            q{1} = [q1 robot.open_gripper*ones(size(q1,1),1); q1(end,:) robot.closed_gripper];
            % Go to bowl - close
            q{2} = [q12;q2];
            q{2} = [q{2} robot.closed_gripper*ones(size(q{2},1),1)];
            % Dump bowl - close
            q{3} = [q3 robot.closed_gripper*ones(size(q3,1),1)];
            % Undump & standby
            q{4} = [flipud(q{3}); flipud(q{2}); flipud(q{1})];
            disp(['Time to plan: ',string(toc)]);
            if (strcmp(robot.target_color, 'blue'))
                obj.blue_traj = q;
            elseif (strcmp(robot.target_color, 'purple'))
                obj.purple_traj = q;
            end
        end
    end
end