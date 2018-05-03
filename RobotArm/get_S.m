function [S] = get_S(T_current, T_goal, speed)
%GET_S Summary of this function goes here
%   Detailed explanation goes here
  d = norm(T_goal.t - T_current.t);
  S = 0:speed/d:1;
end

