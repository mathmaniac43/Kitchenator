classdef KitchenatorArm < handle
    %KITCHENATORARM Class for Cyton E1500
    %   Detailed explanation goes here
    
    properties
        open_gripper = .007; % in m
        closed_gripper = .0033; % in m
        udp
        sim_robot
        
        current_state
        target_state
        target_color
        stopgo
        
        T_goal
        T_approach
        q_goal
        T_traj
        q_traj
        T_current
        q_current
        t_step
        q_measured = [];
        q_next
        mask = [1 1 1 0 0 0];
        gripper_current;
        gripper_goal;
        q_tol = 0.2;            % joint angle tolerance
        q_undump
        use_virtual
        q_neutral;
        T_neutral;
        q;
        idx;
    end
    
    methods
        function obj = KitchenatorArm(udp, sim_robot)
            %KITCHENATORARM Construct an instance of this class
            %   [in] udp : udp connection to Actin Viewer
            %   [in] sim_robot : robotics toolbox cytonE1500 model
            obj.udp = udp;
            obj.sim_robot = sim_robot;
            obj.current_state = 'standby';
        end
        
        function move(obj,joints,gripper_pos)
            %MOVE Sends joints + gripper position over udp connection
            %   [in] joints : joint angles in radians
            %   [in] gripper_pos : gripper open/closed
            obj.sim(joints);
            
            if (strcmp(gripper_pos, 'open'))
                gripper_val = obj.open_gripper;
            elseif (strcmp(gripper_pos,'close'))
                gripper_val = obj.closed_gripper;
            else
                gripper_val = obj.open_gripper;
            end
            desiredAngles = [joints gripper_val];
            if (obj.use_virtual)
                desiredAngles(1:7) = rad2deg(desiredAngles(1:7));
            end
            if (~isempty(obj.udp))
                obj.udp.putData(typecast(desiredAngles,'uint8'));
                obj.update(joints);
            end
            obj.gripper_current = gripper_pos;
        end
        
        function sim(obj,joints)
            %SIM Plots robot toolbox model for given joint
            %   [in] joints : joint angles in radians
            figure(1);
            obj.sim_robot.plot(joints(1:7));
        end
        
        function stop(obj)
            disp('Stopping...');
            % Do nothing for now...
        end
        
        function [done, qdiff] = update(obj, joints)
            
            if(exist('joints','var'))
                obj.q_current = joints;
            end
            
            [reached, qdiff] = obj.measure();
            
            % Only update next point when robot is at last sent
            if (reached)
                obj.t_step = obj.t_step+1;
                obj.q_current = obj.q_next;
            end
            
            if (obj.t_step > size(obj.q_traj,1))
               done = 1;
            else
               obj.q_next = obj.q_traj(obj.t_step,:);
               done = 0;
            end
            obj.T_current = obj.sim_robot.fkine(obj.q_current(1:7));
            
        end
        
        function [reached, qdiff] = measure(obj)
            if ((~isempty(obj.udp)) && (~obj.use_virtual))
                % Read robot joint angles
                bytes = obj.udp.getData();
                if (~isempty(bytes))
                    obj.q_measured = typecast(bytes,'double');
                end
            else
                % Simulate perfect robot
                obj.q_measured = obj.q_next;
            end
            
            if (isempty(obj.q_measured))||(isempty(obj.q_next))
                qdiff = [];
                reached = 0;
            else
                qdiff = obj.q_next(1:7) - obj.q_measured(1:7);
                reached = norm(qdiff) < obj.q_tol;
            end
        end
    end
end

