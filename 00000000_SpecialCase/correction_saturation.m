function [corr_Humd] = correction_saturation(Humd,Temp)

[~, sensors] = size(Humd);

for index = 1:sensors
    
    tLabel = Humd{1,index}; %sensor ID
    tHumd = Humd{2,index}(:,2); % uncorrected %RH
    tTemp = Temp{2,index}(:,2); % degC
    tTime = Humd{2,index}(:,1); %Matlab time
    dTime = Humd{2,index}(2,1)-Humd{2,index}(1,1); %matlab time diff

    if hour(dTime) == 1; %hours 1 or 0
        %do correction with Humd as-is -- perform calc twice, reconcile at end
        Humd1 = tHumd;
        Humd2 = tHumd;
        Temp1 = tTemp;
        Temp2 = tTemp;
    elseif minute(dTime) == 30; %minutes 30 or 0 (for 60)
        %split Humd into two separate arrays each spaced 1 hour apart
        Humd1 = tHumd(1:2:end); %0 1 2 3 4, e.g.
        Humd2 = tHumd(2:2:end); %0.5, 1.5, 2.5, 3.5, e.g.
        Temp1 = tTemp(1:2:end);
        Temp2 = tTemp(2:2:end);
    end

    [N1, ~] = size(Humd1);
    [N2, ~] = size(Humd2);
            
    %% saturation drift correction 1st hour
    for index1 = 1:N1 %each RH hourly time point within 1 sensor
        sum_Humd1 = 0;
        sum_Temp1 = 0;
        counter1 = 0;
        for k = 1:index1 %considering up the k-th value before end of N1
            if Humd1(k) > 69.9999
                sum_Humd1 = sum_Humd1 + Humd1(k); %RH
                sum_Temp1 = sum_Temp1 + Temp1(k); %degC
                counter1 = counter1 + 1;
            else %if Humd drops below 70, then negate correction
                sum_Humd1 = 0;
                sum_Temp1 = 0;
                counter1 = 0;
            end
                        
        end
            
        avg_Humd1(index1) = sum_Humd1 / counter1; %average of RH over # hours exposed above 70%RH (counter1)
        avg_Temp1(index1) = sum_Temp1 / counter1; %average of Temp over # hours exposed above 70%RH (counter1)
            
        if isnan(avg_Humd1(index1))
            avg_Humd1(index1) = 0;
        elseif isnan(avg_Temp1(index1))
            avg_Temp1(index1) = 0;
        end
                    
        sum_of_errors1(index1) = 0;
        for k = 1:counter1 %considering up to the k-th value that sensor has been exposed to >70%RH before end of N1
            sum_of_errors1(index1) = sum_of_errors1(index1) + (0.0156 * avg_Humd1(index1-counter1+k) * 2.54^(-0.3502 * k))/(1 + (avg_Temp1(index1-counter1+k) - 25)/100);     
        end
        
        corr_Humd1(index1) = Humd1(index1) - sum_of_errors1(index1); %correct each sensor reading
        
    end
    
    %% saturation drift correction for half hour delayed (or repeat)
    for index2 = 1:N2 %each RH hourly time point within 1 sensor
        sum_Humd2 = 0;
        sum_Temp2 = 0;
        counter2 = 0;
        for k = 1:index2 %considering up the k-th value before end of N1
            if Humd2(k) > 69.9999
                sum_Humd2 = sum_Humd2 + Humd2(k); %RH
                sum_Temp2 = sum_Temp2 + Temp2(k); %degC
                counter2 = counter2 + 1;
            else %if Humd drops below 70, then negate correction
                sum_Humd2 = 0;
                sum_Temp2 = 0;
                counter2 = 0;
            end
                        
        end
            
        avg_Humd2(index2) = sum_Humd2 / counter2; %average of RH over # hours exposed above 70%RH (counter1)
        avg_Temp2(index2) = sum_Temp2 / counter2; %average of Temp over # hours exposed above 70%RH (counter1)
            
        if isnan(avg_Humd2(index2))
            avg_Humd2(index2) = 0;
        elseif isnan(avg_Temp2(index2))
            avg_Temp2(index2) = 0;
        end
                    
        sum_of_errors2(index2) = 0;
        for k = 1:counter2 %considering up to the k-th value that sensor has been exposed to >70%RH before end of N1
            sum_of_errors2(index2) = sum_of_errors2(index2) + (0.0156 * avg_Humd2(index2-counter2+k) * 2.54^(-0.3502 * k))/(1 + (avg_Temp2(index2-counter2+k) - 25)/100);     
        end
        
        corr_Humd2(index2) = Humd2(index2) - sum_of_errors2(index2); %correct each sensor reading
        
    end
    
    %% recombine corr_Humd1 and corr_Humd2
    if hour(dTime) == 1; %hours 1 or 0
        %no need to reconcile (already appropriate)
        t_corr_Humd = corr_Humd1; %RH
    elseif minute(dTime) == 30; %minutes 30 or 0 (for 60)
        %recombine separated humidity functions
        N = min(2*N1, 2*N2);
        t_corr_Humd(1:2:2*N1) = corr_Humd1;
        t_corr_Humd(2:2:2*N2) = corr_Humd2;
    end
        
    build_Humd(:,1) = tTime;
    build_Humd(:,2) = t_corr_Humd;
    
    corr_Humd{1,index} = tLabel;
    corr_Humd{2,index} = build_Humd;
    
    clear tLabel tHumd tTemp tTime dTime
    clear Humd1 Humd2 Temp1 Temp2
    clear corr_Humd1 corr_Humd2 t_corr_Humd build_Humd
    

end

end