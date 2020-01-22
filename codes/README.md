# Codes Descriptions

* tensor_generate.R
The R code can be used to build the raw tensor. In order to be used directly by Matlab, the missing drug synergy score was set as 0. I have recorded the missing positions in another way.

* cpwopt_final.m
The Matlab code can be used to do the final tensor decomposition. Note that fold 0 was used for validation and was set as missing. The codes to implement 5 fold cross validation is not difficult to implement, which is similar to this code.




* generate_features.py
This python code can be used to generate features for 5 fold cross validation and final DTF based on the factor matrices derived from tensor decomposition.

* dtf_final.py
This python code can be used to implement the DNN of the final DTF model and do the final predictions on missing drug combinations.




More detailed comments are given along with the codes.