import matplotlib.pyplot as plt
import umap
import hdbscan
from scipy import stats as st





# Needs updating of default values -- DONE
def theoretical_clustering(data,
                           n_healthy,
                           n_mod,
                           n_large,
                           dof_num,
                           n_components = 2, 
                           n_neighbors = 30, 
                           min_dist = 0, 
                           metric = 'manhattan', 
                           set_op_mix_ratio=0.95, 
                           plot_flag=False,
                           print_flag=False,
                           total_obs=2):
    

    '''
    The theoretical grouping to expect, based on a supervised knowledge
    of which data is healthy, moderate damag, and large damage.
    
    Note that unlike HDBSCAN_UMAP_Application, min_cluster_size doesn't need
    to be specified here, because we are considering the theoretical groupings
    which are known ahead of time already. 
    '''
    
    n_data = data.shape[0]
    cs = ['1']*n_healthy + ['2']*n_mod + ['3']*n_large # Theoretical Groupings, cs="colours"
    umap_results = {}
    
    for i in range(1,total_obs+1):
        sub_data = data[0:n_data*i//total_obs,:]
        sub_colours = list(map(int,cs))[0:n_data*i//total_obs] # string to int

        umap_obj = umap.UMAP(n_neighbors = n_neighbors, n_components= n_components, 
                             min_dist=min_dist,metric=metric,
                             set_op_mix_ratio=set_op_mix_ratio, random_state=42).fit(sub_data)
        
        data_points = umap_obj.transform(sub_data)

        if plot_flag:
            plt.figure()
            plt.title(f'DOF NUMBER: {dof_num+1}, OBSERVATION: {i}/{total_obs}')
            plt.xlabel('X Magnitude')
            plt.ylabel('Y Magnitude')
            
            DM00_flag = True
            DM20_flag = True
            DM40_flag = True
            
            # inefficient looping
            for j, col in enumerate(sub_colours):
                if col == 1:
                    plt.scatter(data_points[j,0],data_points[j,1],c='g',edgecolors='k',s=150,alpha=0.7,
                             label = 'DM00' if DM00_flag else None)
                    DM00_flag = False
                elif col == 2:
                    plt.scatter(data_points[j,0],data_points[j,1],c='b',edgecolors='k',s=150,alpha=0.7,
                            label = 'DM20' if DM20_flag else None)
                    DM20_flag = False
                else:
                    plt.scatter(data_points[j,0],data_points[j,1],c='r',edgecolors='k',s=150,alpha=0.7,
                            label = 'DM40' if DM40_flag else None)
                    DM40_flag = False
                    
            plt.legend()
            leg = plt.legend()
            for lh in leg.legendHandles: 
                lh._sizes = [300]

                    
        if print_flag: print(f'{i}/{total_obs}')
        
        umap_results[f'{i}_Umap_Object'] = umap_obj
        umap_results[f'{i}_Sub_Data_Fit'] = sub_data
        umap_results[f'{i}_Color_Labels'] = sub_colours
        
    return umap_results




# Needs updating of default values -- DONE
def HDBSCAN_UMAP_Application(data,
                           n_healthy,
                           n_mod,
                           n_large,
                           dof_num,
                           n_components = 2, 
                           n_neighbors = 30, 
                           min_dist = 0, 
                           metric = 'manhattan', 
                           set_op_mix_ratio=0.95, 
                           plot_flag=False,
                           print_flag=False,
                           total_obs=2,
                           min_cluster_size=60,
                           remove_outliers=False,
                           remove_misspec=False):
    
    '''
    n_healthy, n_mod, and n_large are ONLY used to assist in plotting. The entire "data" is used in the 
    UMAP and HDBSCAN procedure without knowing the boundaries of healthy->mod->large dam transitions 
    (unlike in the "theoretical_clustering" function.)
    ''' 

    n_data = data.shape[0]

    for i in range(1,total_obs+1):
        sub_data = data[0:n_data*i//total_obs,:]

        # Note that UMAP is applied to entire observed data set ==> we aren't cheating by
        # knowing whether or not there is damage, and also how much types of damage there are etc.
        umap_obj = umap.UMAP(n_neighbors = n_neighbors, n_components = n_components, 
                             min_dist = min_dist,metric=metric,
                             set_op_mix_ratio = set_op_mix_ratio, random_state=42).fit(sub_data)

        data_points = umap_obj.transform(sub_data)


        clusterer = hdbscan.HDBSCAN(metric='euclidean', 
                                    prediction_data=True, 
                                    min_cluster_size = min_cluster_size).fit(data_points)

        if plot_flag:
            plt.figure()
            plt.title(f'DOF NUMBER: {dof_num+1}, OBSERVATION: {i}/{total_obs}')
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
                    if remove_misspec == True:
                        continue
                    plt.scatter(data_points[j,0],data_points[j,1],c='y',edgecolors='k',s=150,alpha=0.3,
                            label = 'Misspecified Point(s)' if Misspeficiation_flag else None)
                    Misspeficiation_flag = False       
                    
            plt.legend()
            leg = plt.legend()
            for lh in leg.legendHandles: 
                lh._sizes = [300]

            
        if print_flag:
            print(f'{i}/{total_obs}')
            
    # Final Clustering and Label Allocations
    return [hdbscan.all_points_membership_vectors(clusterer), clusterer.labels_]