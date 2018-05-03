tcp_ip = '127.0.0.1';
tcp_port = 51123;
tcp_socket = tcpclient(tcp_ip, tcp_port, 'timeout', 10);

data = 'hello world';
bytes1 = unicode2native(data,'UTF-8');
while(1)
   
   write(tcp_socket, bytes1)
if (tcp_socket.BytesAvailable)
    bytes = read(tcp_socket);
    string = native2unicode(bytes);
    disp(string)
    goal_msg = jsondecode(string);
    disp(goal_msg)
else
    %disp('Nothing received');
end
end