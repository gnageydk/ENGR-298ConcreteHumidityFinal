function [temp_tHumd,temp_tSatu,temp_tTemp,temp_tTime] = plot_Satu_scatter(Humd,Temp,Satu,sites,sub_tex_ansMList,n,check_test)

%% find earliest start and latest times of sensors (not weather)
[tx, ty] = size(Humd);
for k = 1:ty %length(Humd)
    tHumdArray = Humd{2,k};
    tMinHumdTime(k) = tHumdArray(1,1);
    tMaxHumdTime(k) = tHumdArray(end,1);
end
MinHumdTime = min(tMinHumdTime);
MaxHumdTime = max(tMaxHumdTime);

%for k = 1:length(Satu)
%    tSatuArray = Satu{2,k};
%    tMinSatuTime(k) = tSatuArray(1,1);
%    tMaxSatuTime(k) = tSatuArray(end,1);
%end
%MinSatuTime = min(tMinSatuTime);
%MaxSatuTime = max(tMaxSatuTime);

%% Fig 1 Plot all installed Humidities as function of depth
counter = 1;
%temp_Humd_int = zeros(length(z),length(time_Wthr));

[tx, ~] = size(sub_tex_ansMList);
if n > 1 %plot individual wrt time
    for k = 1:tx %length(sub_tex_ansMList)
        if sites{n-1} == sub_tex_ansMList{k,4}
            for k_sub = 1:length(check_test)
                if Humd{1,k} == check_test{k_sub}
                    tHumd{counter} = Humd{2,k};
                    tTemp{counter} = Temp{2,k};
                    tSatu{counter} = Satu{2,k};
                    tLegendHumd{counter} = sub_tex_ansMList{k,5};
                    tDepth(counter) = str2num(sub_tex_ansMList{k,5});
                    daysHumd{counter} = tHumd{counter}(:,1) - MinHumdTime;
            
                    counter = counter + 1;
                end
            end
        end
    end
    
    %% sort iButton data based on depth
    [~, s_index] = sort(tDepth);
    tDepth = tDepth(s_index);
    
%----------------modify all data types to least frequent time -- iButton
%% modifying Gypsum/Saturation data to iButton (make it less frequent; easier to plot)
    counter_t = 1;
    counter_s = 1;
    for index_sensor = s_index %for each sensor arranged by tDepth
        for index_timeSensor = 1:length(tHumd{index_sensor}(:,1)) %run through iButton times for that sensor
            time_value_to_find = tHumd{index_sensor}(index_timeSensor,1); %scalar Matlab time value
            test_time = tSatu{index_sensor}(:,1); %1D array Matlab time
            [min_value min_index] = min(abs(test_time - time_value_to_find));
            
            if abs(test_time - time_value_to_find) > datenum(0,0,0,1,0,0) %if time diff is greater than 1 hour
                %do nothing
            else
                temp_tSatu(counter_t,counter_s) = tSatu{index_sensor}(min_index,2);
                temp_tHumd(counter_t,counter_s) = tHumd{index_sensor}(index_timeSensor,2);
                temp_tTemp(counter_t,counter_s) = tTemp{index_sensor}(index_timeSensor,2);
                temp_tTime(counter_t,counter_s) = tHumd{index_sensor}(index_timeSensor,1);
                
                counter_t = counter_t + 1;
            end

            clear test_time min_value min_index
        end
        counter_s = counter_s + 1;
    end

    %Pruckner Adsorption Isotherm
        R = 8.314; %J/Kmol
        del_u_mono = -17e3; %J/mol Pruckner 
        SD_o = [100; 100]; %wetting and drying, %RH
        alpha_o = [0.01; 0.01]; %wetting and drying, -/-
        RH_b = [98; 89]; %wetting and drying, %RH        
        reg_n = [2; 7.5]; %regression coefficient
        
        RH = [1:0.1:99.999 99.9999 99.99999 99.999999 99.9999999 99.99999999 99.999999999];
        for index_RH = 1:length(RH)
            temp_tDegS(index_RH) = (1-log(abs((R*(25+273)*log(RH(index_RH)/100))/del_u_mono)))/ ...
                                   (1-log(abs((R*(25+273)*log(99.9999999999/100))/del_u_mono)))*100;
            
            
            %(1-log((R*298*log(RH(index_RH)/100))/del_u_mono)) / ...
            %                       (1-log((R*298*log(99.99/100))/del_u_mono)) * 100;
                               
            temp_tWetS(index_RH) = SD_o(1) *(alpha_o(1)*((1-alpha_o(1))/(1+((1-RH(index_RH)/100)/(1-RH_b(1)/100))^reg_n(1))))*100;
            
            temp_tDryS(index_RH) = SD_o(2) *(alpha_o(2)*((1-alpha_o(2))/(1+((1-RH(index_RH)/100)/(1-RH_b(2)/100))^reg_n(2))))*100;
        end
            

%% modifying start and end times based on iButton data
    %absolute earliest and latest run times (in order for data to coincide optimally)
    %MinTime = max(MinHumdTime,MinSatuTime);
    %MaxTime = min(MaxHumdTime,MaxSatuTime);

    %[min_value min_index] = min(abs(
    %[min_value min_index] = min(abs(time_Wthr - MinHumdTime));
    %[max_value max_index] = min(abs(time_Wthr - MaxHumdTime));
        
    %t_start = min_index + 0; %don't add buffer because predictive RH model is OK
    %t_end = max_index;
    
  %  clear min_index max_index    
    
    
%% final plotting of RH
    figure(length(sites)+1+ n - 1)
            axis([0 120 0 120]); %axis([xmin xmax ymin ymax])
            set(gca,'FontSize',28)
            grid
            title(sprintf('Correlation Between Relative Humiditiy and Degree of Saturation at %s', sites{n-1}))
            xlabel('Measured Relative Humidity, %')
            ylabel('Measured Degree of Saturation, %')
    
    %index_t = t_start:t_end;
        
        %RH
        hold on
            %h6 = plot([1:99],[temp_tDegS],'k-');
            %set([h6(1)],'linewidth',3)
            

        
        if length(tDepth) == 1
            %1st sensor
         %   h1 = plot(temp_tHumd(1:end,1),temp_tSatu(1:end,1),'bd');
            %h1 = plot(temp_tHumd(:,1),temp_tSatu(:,1),'ko');
         %   set([h1(1)],'MarkerSize',12)
            
         
            h1_wet = plot(temp_tHumd(1:575,1),temp_tSatu(1:575,1),'ko');
            set([h1_wet(1)],'MarkerSize',12)
            
            h1_dry = plot(temp_tHumd(910:3650,1),temp_tSatu(910:3650,1),'r^');
            set([h1_dry(1)],'MarkerSize',12)
            
            h7 = plot(RH,temp_tWetS,'k--');
            set([h7(1)],'linewidth',3)
            
            h8 = plot(RH,temp_tDryS,'r-.');
            set([h8(1)],'linewidth',3)            
            
            h9 = plot(RH,temp_tDegS,'b:');
            set([h9(1)],'linewidth',3)
            
            legend([h1_wet(1) h1_dry(1) h7(1) h8(1) h9(1)],{'Wetting','Drying','Wet Fit','Dry Fit','Pruckner'},'Orientation','horizontal','Location','northwest')
            
            %legend
            %legend([h1(1)],{sprintf('%s', tLegendHumd{s_index(1)})},'Orientation','horizontal','Location','northwest')
            %legend([h1(1) h6(1)],{sprintf('%s', tLegendHumd{s_index(1)}),'Theoretical Adsorption Isotherm'},'Orientation','horizontal','Location','northwest')
            %legend([h1(1) h6(1)],{sprintf('%s', tLegendHumd{s_index(1)}),'Line of Equality'},'Orientation','horizontal','Location','northwest')                             
    %    elseif length(tDepth) == 2
    %        %1st sensor
    %        h1 = plot(temp_tHumd(:,1),temp_Humd_int(ceil(tDepth(1)*25.4),:),'ko');
    %        set([h1(1)],'MarkerSize',12)
    %        %2nd sensor
    %        h2 = plot(temp_tHumd(:,2),temp_Humd_int(ceil(tDepth(2)*25.4),:),'r^');
    %        set([h2(1)],'MarkerSize',12)
    %        %legend
    %        legend([h1(1) h2(1) h6(1)],{sprintf('%s', tLegendHumd{s_index(1)}),sprintf('%s', tLegendHumd{s_index(2)}),'Line of Equality'},'Orientation','horizontal','Location','northwest')                   
        %elseif length(tDepth) == 3
        elseif length(tDepth) == 3
            %1st sensor
            h1 = plot(temp_tHumd(:,1),temp_tSatu(:,1),'ko');
            %h1 = plot(temp_tHumd(:,1),temp_Humd_int(ceil(tDepth(1)*25.4),:),'ko');
            set([h1(1)],'MarkerSize',12)
            %2nd sensor
            h2 = plot(temp_tHumd(:,2),temp_tSatu(:,2),'r^');
            %h2 = plot(temp_tHumd(:,2),temp_Humd_int(ceil(tDepth(2)*25.4),:),'r^');
            set([h2(1)],'MarkerSize',12)
            %3rd sensor
            h3 = plot(temp_tHumd(:,3),temp_tSatu(:,3),'bd');
            %h3 = plot(temp_tHumd(:,3),temp_tSatu(:,3),'gs');
            %h3 = plot(temp_tHumd(:,3),temp_Humd_int(ceil(tDepth(3)*25.4),:),'gs');
            set([h3(1)],'MarkerSize',12)
            %legend
     %       legend([h3(1) h6(1)],{sprintf('%s', tLegendHumd{s_index(3)}),'Theoretical Adsorption Isotherm'},'Orientation','horizontal','Location','northwest') 
     %      legend([h2(1) h3(1) h6(1)],{sprintf('%s', tLegendHumd{s_index(2)}),sprintf('%s', tLegendHumd{s_index(3)}),'Theoretical Adsorption Isotherm'},'Orientation','horizontal','Location','northwest') 
           legend([h1(1) h2(1) h3(1) h6(1)],{sprintf('%s', tLegendHumd{s_index(1)}),sprintf('%s', tLegendHumd{s_index(2)}),sprintf('%s', tLegendHumd{s_index(3)}),'Theoretical Adsorption Isotherm'},'Orientation','horizontal','Location','northwest')                   
     %   elseif length(tDepth) == 4
     %       %1st sensor
     %       h1 = plot(temp_tHumd(:,1),temp_Humd_int(ceil(tDepth(1)*25.4),:),'ko');
     %       set([h1(1)],'MarkerSize',12)
     %       %2nd sensor
     %       h2 = plot(temp_tHumd(:,2),temp_Humd_int(ceil(tDepth(2)*25.4),:),'r^');
     %       set([h2(1)],'MarkerSize',12)
     %       %3rd sensor
     %       h3 = plot(temp_tHumd(:,3),temp_Humd_int(ceil(tDepth(3)*25.4),:),'gs');
     %       set([h3(1)],'MarkerSize',12)
     %       %4th sensor
     %       h4 = plot(temp_tHumd(:,4),temp_Humd_int(ceil(tDepth(4)*25.4),:),'bd');
     %       set([h4(1)],'MarkerSize',12)
     %       %legend
     %       legend([h1(1) h2(1) h3(1) h4(1) h6(1)],{sprintf('%s', tLegendHumd{s_index(1)}),sprintf('%s', tLegendHumd{s_index(2)}),sprintf('%s', tLegendHumd{s_index(3)}),sprintf('%s', tLegendHumd{s_index(4)}),'Line of Equality'},'Orientation','horizontal','Location','northwest')                   
     %   elseif length(tDepth) == 5
     %       %1st sensor
     %       h1 = plot(temp_tHumd(:,1),temp_Humd_int(ceil(tDepth(1)*25.4),:),'ko');
     %       set([h1(1)],'MarkerSize',12)
     %       %2nd sensor
     %       h2 = plot(temp_tHumd(:,2),temp_Humd_int(ceil(tDepth(2)*25.4),:),'r^');
     %       set([h2(1)],'MarkerSize',12)
     %       %3rd sensor
     %       h3 = plot(temp_tHumd(:,3),temp_Humd_int(ceil(tDepth(3)*25.4),:),'gs');
     %       set([h3(1)],'MarkerSize',12)
     %       %4th sensor
     %       h4 = plot(temp_tHumd(:,4),temp_Humd_int(ceil(tDepth(4)*25.4),:),'bd');
     %       set([h4(1)],'MarkerSize',12)
     %       %5th sensor
     %       h5 = plot(temp_tHumd(:,5),temp_Humd_int(ceil(tDepth(5)*25.4),:),'cp');
     %       set([h5(1)],'MarkerSize',12)
     %       %legend
     %       legend([h1(1) h2(1) h3(1) h4(1) h5(1) h6(1)],{sprintf('%s', tLegendHumd{s_index(1)}),sprintf('%s', tLegendHumd{s_index(2)}),sprintf('%s', tLegendHumd{s_index(3)}),sprintf('%s', tLegendHumd{s_index(4)}),sprintf('%s', tLegendHumd{s_index(5)}),'Line of Equality'},'Orientation','horizontal','Location','northwest')
        end
        
     
                
end

end