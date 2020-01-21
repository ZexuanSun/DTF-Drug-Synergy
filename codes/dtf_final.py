#Deep Tensor Factorization
#Author: Zexuan Sun
#This Keras script shows the how the DNN of DTF was built to do the final predictions on missing pairs. 
#About 10% (fold 0) of the known data was used for validation, and the remaining data (fold 1-9) was 
#used for training.



from tensorflow import keras
from tensorflow.keras import models,layers,optimizers
import gzip
import pickle
import pandas as pd
import numpy as np

#Define nomalization and other functions
#It normalizes the input data X. If X is used for training the mean and 
#the standard deviation is calculated during normalization. If X is used 
#for validation or testing, the previously calculated mean and standard 
#deviation of the training data should be used.  If "tanh_norm" is used as
#normalization strategy, then the mean and standard deviation are calculated twice.

def normalize(X, means1=None, std1=None, means2=None, std2=None, norm='tanh_norm'):
    if std1 is None:
        std1 = np.nanstd(X, axis=0)
    X = np.ascontiguousarray(X)
    if norm is None:
        return (X, means1, std1, feat_filt)
    if means1 is None:
        means1 = np.mean(X, axis=0)
    X = (X-means1)/std1
    if norm == 'norm':
        return(X, means1, std1)
    elif norm == 'tanh':
        return(np.tanh(X), means1, std1)
    elif norm == 'tanh_norm':
        X = np.tanh(X)
        if means2 is None:
            means2 = np.mean(X, axis=0)
        if std2 is None:
            std2 = np.std(X, axis=0)
        X = (X-means2)/std2
        return(X, means1, std1, means2, std2)

#function to binarilize data
def binary(data, threshold = 30):
    data[ data < threshold ] = 0
    data[ data >= threshold ] = 1
    return data


#Define the parameters for data generation: 
#folds for testing and validation and normalization strategy
norm = 'tanh'
val_fold = 0

#Load features and labels

#contains the data in both feature ordering
#ways (drug A - drug B - cell line and drug B - drug A - cell line)
#in the first half of the data the features are ordered 
#(drug A - drug B - cell line)
#in the second half of the data the features are ordered 
#(drug B - drug A - cell line)

file = open('final_val_fold_0_features.p.gz', 'rb')
X = pickle.load(file)
file.close()

#features for miss pairs also containing the data in both ordering ways
file = open('final_miss_val_fold_0_features.p.gz', 'rb')
X_miss = pickle.load(file)    
file.close()

#contains synergy values and fold split (numbers 0-9)
data = pd.read_csv('drug_drug_synergy_original_10_fold.csv') 
#labels are duplicated for the two different ways of ordering in the data
double_data = pd.concat([data, data])


#Define indices for splitting

#indices of training data for final model: fold 1-9
idx_train = np.where(double_data['fold']!=val_fold)
#indices of validation data for final model: fold 0
idx_val = np.where(double_data['fold']==val_fold)


#Split data

X_train = X[idx_train]
X_val = X[idx_val]


y_train = double_data.iloc[idx_train]['synergy'].values
#binarilize synergy score
y_train = binary(y_train)
y_val = double_data.iloc[idx_val]['synergy'].values
y_val = binary(y_val)


#Normalize training, test and miss features
if norm == "tanh_norm":
    X_train, mean, std, mean2, std2 = normalize(X_train, norm=norm)
    X_val, mean, std, mean2, std2 = normalize(X_val, mean, std, mean2, std2,  norm=norm)
    X_miss, mean, std, mean2, std2 = normalize(X_miss, mean, std, mean2, std2, norm=norm)    
else:
    X_train, mean, std = normalize(X_train, norm=norm)
    X_val, mean, std = normalize(X_val, mean, std, norm=norm)
    X_miss, mean, std = normalize(X_miss, mean, std, norm=norm)



#Define parameters for the model
nn_struc = [2048, 1024, 512]
learning_rate = 0.000010   
input_dp = 0.2
first_dp = 0.5
second_dp = 0.5


#Build NN model

adam = optimizers.Adam( lr = learning_rate )
model = models.Sequential()
model.add(layers.Dense(nn_struc[0],activation = 'relu',input_shape = (3000,)
                           ,kernel_initializer='he_normal'))
if input_dp != 0:
    model.add(layers.Dropout(input_dp))

model.add(layers.Dense(nn_struc[1], activation='relu',kernel_initializer='he_normal'))

if first_dp != 0:
    model.add(layers.Dropout(first_dp))

if len(nn_struc) == 3:
    model.add(layers.Dense(nn_struc[2], activation='relu',kernel_initializer='he_normal'))

if second_dp != 0:
    model.add(layers.Dropout(second_dp))

model.add(layers.Dense(1, activation='sigmoid'))
model.compile(optimizer= adam, loss='binary_crossentropy',
          metrics =['binary_accuracy'])


#Run model and do the final predicting

early_stopping_cb = keras.callbacks.EarlyStopping(patience = 3, restore_best_weights = True)
hist = model.fit(X_train, y_train, epochs = 1000 ,batch_size = 128,
             validation_data = (X_val,y_val), callbacks = [early_stopping_cb])

miss_pre = model.predict(X_miss)
