mdl_cyton

%% MISC
%ready_pose = rad2deg([0 -.7 0 -.7 0 -.7 0]);
%zero_pose = [0 0 0 0 0 0 0];

neutral_pose = [90   0  -50   0  -22    0    100];

%%
% FOR LEFT INGREDIENT (according to robot's perspective)

% old point, use left_intermediate2 for more space on approach
% left_intermediate = [75.69 -63.42 -42.57 -18.97 -50.75 23.11 -89.29];

% left_intermediate2 = [75.69 -63.42 -42.57 -18.97 -50.75 23.11 -89.29];

% right_side = [185.231714 0.564036 20.149444 155.133411 -52.611582 -35.142579 -56.699124];
right_side = [65.042889 60.640720 -83.645478 34.437355 -23.772030 -46.254051 -87.809153];
% left_side = [106.957027 -126.822040 20.109517 -2.633301 -52.611582
right_bowl = [ 77.561998 16.549634 -86.679872 13.886311 -38.047608 -37.883992 -38.296008];
left_bowl = [17.265882 -35.836324 -17.194902 -97.969201 13.099350 40.220322 66.571709];
left_side = [51.918668 -71.713079 -34.389803 -73.663138 31.103386 54.781322 73.821218];
% left_approach = [91.9 -76.67 -55.21 -42.75 -23.48 34.47 -86.23];

% left_pickup = [72.92 -76.67 -41.82 -47.48 -23.48 34.47 -86.23];

% left_ready_to_pour = [57.37 -58.50 -53.06 -41.35 -23.50 34.478 -107.35];

% left_pouring = [57.36 -59.08 -53.04 -41.42 -23.5 34.48 -10];

% left_pickup_b = [16.338042 -71.510919 25.725809 -63.268527 10.273604 43.298257 94.950884];

% FOR RIGHT INGREDIENT

% not actually tested, just mirroring left
% right_pickup_sim = [72, 76, -41, 47, -23, -43, 86];

% right_pickup = [84.667, 74.550, -68.320, 39.961, -20.839, -34, 94.9609];

% right_clear_bowl = [84.675, 74.576, -68.300, 21.4843, -20.991, -34.559, 94.951];

% right_about_to_pour = [109.277, 74.576, -68.3, 21.484, -20.991, -34.559, 94.95];

% right_pouring = [109.277, 74.576, -68.3, 21.484, -20.991, -34.559 25.566];

cyton_positions = {...
%     'ready_pose', 'zero_pose',...
    'neutral_pose', ...
    'left_bowl', 'left_side',...
    'right_bowl', 'right_side'
%     'left_intermediate2', 'left_approach', 'left_pickup','left_ready_to_pour','left_pouring','left_pickup_b',...
%     'right_pickup', 'right_clear_bowl', 'right_about_to_pour', 'right_pouring'...
    };

cyton_joint_positions = {...
    %ready_pose, zero_pose, ...
    neutral_pose, ...
    left_bowl, left_side,...
   right_bowl, right_side
%     left_intermediate2,left_approach,left_pickup,left_ready_to_pour,left_pouring, left_pickup_b,...
%     right_pickup,right_clear_bowl,right_about_to_pour,right_pouring...
    };
cyton_ee_positions = cell(size(cyton_positions));
cyton_T_positions = cell(size(cyton_positions));
for i = 1:length(cyton_joint_positions)
    cyton_joint_positions{i} = deg2rad(cyton_joint_positions{i});
    cyton_T_positions{i} = cyton.fkine(cyton_joint_positions{i});
    cyton_ee_positions{i} = cyton_T_positions{i}.t;
    
end

% Lookup end effector xyz position/transforms or joints by Name
cyton_T_map = containers.Map(cyton_positions, cyton_T_positions);
cyton_ee_map = containers.Map(cyton_positions, cyton_ee_positions);
cyton_joint_map = containers.Map(cyton_positions, cyton_joint_positions);

cyton_pose_mat = cell2mat(cyton_ee_positions)';

visualize_poses = 0;
if (visualize_poses)
    figure; hold on;
    cmap = colormap(lines);
    for i = 1:length(cyton_T_positions)
        trplot(cyton_T_positions{i},'length',0.1,'color',cmap(i,:),'framelabel',cyton_positions{i})
    end
end