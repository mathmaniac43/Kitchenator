map = robotics.BinaryOccupancyGrid(10,10,.5)
show(map)
setOccupancy(map,[0,0],1)
setOccupancy(map,[5,5],.5)
show(map)
prm = robotics.PRM
prm.Map = map
prm.NumNodes = 50
p = findpath(prm, [3,0], [5,8])
show(prm)