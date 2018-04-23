'''
 The Arm Manager/Client:

 -> Queries the state, if state is 'delivering' then query goalPos 
    (or maybe get it all as one json chunk)
 -> Start moving along waypoints, calling to query the state along the way??
 -> if state is 'delivering' & gesture = $StopGesture then pause, keep waiting for instructions
 -> etc, etc


'''