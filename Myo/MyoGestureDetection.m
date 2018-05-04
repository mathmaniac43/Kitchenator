url = 'http://127.0.0.1:12345/setGestureState';
options = weboptions('RequestMethod', 'post'); 
hMyo = Inputs.MyoUdp.getInstance();
hMyo.initialize();

while(1)

    emgData2init = hMyo.getData;
    emgData2init = hMyo.getData;
    emgData2 = hMyo.getData;

    for i=1:1:1000
        emgData2(i,16)=i/100;
    end

    emgData2 = [emgData2 zeros(1000,1)];
    emgData2(:,17) = emgData2(:,16);
    emgData2(:,16) = 0;

    DC_Avg=500; % number of samples to average for the DC subtraction
    LPF=200;
    Intent = 200;

    %amplify data
    emgData2 = emgData2*10;


    %calculate dc rolling offset
    for i=DC_Avg:1:1000
        emgData2(i,9)=sum(emgData2(i-(DC_Avg-1):i,1)/DC_Avg);
        emgData2(i,10)=sum(emgData2(i-(DC_Avg-1):i,2)/DC_Avg);
        emgData2(i,11)=sum(emgData2(i-(DC_Avg-1):i,3)/DC_Avg);
        emgData2(i,12)=sum(emgData2(i-(DC_Avg-1):i,4)/DC_Avg);
        emgData2(i,13)=sum(emgData2(i-(DC_Avg-1):i,5)/DC_Avg);
        emgData2(i,14)=sum(emgData2(i-(DC_Avg-1):i,6)/DC_Avg);
        emgData2(i,15)=sum(emgData2(i-(DC_Avg-1):i,7)/DC_Avg);
        emgData2(i,16)=sum(emgData2(i-(DC_Avg-1):i,8)/DC_Avg);
    end

    emgData2(1:DC_Avg-1,9)=emgData2(DC_Avg,9);  %Fill in the first DC_Avg samples with a the first average.  s
    emgData2(1:DC_Avg-1,10)=emgData2(DC_Avg,10);
    emgData2(1:DC_Avg-1,11)=emgData2(DC_Avg,11);
    emgData2(1:DC_Avg-1,12)=emgData2(DC_Avg,12);
    emgData2(1:DC_Avg-1,13)=emgData2(DC_Avg,13);  
    emgData2(1:DC_Avg-1,14)=emgData2(DC_Avg,14);
    emgData2(1:DC_Avg-1,15)=emgData2(DC_Avg,15);
    emgData2(1:DC_Avg-1,16)=emgData2(DC_Avg,16);

    %subtract dc offset from original signal
    emgData2(:,9) = abs(emgData2(:,1) - emgData2(:,9));
    emgData2(:,10) = abs(emgData2(:,2) - emgData2(:,10));
    emgData2(:,11) = abs(emgData2(:,3) - emgData2(:,11));
    emgData2(:,12) = abs(emgData2(:,4) - emgData2(:,12));
    emgData2(:,13) = abs(emgData2(:,5) - emgData2(:,13));
    emgData2(:,14) = abs(emgData2(:,6) - emgData2(:,14));
    emgData2(:,15) = abs(emgData2(:,7) - emgData2(:,15));
    emgData2(:,16) = abs(emgData2(:,8) - emgData2(:,16));

    %add some new columns to the datapoint
    emgData2 = [emgData2(:,1:16) zeros(1000,8) emgData2(:,17)];

    %Low pass filter to average data
    for i=LPF:1:1000
        emgData2(i,17)=sum(emgData2(i-(LPF-1):i,9)/LPF);
        emgData2(i,18)=sum(emgData2(i-(LPF-1):i,10)/LPF);
        emgData2(i,19)=sum(emgData2(i-(LPF-1):i,11)/LPF);
        emgData2(i,20)=sum(emgData2(i-(LPF-1):i,12)/LPF);
        emgData2(i,21)=sum(emgData2(i-(LPF-1):i,13)/LPF);
        emgData2(i,22)=sum(emgData2(i-(LPF-1):i,14)/LPF);
        emgData2(i,23)=sum(emgData2(i-(LPF-1):i,15)/LPF);
        emgData2(i,24)=sum(emgData2(i-(LPF-1):i,16)/LPF);
    end

    emgData2(1:LPF-1,17)=emgData2(LPF,17);  %Fill in the first DC_Avg samples with a the first average.  s
    emgData2(1:LPF-1,18)=emgData2(LPF,18);
    emgData2(1:LPF-1,19)=emgData2(LPF,19);
    emgData2(1:LPF-1,20)=emgData2(LPF,20);
    emgData2(1:LPF-1,21)=emgData2(LPF,21);  
    emgData2(1:LPF-1,22)=emgData2(LPF,22);
    emgData2(1:LPF-1,23)=emgData2(LPF,23);
    emgData2(1:LPF-1,24)=emgData2(LPF,24);


    for i=1:1:1000
        for j=17:1:24
            if emgData2(i,j) > .5
                emgData2(i,j) = 1;
            else
                emgData2(i,j) = 0;
            end
        end
    end

    emgData2 = [emgData2(:,1:24) zeros(1000,1) emgData2(:,25)];

    emgData2(:,25)=emgData2(:,19)*128 + emgData2(:,18)*64 + emgData2(:,20)*32 + emgData2(:,23)*16 + emgData2(:,21)*8 + emgData2(:,17)*4 + emgData2(:,22)*2 + emgData2(:,24)*1;

    for i=Intent:1:1000
        emgData2(i,25)=round(sum(emgData2(i-(Intent-1):i,25)/Intent));
    end
    emgData2(1:Intent,25)=emgData2(Intent,25);

    value = sum(emgData2(:,25))/1000

    if value > 200
        %gesture is GO
        gesture = 1
    elseif value > 50
        %gesture is STOP
        gesture = 2
    else
        %no valid gesture
        gesture = 0
    end
    
    response = webwrite(url, num2str(gesture), options);
    
        
    pause(0.1)

end
