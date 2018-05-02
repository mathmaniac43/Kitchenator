function [x] = get_pose_by_name(pose_name, pose_map)
    cyton_poses
    
    v = values(pose_map, {pose_name});
    x = v{1};
end