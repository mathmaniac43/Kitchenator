url = 'http://127.0.0.1:12345/setGesture';
%url = 'http://192.168.0.10:12345/setGesture';

options = weboptions('RequestMethod', 'post'); 
options.Timeout = 100;
hMyo = Inputs.MyoUdp.getInstance();
hMyo.initialize();
preValue = zeros(10,1);

while(1)

    emgData2 = hMyo.getData;
    emgData2 = hMyo.getData;
    emgData2 = hMyo.getData;

    sample = 100;
    wait = 1/sample;


    for i=1:1:1000
        emgData2(i,16)=i/100;
    end

    emgData2 = [emgData2 zeros(1000,1)];
    emgData2(:,17) = emgData2(:,16);
    emgData2(:,16) = 0;

    %amplify data
    emgData2(:,1) = emgData2(:,1)*10;
    emgData2(:,2) = emgData2(:,2)*10;
    emgData2(:,3) = emgData2(:,3)*10;
    emgData2(:,4) = emgData2(:,4)*10;
    emgData2(:,5) = emgData2(:,5)*10;
    emgData2(:,6) = emgData2(:,6)*10;
    emgData2(:,7) = emgData2(:,7)*10;
    emgData2(:,8) = emgData2(:,8)*10;

    DC_Avg=500; % number of samples to average for the DC subtraction
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

    %subtract dc offset from original signal and take absolute value
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
    LPF = 20;
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

    emgData2(1:LPF-1,17)=emgData2(LPF,17);  %Fill in the first LPF samples with a the first average.  s
    emgData2(1:LPF-1,18)=emgData2(LPF,18);
    emgData2(1:LPF-1,19)=emgData2(LPF,19);
    emgData2(1:LPF-1,20)=emgData2(LPF,20);
    emgData2(1:LPF-1,21)=emgData2(LPF,21);  
    emgData2(1:LPF-1,22)=emgData2(LPF,22);
    emgData2(1:LPF-1,23)=emgData2(LPF,23);
    emgData2(1:LPF-1,24)=emgData2(LPF,24);

    for i=1:1:1000
        if emgData2(i,17) > .5
            emgData2(i,17) = 1;
        else
            emgData2(i,17) = 0;
        end
    
        if emgData2(i,18) > .5
            emgData2(i,18) = 1;
        else
            emgData2(i,18) = 0;
        end
    
        if emgData2(i,19) > 3
            emgData2(i,19) = 1;
        else
            emgData2(i,19) = 0;
        end
    
        if emgData2(i,20) > 1
            emgData2(i,20) = 1;
        else
            emgData2(i,20) = 0;
        end
    
        if emgData2(i,21) > .4
            emgData2(i,21) = 1;
        else
            emgData2(i,21) = 0;
        end
    
        if emgData2(i,22) > .4
            emgData2(i,22) = 1;
        else
            emgData2(i,22) = 0;
        end
    
        if emgData2(i,23) > .4
            emgData2(i,23) = 1;
        else
            emgData2(i,23) = 0;
        end
    
        if emgData2(i,24) > .15
            emgData2(i,24) = 1;
        else
            emgData2(i,24) = 0;
        end
    end

    emgData2 = [emgData2(:,1:24) zeros(1000,1) emgData2(:,25)];

    %Binary Sum
    emgData2(:,25)=emgData2(:,19)*128 + emgData2(:,20)*64 + emgData2(:,18)*32 + emgData2(:,21)*16 + emgData2(:,17)*8 + emgData2(:,22)*4 + emgData2(:,23)*2 + emgData2(:,24)*1;

    %plot(emgData2(:,26),emgData2(:,25))

    value = sum(emgData2(:,25))/1000
    preValue(1:end-1,1) = preValue(2:end,1)
    preValue(end,1) = value;
    
    if value > 125
        %gesture is STOP
        gesture = 2
    %elseif min(preValue > 25) && min(preValue < 70)
    elseif min(preValue > 10) && min(preValue < 70)

        %gesture is GO
        gesture = 1
    else
        %no valid gesture
        gesture = 0
    end
    %jsonencode({'gesture',gesture})
    
    response = webwrite(url, num2str(gesture), options);
    
        
    %pause(0.05)
    pause(1)
end
