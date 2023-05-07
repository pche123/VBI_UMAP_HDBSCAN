import numpy as np
from scipy.fft import fft
from numpy.random import permutation
from sklearn.utils import resample

def fft_feature_engineering(data_array, nfft):
    '''
    Refers to one observed car data point (one row of input file)
    data_array.shape = (DOFs, end_pos-start_pos)
    
    Note: The mean is taken first, then the logarithm
    '''
    return fft(data_array - data_array.mean(axis=1).reshape(-1,1), axis=1, n=nfft)[:,:nfft//2]
    
    
def log_abs_transform(data):
    return np.log(np.abs(data))


def bootstrap_sampling(data_array_ffts, sample_times=1000):
    '''
    Assumes all the data have been collected into their own post fft [N x nfft] arrays / DOF

    sample_times is how many times the data is sampled (with replacement). 
    The default value here is 1000 times, with 599 recommended for general use:
    
    Wilcox(2010) writes "599 is recommended for general use.
    Wilcox, R. R. (2010). Fundamentals of modern statistical methods: Substantially improving power and accuracy. Springer.
    '''
 
    
    num_data, array_length = data_array_ffts.shape # shape of input data
    idxs = permutation(num_data) # random permutation over the indices
    
      
    data_bootstrap_samples = []

    for _ in range(sample_times):
        idxs_resample = resample(idxs)
        data_bootstrap_samples.append(np.mean(data_array_ffts[idxs_resample,:], axis=0))

    return [np.array(data_bootstrap_samples)]
