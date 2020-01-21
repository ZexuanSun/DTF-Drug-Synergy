#generate features for 5 cross validation

import numpy as np
import pandas as pd
import pickle
from pandas import Series, DataFrame
all_drug = pd.read_csv('../data_set//drug_names.csv',index_col=0).values[:,0]
cell_line = pd.read_csv('../data_set//cell_line_names.csv',index_col=0).values[:,0]
raw_data = pd.read_csv('../data_set//drug_drug_synergy_original.csv')
all_len = raw_data.shape[0]
folder_name = '../data_set/feature_matrices_5_fold/'

drug_dict = dict()
cell_line_dict = dict()
for i in range(len(all_drug)):
    drug_dict[all_drug[i]] = i
    
for i in range(len(cell_line)):
    cell_line_dict[cell_line[i]] = i
    

for flag in range(5):
    folder_name = '/Users/apple/Desktop/tensor_pro/project_sim/5_fold_cv/dtf_5_fold/'
    features = np.zeros(2*all_len*3000).reshape(2*all_len,3000)
    drug_a_feature = pd.read_csv(folder_name +'exclude_'+ str(flag) + '/' + 'drug_a.csv',header=None)
    drug_b_feature = pd.read_csv(folder_name + 'exclude_'+ str(flag) + '/' 'drug_b.csv',header = None)
    cell_line_feature = pd.read_csv(folder_name +'exclude_'+ str(flag) + '/''cell_line.csv', header = None)
    for i in range(all_len):
        tmp_item = raw_data.iloc[i]
        x = drug_dict[tmp_item.drug_a_name]
        y = drug_dict[tmp_item.drug_b_name]
        z = cell_line_dict[tmp_item.cell_line]
        tmp_fold = tmp_item.fold
        #if fold != flag and fold !=0
        features[i,0:1000] = drug_a_feature.values[x,:]
        features[i,1000:2000] = drug_b_feature.values[y,:]
        features[i,2000:3000] = cell_line_feature.values[z,:]
        features[i + all_len ,0:1000] = drug_a_feature.values[y,:]
        features[i + all_len ,1000:2000] = drug_b_feature.values[x,:]
        features[i + all_len ,2000:3000] = cell_line_feature.values[z,:]
    file_name = folder_name + 'exclude_'+ str(flag)  + '_features.p.gz'
    outfile = open(file_name, 'wb')
    pickle.dump(features, outfile)
    outfile.close()



#generate features for final dtf model

#train and validation features
folder_name = '../data_set/final_feature_matrices/'
features = np.zeros(2*all_len*3000).reshape(2*all_len,3000)
drug_a_feature = pd.read_csv(folder_name  + 'drug_a.csv',header=None)
drug_b_feature = pd.read_csv(folder_name + 'drug_b.csv',header = None)
cell_line_feature = pd.read_csv(folder_name +'cell_line.csv', header = None)
for i in range(all_len):
    tmp_item = raw_data.iloc[i]
    x = drug_dict[tmp_item.drug_a_name]
    y = drug_dict[tmp_item.drug_b_name]
    z = cell_line_dict[tmp_item.cell_line]
    tmp_fold = tmp_item.fold
    #if fold != flag and fold !=0
    features[i,0:1000] = drug_a_feature.values[x,:]
    features[i,1000:2000] = drug_b_feature.values[y,:]
    features[i,2000:3000] = cell_line_feature.values[z,:]
    features[i + all_len ,0:1000] = drug_a_feature.values[y,:]
    features[i + all_len ,1000:2000] = drug_b_feature.values[x,:]
    features[i + all_len ,2000:3000] = cell_line_feature.values[z,:]
file_name = folder_name + 'final_val_fold_0_features.p.gz'
outfile = open(file_name, 'wb')
pickle.dump(features, outfile)
outfile.close()

#get  features for missing pairs and record the index of missing pairs
miss_features = np.zeros(240*39*3000).reshape(240*39,3000)
miss_index = np.zeros(240*39)
miss_list = [0, 5, 6, 8, 10, 12, 14, 17, 18, 19, 26, 27, 29, 33, 34, 35]

num = 0
for z in range(39):#z
    for i in range(16):#x
        for j in range(i+1,16):#y
            x = miss_list[i]
            y = miss_list[j]
            miss_features[num,:1000] = drug_a_feature.values[x,:]
            miss_features[num,1000:2000] = drug_b_feature.values[y,:]
            miss_features[num,2000:3000] = cell_line_feature.values[z,:]
            tmp_index = x + 38*y + z*38*38
            miss_index[num] = tmp_index
            miss_features[num + 120*39,:1000] = drug_a_feature.values[x,:]
            miss_features[num + 120*39,1000:2000] = drug_b_feature.values[y,:]
            miss_features[num + 120*39,2000:3000] = cell_line_feature.values[z,:]
            tmp_index = y + 38*x + z*38*38
            miss_index[num + 120*39] = tmp_index
            num += 1
file_name = folder_name + 'final_miss_val_fold_0_features.p.gz'
outfile = open(file_name, 'wb')
pickle.dump(miss_features, outfile)
outfile.close()
np.savetxt(folder_name+'miss_index.txt',miss_index)





