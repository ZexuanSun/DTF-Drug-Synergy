# Data Sets  Descriptions
 


### basic_info
This folder contains the basic data sets I used. 

* The *drug_drug_synergy_original.csv* is the raw data that I used to build the tensor to be composed, the data of which is divided into 5 fold based on "leave drug combinations out" stratified cross-validation method. 
*drug_drug_synergy_original_10_fold.csv* is a little bit different from the previous file, since I divided the data in 
10 fold, also based on the stratified cross-validation method mentioned above. 

* The axes of the 3-D tensor represent drug-A, drug-B and cell line, respectively. The *drug_names.csv* and *cell_line_names* record the name of the drug or cell linethe number of the axis and its corresponding index of the axis.
Note that they are not ordered alphabetically. 

* The *39_cellines_information.csv* contains the information that the cancer type that each cell line belongs to, which is used for carry out more analysis of the predicting results on missing drug pairs.



### feature_matrices_5_fold
This folder contains the decomposition results for 5 fold cross validation. In the process of cross validation, one fold is used for testing. Since the DTF model is integrated, the tensor to be decomposed is different every time, to be specific, it has different indexes needed to be set as missing. The results of tensor decomposition are given in the form of three factor matrices. The folder *exclude_num* contains the results when fold *num* is used for testing. 
The *drug_a.csv* is the factor matrix for the  drug-A axis. Same rule applies for drug-B and cell line.


### final_data
This folder contains the decomposition results for final DTF model. Note that here 
*drug_drug_synergy_original_10_fold.csv* was used and fold 0 was used for validation. Therefore the index of fold 0 was set as missing before tensor decomposition. The results are also provided in the form of factor matrices. 
The meaning of each file is the same as in previous folder.

### tensor
This folder contains the tensor build based on the *drug_drug_synergy_original.csv*. Note that the missing drug synergy is set as 0.
