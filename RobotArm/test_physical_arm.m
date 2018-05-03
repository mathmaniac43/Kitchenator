mdl_cyton
udp_connection = PnetClass(8889, 8888, '127.0.0.1');
udp_connection.initialize();
robot = KitchenatorArm(udp_connection, cyton);
% robot.move(qz, robot.open_gripper);
% pause
left_intermediate = [75.69 -63.42 -42.57 -18.97 -50.75 23.11 -89.29];
left_intermediate2 = [75.69 -63.42 -42.57 -18.97 -50.75 23.11 -89.29];
left_approach = [91.9 -76.67 -55.21 -42.75 -23.48 34.47 -86.23];
left_pickup = [72.92 -76.67 -41.82 -47.48 -23.48 34.47 -86.23];
left_ready_to_pour = [57.37 -58.50 -53.06 -41.35 -23.50 34.478 -107.35];
left_pouring = [57.36 -59.08 -53.04 -41.42 -23.5 34.48 -10];
robot.move(deg2rad(qz), robot.open_gripper);
pause
robot.move(deg2rad(left_intermediate2), robot.open_gripper);
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
cyton.plot(qtest)

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