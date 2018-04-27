classdef KitchenatorArm < handle
    %KITCHENATORARM Class for Cyton E1500
    %   Detailed explanation goes here
    
    properties
        open_gripper = .013; % in m
        closed_gripper = .005; % in m
        udp
        sim_robot
        mode
        T_goal
        q_goal
        T_traj
        q_traj
        T_current
        q_current
        t_current
        q_next
        T_world = SE3(transl(0,.5,0));
    end
    
    methods
        function obj = KitchenatorArm(udp, sim_robot)
            %KITCHENATORARM Construct an instance of this class
            %   [in] udp : udp connection to Actin Viewer
            %   [in] sim_robot : robotics toolbox cytonE1500 model
            obj.udp = udp;
            obj.sim_robot = sim_robot;
            obj.mode = RobotMode.IDLE;
        end
        
        function move(obj,joints,gripper_pos)
            %MOVE Sends joints + gripper position over udp connection
            %   [in] joints : joint angles in radians
            %   [in] gripper_pos : gripper position in meters
            desiredAngles = [joints gripper_pos];
            obj.udp.putData(typecast(desiredAngles,'uint8'));
        end
        
        function sim(obj,joints)
            %SIM Plots robot toolbox model for given joint
            %   [in] joints : joint angles in radians
            figure(1);
            obj.sim_robot.plot(joints);
        end
        
        function stop(obj)
            disp('Stopping...');
            % Do nothing for now...
        end
        
        function done = update(obj, joints)
            disp(joints)
            obj.q_current = joints;
            obj.T_current = obj.sim_robot.fkine(obj.q_current);
            obj.t_current = obj.t_current+1;
            if (obj.t_current > size(obj.q_traj,1))
                done = 1;
            else
                obj.q_next = obj.q_traj(obj.t_current,:);
                done = 0;
            end
        end
    end
end

