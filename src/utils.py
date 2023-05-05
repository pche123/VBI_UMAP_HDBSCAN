import scipy.io
from .processing import fft_feature_engineering
import numpy as np

# https://stackoverflow.com/questions/11955000/how-to-preserve-matlab-struct-when-accessing-in-python
def _check_keys( dict):
    """
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    """
    for key in dict:
        if isinstance(dict[key], scipy.io.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict


def _todict(matobj):
    """
    A recursive function which constructs from matobjects nested dictionaries
    """
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, scipy.io.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict


def loadmat(filename):
    """
    this function should be called instead of direct scipy.io .loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    """
    data = scipy.io.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)


def mkdir_p(mypath):
    '''Creates a directory. equivalent to using mkdir -p on the command line
    Taken from:
    https://stackoverflow.com/questions/11373610/save-matplotlib-file-to-a-directory
    '''

    from errno import EEXIST
    from os import makedirs,path

    try:
        makedirs(mypath)
    except OSError as exc: # Python >2.5
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else: raise


def read_data_fft(Bridge_Type, Damage_Location, Vehicle_Type, Bridge_Profile, 
                  Damage_Levels = ['DM00', 'DM20', 'DM40'], 
                  NUM_DATA_IN_DIR = 400 , 
                  DATA_ROOT_LOC = 'data/', 
                  NFFT=2**7):

    
    if Vehicle_Type == 'V1':
        DOF = 2
    elif Vehicle_Type == 'V2':
        DOF = 4
    else:
        DOF = 8
        
    # List of Dicts 
    # len(list) = num DOFs
    # Each element in list (dict) is the data for one damage level
    data_dict_DOFS = []
    for _ in range(DOF):
        data_dict_DOFS.append({})
    
    for i in range(len(Damage_Levels)):
        str_root_location = Bridge_Type + '/' + Damage_Location + '/' + Damage_Levels[i] + '/' + Vehicle_Type + '/' + Bridge_Profile + '/'
        str_root_event_file = Bridge_Type + Damage_Location + Damage_Levels[i] + Vehicle_Type + Bridge_Profile + 'E'
        
        # List of Lists
        # len(list) = num DOFs
        # Each element in list (another list) stores the data for one damage level
        # This gets reset per damage level (the history of features per damage level)
        # Is designed to be stored in the outer dictionary
        event_list_DOFS = []
        for _ in range(DOF):
            event_list_DOFS.append([])
        
        # For each event
        for j in range(1,NUM_DATA_IN_DIR+1): 
            data_str = DATA_ROOT_LOC + str_root_location + str_root_event_file + f'{j:04d}' + '.mat'
            data_read = loadmat(data_str)
            
            start_pos = data_read['Event']['Veh']['Pos']['t0_ind_beam']
            end_pos = data_read['Event']['Veh']['Pos']['t_end_ind_beam']
            data_matrix = data_read['Event']['Sol']['Veh']['A'][:,start_pos:end_pos] # important to keep start:end range
                        
            features = fft_feature_engineering(data_matrix, nfft=NFFT)
            # Keep accumulating the features, across event, for each observed DOF, at a specific damage level
            for dof_num in range(DOF):
                event_list_DOFS[dof_num] += [features[dof_num,:]]

            
            if j%50 == 0: print(f'Processed Event {j} from damage level {Damage_Levels[i]}')
            
        for dof_num in range(DOF):
            data_dict_DOFS[dof_num][Damage_Levels[i]] = np.array(event_list_DOFS[dof_num] )
        
        print()
        
    print( f'Finished processing information from:\n'
           f'Bridge - {Bridge_Type}\n'
           f'Location - {Damage_Location}\n' 
           f'Vehcile Type - {Vehicle_Type}\n'
           f'Road Profile - {Bridge_Profile}!\n\n')
    
    return data_dict_DOFS