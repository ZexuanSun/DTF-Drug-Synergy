num_drug_a = 38;
num_drug_b = 38;
num_cell_line = 39;
P = tenones([num_drug_a num_drug_b num_cell_line]);
R = 1000;


%read tensor
exp_tensor = tenzeros([38 38 39]);
for i = 1:39
    file_to_read = strcat('../data_sets/tensor/tensor_',...
        string(i),'.csv');
    exp_tensor(:,:,i) = csvread(file_to_read,1,1);
end



num_predict = 240 * num_cell_line;

P = tenones([num_drug_a num_drug_b num_cell_line]);
%In Matlab index starts from 1
miss = [0, 5, 6, 8, 10, 12, 14, 17, 18, 19, 26, 27, 29, 33, 34, 35] +1;

for k = 1:16
    for j = i+1:16
        P(miss(k),miss(j),:) = 0;
        P(miss(j),miss(k),:) = 0;
    end
end

%get indexes of val set
data = csvread('../data_sets/final_data/fold_0_final.csv')


len = length(data);
    
for k  = 1:len
    z = floor(data(k)/(num_drug_a * num_drug_b)) + 1;
    x_y = mod(data(k), num_drug_a * num_drug_b);
    x = mod(x_y,num_drug_b) + 1;
    y = floor(x_y/num_drug_a) + 1;
    P(x,y,z) = 0;
    P(y,x,z) = 0;
end 

[M,~,output] = cp_wopt(exp_tensor,P,R);

tmp_folder = '/Users/apple/Desktop/tensor_pro/project_sim/final_dtf/' 

to_write_name = strcat(tmp_folder,'drug_a.csv');
csvwrite(char(to_write_name), M.u{1} );

to_write_name = strcat(tmp_folder,'drug_b.csv');
csvwrite(char(to_write_name), M.u{2} );

to_write_name = strcat(tmp_folder,'cell_line.csv');
csvwrite(char(to_write_name), M.u{3} );