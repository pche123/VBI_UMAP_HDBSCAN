import matplotlib.pyplot as plt
import umap
import hdbscan
from scipy import stats as st



def HDBSCAN_UMAP_Application(data,
                           n_healthy,
                           n_mod,
                           n_large,
                           dof_num,
                           n_components = 2, 
                           n_neighbors = 30, 
                           min_dist = 0, 
                           metric_UMAP = 'manhattan', 
                           metric_HDBSCAN = 'euclidean',
                           set_op_mix_ratio=0.90, 
                           plot_flag=False,
                           print_flag=False,
                           min_cluster_size=60,
                           remove_outliers=False,
                           remove_misspec=False):
  
    '''
    Applies the UMAP --> HDBSCAN data pipeline. 
    
    Several comments have been applied to help further contextualize the assumptions made
    and provide advice on how to extend the pipeline to a more practical scenario.
    
    This purpose of this function is to demonstrate the efficacy of the pipeline on several 
    distinct datasets. Without needing to change any hyper-parameters this pipeline works on
    the following 18 distinct datasets, reflect different road profiles, damage locations, 
    sampling rate, and bridge length:
    
    - DSA_B09_DL50_P00 | DSA_B09_DL50_PA1 | DSA_B09_DL50_PA2
    - DSA_B09_DL25_P00 | DSA_B09_DL25_PA1 | DSA_B09_DL25_PA2
    - DSA_B15_DL50_P00 | DSA_B15_DL50_PA1 | DSA_B15_DL50_PA2
    - DSA_B15_DL25_P00 | DSA_B15_DL25_PA1 | DSA_B15_DL25_PA2
    - DSB_B09_DL50_P00 | DSB_B09_DL50_PA1 | DSB_B09_DL50_PA2
    - DSB_B09_DL25_P00 | DSB_B09_DL25_PA1 | DSB_B09_DL25_PA2 
    '''
    
    
    
    # Note that UMAP is applied to the entire observed data set for demonsrration purposes
    # Regardless we still don't know whether or not there is damage, 
    # and also how many types of damage there are,nand at which point we transition 
    # from DM00-->DM20-->DM40 etc. 
    
    # This would be like applying a PCA to the entirety of some observed dataset, 
    # and hoping that cluster information is sufficienly picked up. 
    
    # More information is available here:
    
    #             https://umap-learn.readthedocs.io/en/latest/parameters.html
    
    # If a more sophisiticated train/val/test split is wanted a parametric map of UMAP onto only
    # the healthy data can be applied. More information is available here:
    
    # Cheema, P., Alamdari, M. M., Chang, K. C., Kim, C. W., & Sugiyama, M. (2022). 
    # A drive-by bridge inspection framework using non-parametric clusters over 
    # projected data manifolds. Mechanical Systems and Signal Processing, 180, 109401.
    
    # And over here:
    
    #            https://umap-learn.readthedocs.io/en/latest/parametric_umap.html
    data_points = umap.UMAP(n_neighbors = n_neighbors, n_components = n_components, 
                         min_dist = min_dist,metric=metric_UMAP,
                         set_op_mix_ratio = set_op_mix_ratio, random_state=42).fit_transform(data)

    clusterer = hdbscan.HDBSCAN(metric=metric_HDBSCAN, 
                                prediction_data=True, 
                                min_cluster_size = min_cluster_size).fit(data_points)

    
        
    # THE FOLLOWING IS EXPERIMENTAL 
    #       --> IT IS USED TO PROVIDE COLOR CONSISTENCY AND IN NO WAY EFFECTS THE ABOVE ALGORITHM
    # Further Information:
    # The following is long because HDBSCAN randomly allocates cluster labels in no 
    # particular order. In other words one cannot assume the DM00 is the first cluseter.
    # Thus the following cose is used here to just try to make sure the 
    # same colours for the same clusters are consistenly produced.e.g. DM00 --> green, DM40 --> red
    fig_list = []
    if plot_flag:
        fig = plt.figure()
        fig_list.append(fig)
        plt.title(f'DOF NUMBER: {dof_num+1}')
        plt.xlabel('X Magnitude')
        plt.ylabel('Y Magnitude')

        DM00_flag = True
        DM20_flag = True
        DM40_flag = True
        Outlier_flag = True
        Misspeficiation_flag = True

        healthy_label = None
        mod_label = None
        large_label = None
        outlier_label = -1

        if len(clusterer.labels_) <= n_healthy:
             healthy_label = int(st.mode(clusterer.labels_)[0])

        elif len(clusterer.labels_) <= n_healthy + n_mod:  
            healthy_label = int(st.mode(clusterer.labels_[0:n_healthy])[0])
            mod_label = int(st.mode(clusterer.labels_[n_healthy:-1])[0])

        else:
            healthy_label = int(st.mode(clusterer.labels_[0:n_healthy])[0])
            mod_label = int(st.mode(clusterer.labels_[n_healthy:n_healthy+n_mod])[0])
            large_label = int(st.mode(clusterer.labels_[n_healthy+n_mod:-1])[0])

        for j,label in enumerate(clusterer.labels_):
            if label == healthy_label:
                plt.scatter(data_points[j,0],data_points[j,1],c='g',edgecolors='k',s=150,alpha=0.7,
                         label = 'DM00' if DM00_flag else None)
                DM00_flag = False
            elif label == mod_label:
                plt.scatter(data_points[j,0],data_points[j,1],c='b',edgecolors='k',s=150,alpha=0.7,
                            label = 'DM20' if DM20_flag else None)
                DM20_flag = False  

            elif label == large_label:
                plt.scatter(data_points[j,0],data_points[j,1],c='r',edgecolors='k',s=150,alpha=0.7,
                        label = 'DM40' if DM40_flag else None)
                DM40_flag = False

            elif label == outlier_label:
                if remove_outliers == True:
                    continue
                plt.scatter(data_points[j,0],data_points[j,1],c='k',edgecolors='k',s=150,alpha=0.3,
                        label = 'Outlier' if Outlier_flag else None)
                Outlier_flag = False    

            else:
                # misspec is meant to mean if the cluster color allocations are incorrect e.g. cluster
                # 3 (DM40) is allocated to cluster 1 (DM00) 
                # However the following solution can sometimes be slightly inconsistent 
                if remove_misspec == True:
                    continue
                plt.scatter(data_points[j,0],data_points[j,1],c='y',edgecolors='k',s=150,alpha=0.3,
                        label = 'Misspecified Point(s)' if Misspeficiation_flag else None)
                Misspeficiation_flag = False       

        plt.legend()
        leg = plt.legend()
        for lh in leg.legendHandles: 
            lh._sizes = [300]

    # Final Clustering and Label Allocations
    return [hdbscan.all_points_membership_vectors(clusterer), clusterer.labels_, fig_list]