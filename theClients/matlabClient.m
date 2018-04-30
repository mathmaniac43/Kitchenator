% For an arm client, for example
while true
    url = 'http://127.0.0.1:8080/getArmGoals';
    data = webread(url); % Get dat string
    jsonData = jsondecode(data)
    pause(5)
end