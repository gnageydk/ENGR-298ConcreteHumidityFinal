function [Saturation] = load_Saturation(allFiles)

%import weather data

%----------START OF HARD CODE-----------%
counterW = 1;
for j = 1 : length(allFiles)
    if(strfind(allFiles(j).name, 'DATALOG-retrieved_at_'))
        ansW = allFiles(j).name;
        
        [num_ansW, ~] = xlsread(ansW);
        
        temp_date = num_ansW(3:end,1); %read first column, skip sometimes erroneous first 3 rows

        for k = 1:length(temp_date)
            if(strfind(allFiles(j).name,'20141207'))
                timeW(k) = (temp_date(k)-4.8*60*60)/86400 + datenum(1970,1,15); %manually fix an error
            elseif(strfind(allFiles(j).name,'20150529'))
                timeW(k) = temp_date(k)/86400 + datenum(1970,1,-3); %convert from UNIX time to matlab time
            else
                timeW(k) = temp_date(k)/86400 + datenum(1970,1,1); %convert from UNIX time to matlab time  
            end
        end
        
        for k = 1:length(num_ansW(:,1))
            for k2 = 2:7
                if num_ansW(k,(2*k2-1)) == 0
                    num_ansW(k,(2*k2-1)) = 1306500;
                else
                    %do nothing
                end                
            end
        end
        
        Satu{counterW,1} = timeW'; %timestamp 
        Satu{counterW,2} = (num_ansW(3:end,3)./817.14).^(1/-1.284); %impedance of Gypsum block 1
        Satu{counterW,3} = (num_ansW(3:end,5)./817.14).^(1/-1.284); %impedance of Gypsum block 2
        Satu{counterW,4} = (num_ansW(3:end,7)./817.14).^(1/-1.284); %impedance of Gypsum block 3
        Satu{counterW,5} = (num_ansW(3:end,9)./817.14).^(1/-1.284); %impedance of Gypsum block 4
        Satu{counterW,6} = (num_ansW(3:end,11)./817.14).^(1/-1.284); %impedance of Gypsum block 5
        Satu{counterW,7} = (num_ansW(3:end,13)./817.14).^(1/-1.284); %impedance of Gypsum block 6        
        
        counterW = counterW + 1;
        clear ansW num_ansW temp_date timeW
    end
    
end
clear counterW

%reformat Saturation file from cell into one vector (Satu)
[tx, ty] = size(Satu);
counter = 1;
for k = 1 : tx %for each file
   for L = 1:length(Satu{k,1}) %for the length of the Saturation File
       time(counter) = Satu{k,1}(L);
       
       for k2 = 1:6
           if Satu{k,k2+1}(L) > 1
               sensor(counter,k2) = 100;
           else
               sensor(counter,k2) = Satu{k,k2+1}(L)*100;
           end  
       end
  
       %sensor(counter,1) = Satu{k,2}(L)*100;
       %sensor(counter,2) = Satu{k,3}(L)*100;
       %sensor(counter,3) = Satu{k,4}(L)*100;
       %sensor(counter,4) = Satu{k,5}(L)*100;
       %sensor(counter,5) = Satu{k,6}(L)*100;
       %sensor(counter,6) = Satu{k,7}(L)*100;
       
       counter = counter + 1;

    end
end
%% sensors represented in datalogs, sensor 0 is right next to B407, sensor 1 is right next to FDDD, etc.
%% B4EC (sensor 3) is 0.5 depth into the sensor from the masterlog, norail better data
array_ref = {'B407', 'FDDD', 'AE1D', 'B4EC', 'AE76', 'FC67'}; %gypsum blocks correspond to depths of these iButton sensors
counter = 1;
for index_final = [5 4 6 3 1 2] %only 6 gypsum sensors total
    Saturation{1,counter} = array_ref{index_final};
    intermediary_sensor(:,1) = time;
    intermediary_sensor(:,2) = sensor(:,index_final);
    Saturation{2,counter} = intermediary_sensor;
    
    counter = counter + 1;
    
end

end