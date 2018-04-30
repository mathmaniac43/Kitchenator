% For an arm client, for example
while true
    url = 'http://127.0.0.1:8080/getArmGoals';
    options = weboptions('RequestMethod', 'get'); % could also be 'post'
    data = webread(url, options); % Get dat string
    jsonData = jsondecode(data)
    pause(5)
end