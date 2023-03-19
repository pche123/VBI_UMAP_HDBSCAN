import numpy as np
from scipy.fft import fft
from numpy.random import permutation
from sklearn.utils import resample

def fft_feature_engineering(data_array, nfft):
    '''
    Refers to one observed car data point (one row of input file)
    data_array.shape = (DOFs, end_pos-start_pos)
    '''
    # TODO: Consider about the order of the sum then the log -- is there some theoretical comment here?
    return fft(data_array - data_array.mean(axis=1).reshape(-1,1), axis=1, n=nfft)[:,:nfft//2]
    
    
def log_abs_transform(data):
    return np.log(np.abs(data))


def bootstrap_sampling(data_array_ffts, sample_times=1000):
    '''
    Assumes all the data have been collected into their own post fft [N x nfft] arrays / DOF

    idxs <-- randperm(N)
    train / test / val split (idxs)

    Splits generated once to avoid train-val-test split data leakage problems.
    '''
    

    # Wilcox(2010) writes "599 is recommended for general use."
    # Wilcox, R. R. (2010). Fundamentals of modern statistical methods: Substantially improving power and accuracy. Springer.
    
    num_data, array_length = data_array_ffts.shape # shape of input data
    idxs = permutation(num_data) # random permutation over the indices
    
      
    data_bootstrap_samples = []

    for _ in range(sample_times):
        idxs_resample = resample(idxs)
        data_bootstrap_samples.append(np.mean(data_array_ffts[idxs_resample,:], axis=0))

    return [np.array(data_bootstrap_samples)]


def scale(data):
    scaler = StandardScaler()
    return




# ### I need to see which sections have the majority of the [0,1,2] splits
# # and not just see "which is the first one to appear"
# def remap(clustering_labels):
#     '''
#     remap clustering to reflect order of appearance
#     '''
#     remaped_indices = []
#     _, idx_order = np.unique(clustering_labels,return_index=True)
#     value_order = list(clustering_labels[np.sort(idx_order)])
        
#     print(idx_order)
#     print(value_order)
#     if -1 in value_order: value_order.remove(-1)
    
#     print(value_order)
#     for L in clustering_labels:
#         if L == -1: 
#             remaped_indices.append(-1)
#             continue
#         count = 0
#         for val in value_order:
#             if val == L:
#                 remaped_indices.append(count)
#             count += 1
        
#     return remaped_indices