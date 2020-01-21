# DTF: Deep Tensor Factorization for Predicting Anticancer Drug Synergy

These are the codes and data mainly used for the project using deep tensor factorization for 
Predicting Anticander Drug Synergy.

The only data set I used here is drug synergy data of 38 drugs and 39 cell lines, which is derived
from the study of ONeil *et al.* .

To implement the DTF model, firstly, I used **R** to preprocess the raw data to build the tensor to be used next for
**Python** and **MATLAB**. For some specific cell lines, there were experiments carried out multiple times for the same drug pairs. In order to construct the three-dimensional (3D) drug-drug-cell-line tensor, we averaged these scores for the same drug-drug pairs. The resulting tensor is provided in the data_sets folder.
To decompose the tensor in matlab, I employed the [Tensor Toolbox](http://www.tensortoolbox.org) and  [L-BFGS-B code](http://users.eecs.northwestern.edu/~nocedal/lbfgsb.html). The Matlab codes are not provided, since with the tensor given, it is not difficult to implement. The results of the tensor decomposition are provided in the form of factor matrices. The python codes are mainly concerning how to generate features based on the output of Matlab and the code to build the final DTF model to do predictions on missing drug combinations are given.



The manuscript of this research project is now avaliable on [arXiv](https://arxiv.org/abs/1911.10313). If you have any questions or suggestions, please feel free to contact me :).


