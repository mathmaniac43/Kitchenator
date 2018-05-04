% For the voice client

url = 'http://127.0.0.1:12345/setGoalIngredient';
options = weboptions('RequestMethod', 'post'); % could also be 'post'

nutmeg=audioread('nutmeg.wav');
flour=audioread('flour.wav');

nutmeg=nutmeg';
nutmeg(nutmeg==0) = [];
nutmeg=nutmeg';
nutmeg=abs(nutmeg);
%nutmeg=movmean(nutmeg,50);
%plot(nutmeg)
figure
flour=flour';
flour(flour==0) = [];
flour=flour';
flour=abs(flour);
%cinnamon=movmean(cinnamon,50);
%plot(flour)

while true
    figure('color','white','menu','none')
    text(0.5,0.5, 'Press to speak', 'FontSize', 50, 'Color', 'k','HorizontalAlignment','Center','VerticalAlignment','Middle')
    axis off
    k=waitforbuttonpress
    clf
    axis off
    text(0.5,0.5,'Speak Now', 'FontSize', 50, 'Color', 'k','HorizontalAlignment','Center','VerticalAlignment','Middle')
    recorder = audiorecorder
    disp('Start speaking.')
    recordblocking(recorder, 3);
    disp('End of Recording.');
    play(recorder);
    y = getaudiodata(recorder);
    y=y';
    y(y==0) = [];
    y=y';
    y=abs(y);
    %y=movmean(y,50);
    %figure
    %plot(y)

    checkNut = xcorr(y,nutmeg);
    checkCin = xcorr(y,flour);
    maxNut = max(checkNut)
    maxCin = max(checkCin)

    if maxNut > maxCin
        %Ingredient is nutmeg
        ingredient = 'nutmeg'
    else
        %Ingredient is flour
        ingredient = 'flour'
    end
    stringredient = num2str(ingredient)
    clf
    axis off
    text(0.5,0.5,sprintf('Serving up %s',stringredient), 'FontSize', 35, 'Color', 'k','HorizontalAlignment','Center','VerticalAlignment','Middle')
    response = webwrite(url, ingredient, options); % Get dat string
    %jsonData = jsondecode(ingredient)
    pause(0)
end