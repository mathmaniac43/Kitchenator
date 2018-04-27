tcp_ip = '127.0.0.1';
tcp_port = 51127;
tcp_socket = tcpclient(tcp_ip, tcp_port, 'timeout', 10);

data = '';
bytes1 = unicode2native(data,'UTF-8');

% Myo setup code goes here:
hMyo etc etc
%

ticksPerMyoRead = 20;
currentGesture = 0;
index = 1
while(1)
   
    % If request:
    if (tcp_socket.BytesAvailable)
        % MYO READ HAPPPENS HERE
        % update currentGesture....
        % END MYO READ 
        
        % Write data to tcp socket
        bytes1 = unicode2native(currentGesture, 'UTF-8');
        write(tcp_socket, bytes1);
    else
        %disp('Nothing received');
    end
end