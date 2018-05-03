base_radius = 0.15;
resolution = 100;
world_x = 0.7;
world_y = 1;

map = robotics.BinaryOccupancyGrid(world_x,world_y,resolution);
setOccupancy(map, [0 world_y/2], 1);
inflate(map, base_radius);
y = 0:1/resolution:world_y;
x = zeros(size(y));
setOccupancy(map, [x' y'], 1);
show(map)

prm = robotics.PRM;
prm.Map = map;
prm.NumNodes = 100;
p = findpath(prm, [.1 0],[.3 .9]);
show(prm)