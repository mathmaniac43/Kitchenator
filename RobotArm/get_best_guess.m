function [q, ck, T] = get_best_guess(xyz_query, draw_plot)
    cyton_poses
    
    if ~exist('draw_plot','var')
        draw_plot = false;
    end
    
    if (length(xyz_query) ~= 3)
        q = zeros(1,cyton.n);
        return
    end
    
    % Nearest Neighbor Search
    idx = knnsearch(cyton_pose_mat, xyz_query);
    ck = cyton_positions{idx};
    qcell = values(cyton_joint_map,{ck});
    Tcell = values(cyton_T_map, {ck});
    T = Tcell{1};
    q = qcell{1};
    if (draw_plot)
        figure; hold on;
        plot3(cyton_pose_mat(:,1), cyton_pose_mat(:,2), cyton_pose_mat(:,3), '*');
        for i = 1:size(cyton_pose_mat,1)
            text(cyton_pose_mat(i,1),cyton_pose_mat(i,2),cyton_pose_mat(i,3),cyton_positions{i});
        end
        plot3(xyz_query(1),xyz_query(2),xyz_query(3),'o');
        plot3(cyton_pose_mat(idx,1), cyton_pose_mat(idx,2), cyton_pose_mat(idx,3));
        legend(cyton_positions);
    end
end