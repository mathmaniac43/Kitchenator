mdl_cyton
cyton_poses

dt = 1;

udp_connection = PnetClass(8889, 8888, '127.0.0.1');
udp_connection.initialize();
robot = KitchenatorArm(udp_connection, cyton);

% Initial zero position
robot.move(deg2rad(left_intermediate2), 0.01);
pause
arbitrary_goal = [-0.2, 0.41, 0.08928];
arbitrary_yaw = deg2rad(30);
[q0,n,T0] = get_best_guess(arbitrary_goal);
rpy = tr2rpy(T0);
T_goal = transl(arbitrary_goal);%*rt2tr(T0.R,[0,0,0]');
joints_goal = cyton.ikine(T_goal, 'q0', q0, 'mask', [1 1 1 1 1 1]);
robot.move(joints_goal, robot.open_gripper);
% if (~isempty(T_joint))
%     robot.move(T_joint, robot.open_gripper);
% end
% T_traj = ctraj(robot.T_current, T_goal);

pause;
% joint_goal = cyton.ikine(r, 'q0', q0, 'mask', [1 1 1 0 0 0]);
% q1 = jtraj(robot.q_current, left_intermediate2, 20);
goal1 = cyton.ikine(transl([-0.3356, 0.3588, 0.09404]), 'q0', left_approach, 'mask', [1 1 1 0 0 0]);
q2 = jtraj(left_intermediate2, goal1, 20);
goal2 = cyton.ikine(transl([-0.286, 0.459, 0.08928]), 'q0', left_pickup, 'mask', [1 1 1 0 0 0]);
q3 = jtraj(goal1, goal2, 30);
q = [q1; q2; q3];

%     bytes = udp_connection.getData();
%     done = 0
%     while (~done)
%     while (isempty(bytes))
%         bytes = udp_connection.getData();
%     end
%     angles = typecast(bytes,'singles');
%     angles
%     q(i,:) - angles
%     done = input('done?')

pause
robot.move(deg2rad(left_approach), robot.open_gripper);
pause
robot.move(deg2rad(left_pickup), robot.open_gripper);
pause
robot.move(deg2rad(left_pickup), robot.closed_gripper);
pause
robot.move(deg2rad(left_ready_to_pour), robot.closed_gripper);
pause
robot.move(deg2rad(left_pouring), robot.closed_gripper);
pause
robot.move(deg2rad(left_ready_to_pour), robot.closed_gripper);
pause
robot.move(deg2rad(left_pickup), robot.closed_gripper);
pause
robot.move(deg2rad(left_pickup), robot.open_gripper);
pause

% set the current angles of the robot
% currentAngles = zeros(1,9);
% 
% % generate some new angles for the robot to go to
% qDefault = [0 0 0 0 0 0 0];
% qa1up = [-0.636775	-1.042044	0.097326	-0.467157	-0.014381	-1.572323	1.816137
% ];
% qa1down = [-0.636542	-1.374181	0.081066	-0.363445	-0.013303	-1.468995	1.907175
% ];
% qa8 = [-1.134898	-0.596764	0.179554	-1.764614	0.199388	-0.845461	0.246884
% ]
% a1D = [	-0.912914	-1.627988	0.256206	-0.008164	0.609084	-1.536184	-1.702333];
% a2D = [	-1.138866	-1.525901	0.432044	-0.193212	0.761267	-1.396207	-1.488203];
% a1U =	[-0.636775	-1.042044	0.097326	-0.467157	-0.014381	-1.572323	1.816137];
% a2U	= [-0.950028	-1.120609	0.226242	-0.525514	0.704199	-1.458815	-1.65186];
% 
% % create a vector that includes the robot's arm angles and the gripper
% % distance
% desiredAngles = [qDefault, 0.01];
% % send the data to the Actin Viewer
% udp_connection.putData(typecast(desiredAngles,'uint8'))
udp_connection.close();