function [iButton,Temp,Humd] = load_TempRH(allFiles,indexDir)

%How many iButtons + weather were used?
iButton = length(indexDir)./2;

%Create empty cell arrays whose # columns is equal to number of iButtons
%Temp = cell(2,iButton);
%Humd = cell(2,iButton);

%import temp/RH CSV files
counterT = 1;
counterR = 1;
for j = 1 : length(indexDir)
    k = indexDir(j);
    if(strfind(allFiles(k).name, 'TOP'))
        'do nothing';
    elseif(strfind(allFiles(k).name, 'MID'))
        'do nothing';
    elseif(strfind(allFiles(k).name, 'BOT'))
        'do nothing';
    elseif(strfind(allFiles(k).name, '_Temp.csv'))
        ansT = allFiles(k).name;
        
        [num_ansT, tex_ansT] = xlsread(ansT);
        Temp{1,counterT} = tex_ansT{2}(47:50);  %(1:2) shortens the name of the sensor
        for L = 21:length(tex_ansT)
            timeT(L-20) = datenum(tex_ansT{L});
        end
        Temp{2,counterT} = [timeT', num_ansT];
        
        counterT = counterT + 1;
        clear ansT num_ansT tex_ansT timeT
    elseif(strfind(allFiles(k).name, '_RH.csv'))
        ansR = allFiles(k).name;
        
        [num_ansR, tex_ansR] = xlsread(ansR);
        Humd{1,counterR} = tex_ansR{2}(47:50);  %(1:2) shortens the name of the sensor
        for L = 21:length(tex_ansR)
            timeR(L-20) = datenum(tex_ansR{L});
        end
        Humd{2,counterR} = [timeR', num_ansR];
        
        counterR = counterR + 1;
        clear ansR num_ansR tex_ansR timeR
    end
end

end