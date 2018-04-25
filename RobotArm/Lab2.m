udp = PnetClass(8889, 8888, '127.0.0.1');
udp.initialize();
currentAngles = zeros(1,8);
q = [0 -0.7 0 0.7 0 -0.7 0];
desiredAngles = [q, 0.01];

udp.putData(typecast(desiredAngles,'uint8'))
bytes = udp.getData();
angles = typecast(bytes,'double');