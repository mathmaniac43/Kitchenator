classdef KitchenatorArm
    %KITCHENATORARM Class for Cyton E1500
    %   Detailed explanation goes here
    
    properties
        open_gripper = .013; % in m
        closed_gripper = .005; % in m
        udp
        sim_robot
        mode
        goal
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
            % TODO: figure out how to pack enable/disable hardware command
            %obj.udp.putData(typecast(,'uint8'));
        end
        
        function set_goal(obj, goal)
            obj.goal = goal;
        end
    end
end

