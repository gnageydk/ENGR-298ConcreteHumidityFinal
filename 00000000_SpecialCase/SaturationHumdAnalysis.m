%Data analysis of sensors in concrete

clear all
clc

check_test = {'AE76';'B4EC';'FC67';'AE1D';'B407';'FDDD'}; %working RH sensors

%% ----------START OF HARD CODE----------- %%

allFiles = dir;

%import MasterList.csv
[num_ansMList, tex_ansMList] = xlsread('MasterList.csv');

%% Search for all sensors from what's available in directory
counter = 1;
for j = 1 : length(dir) %all files in the directory
    for k = 1:length(tex_ansMList) %cross-reference to sensors in MasterList
        if(strfind(allFiles(j).name, tex_ansMList{k}))
            indexDir(counter)   = j; %element index for directory
            indexMList(counter) = k; %element index for MasterList
            counter = counter + 1;
        end
    end
end

%% ------------Load temp/RH/weather CSV files
'Begin loading all files'

[iButton,Temp,raw_Humd] = load_TempRH(allFiles,indexDir);
[Satu] = load_Saturation(allFiles);

'All files loaded', cputime

%% saturation drift correction
%[Humd] = correction_saturation(raw_Humd,Temp);

'RH saturation drift is complete', cputime

%% ------------Plot temp/RH CSV files
'Begin plotting', cputime

counter = 1;
for n = 1:2:length(indexMList) %for all sensors (half because of Temp/Humd)
    sub_tex_ansMList{counter,1} = tex_ansMList{indexMList(n),1}; %sensor id
    sub_tex_ansMList{counter,2} = tex_ansMList{indexMList(n),2}; %specimen name
    sub_tex_ansMList{counter,3} = tex_ansMList{indexMList(n),3};
    sub_tex_ansMList{counter,4} = strcat(tex_ansMList{indexMList(n),2},tex_ansMList{indexMList(n),3});
    sub_tex_ansMList{counter,5} = num2str(num_ansMList(indexMList(n),1));
    sites{counter,1} = sub_tex_ansMList{counter,4};
    
    counter = counter + 1;
end



Humd = raw_Humd;

new_Humd(:,1) = [[Humd{2,1}(:,1)];[Humd{2,2}(:,1)];[Humd{2,3}(:,1)]];
new_Humd(:,2) = [[Humd{2,1}(:,2)];[Humd{2,2}(:,2)];[Humd{2,3}(:,2)]];

%new_Satu(:,1) = [[Satu{2,1}(:,1)];[Satu{2,2}(:,1)];[Satu{2,3}(:,1)]];
%new_Satu(:,2) = [[Satu{2,1}(:,2)];[Satu{2,2}(:,2)];[Satu{2,3}(:,2)]];

new_Temp(:,1) = [[Temp{2,1}(:,1)];[Temp{2,2}(:,1)];[Temp{2,3}(:,1)]];
new_Temp(:,2) = [[Temp{2,1}(:,2)];[Temp{2,2}(:,2)];[Temp{2,3}(:,2)]];

cell_Humd = {'FC67'; new_Humd};
%cell_Satu = {'FC67'; new_Satu};
cell_Temp = {'FC67'; new_Temp};

fin_Humd = {cell_Humd{1,1}, Humd{1,4}, Humd{1,5}, Humd{1,6}, Humd{1,7}, Humd{1,8}; ...
            cell_Humd{2,:}, Humd{2,4}, Humd{2,5}, Humd{2,6}, Humd{2,7}, Humd{2,8}};
%fin_Satu = {cell_Satu{1,1}, Satu{1,4}, Satu{1,5}, Satu{1,6}; ...
%            cell_Satu{2,:}, Satu{2,4}, Satu{2,5}, Satu{2,6}};   
fin_Temp = {cell_Temp{1,1}, Temp{1,4}, Temp{1,5}, Temp{1,6}, Temp{1,7}, Temp{1,8}; ...
            cell_Temp{2,:}, Temp{2,4}, Temp{2,5}, Temp{2,6}, Temp{2,7}, Temp{2,8}};         

sub_tex_ansMList = sub_tex_ansMList(3:end,:);

%plot(Satu{2,3}(:,1)-Satu{2,3}(1,1),Satu{2,3}(:,2),'ko',fin_Humd{2,1}(:,1)-fin_Humd{2,1}(1,1),fin_Humd{2,1}(:,2),'r^',fin_Temp{2,1}(:,1)-fin_Temp{2,1}(1,1),fin_Temp{2,1}(:,2),'gs')

last_Humd = fin_Humd(:,1);
last_Temp = fin_Temp(:,1);
last_Satu = Satu(:,3);
last_sub_tex_ansMList = sub_tex_ansMList(1,:);

[last_Humd] = correction_saturation(last_Humd,last_Temp);

sites = unique(sites);
last_sites = sites(1);
for n = 2% 1:length(sites)+1
    %plot_Humd_Pruckner_time(PrucknerHumd,sites,sub_tex_ansMList,n)
    %plot_Humd_Bolton_time(BoltonHumd,sites,sub_tex_ansMList,n)
    %plot_Humd_time(Humd,sites,sub_tex_ansMList,n,check_test)
    
    %plot_Satu_time(Satu,sites,sub_tex_ansMList,n,check_test)
    
    %plot_Humd_Pruckner_depth(PrucknerHumd,time_Wthr,time_RH_int_bal,RH_int_bal,RH_Wthr_air,RH_Bal_top,RH_Bal_top_time,RH_Bal_bot,RH_Bal_bot_time,sites,sub_tex_ansMList,z,n)
    %plot_Humd_Bolton_depth(BoltonHumd,time_Wthr,time_RH_int_bal,RH_int_bal,RH_Wthr_air,RH_Bal_top,RH_Bal_top_time,RH_Bal_bot,RH_Bal_bot_time,sites,sub_tex_ansMList,z,n)
    %plot_Humd_depth_troubleshoot(Humd,time_Wthr,time_RH_int_bal,RH_int_bal,RH_Wthr_air,RH_Bal_top,RH_Bal_top_time,RH_Bal_bot,RH_Bal_bot_time,sites,sub_tex_ansMList,z,n,check_test)
    %plot_Humd_depth(Humd,time_Wthr,time_RH_int_bal,RH_int_bal,RH_Wthr_air,RH_Bal_top,RH_Bal_top_time,RH_Bal_bot,RH_Bal_bot_time,sites,sub_tex_ansMList,z,n,check_test)
 
    %plot_Humd_Pruckner_scatter(PrucknerHumd,time_Wthr,time_RH_int_bal,RH_int_bal,RH_Wthr_air,RH_Bal_top,RH_Bal_top_time,RH_Bal_bot,RH_Bal_bot_time,sites,sub_tex_ansMList,z,n)
    %plot_Humd_Bolton_scatter(BoltonHumd,time_Wthr,time_RH_int_bal,RH_int_bal,RH_Wthr_air,RH_Bal_top,RH_Bal_top_time,RH_Bal_bot,RH_Bal_bot_time,sites,sub_tex_ansMList,z,n)
    %plot_Humd_scatter(Humd,time_Wthr,time_RH_int_bal,RH_int_bal,RH_Wthr_air,RH_Bal_top,RH_Bal_top_time,RH_Bal_bot,RH_Bal_bot_time,sites,sub_tex_ansMList,z,n,check_test)
    
    %plot_Satu_scatter(Humd,Temp,Satu,sites,sub_tex_ansMList,n,check_test)
    %plot_Satu_scatter(fin_Humd,fin_Temp,Satu,sites,sub_tex_ansMList,n,check_test)
    [temp_tHumd,temp_tSatu,temp_tTemp,temp_tTime] = plot_Satu_scatter(last_Humd,last_Temp,last_Satu,last_sites,last_sub_tex_ansMList,n,check_test);
end

%% 
'end of all operations', cputime

