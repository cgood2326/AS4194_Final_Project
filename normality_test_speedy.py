# Task #1
# Cole Good & Max Abrecht
# Import Packages
import sys
import numpy as np
import netCDF4 as nc
import scipy.stats
import pickle
from datetime import datetime, timedelta

def calculate_p_values(file_path, variable_name):
    '''
    A function to load ensemble data and calculate the p value of the Shapiro-Wilk Test for each grid point.

    Inputs:
    -------
    file_path : string
        Path to NetCDF file.
    variable_name : string
        Name of the of the varible to be analyzed.
    
    Returns:
    --------
    p_values: array
        A 3D array of p-values.
    '''
    # Open the SPEEDY File.
    with nc.Dataset(file_path, mode='r') as dataset:
        # Pull data for specified variable.
        variable_data=dataset.variables[variable_name][:]

        # Code to squeeze out single value dimensions
        variable_data=np.squeeze(variable_data)

        # Code to create arrays to hold p-values.
        # If statement to create arrays coresponding to the different dimensions. (ie. 'u' and 'v' are 5D whereas 'ps' is 4D)
        if variable_data.ndim ==4:
            p_values = np.empty(variable_data.shape[1:])  
            levels, latitudes, longitudes = variable_data.shape[1:]
        elif variable_data.ndim == 3:  # Variables like 'ps'
            p_values = np.empty(variable_data.shape[1:])  
            levels, latitudes, longitudes = None, variable_data.shape[1], variable_data.shape[2]
    
        # Code for nested for loops to run the SW test and if statement to account for 5D vs 4D.
        if levels:  # For 5D variables.
            for lev in range(levels):
                for lat in range(latitudes):
                    for lon in range(longitudes):
                        # Code to extract ensemble values for the current grid point.
                        ensemble_values = variable_data[:, lev, lat, lon]
                        # Code to perform Shapiro-Wilk test and store the p-value.
                        p_values[lev, lat, lon] = scipy.stats.shapiro(ensemble_values)[1]
        else:  # For 4D variables. 
            for lat in range(latitudes):
                for lon in range(longitudes):
                    # Code to extract ensemble values for the current grid point.
                    ensemble_values = variable_data[:, lat, lon]
                    # Code to perform Shapiro-Wilk test and store the p-value.
                    p_values[lat, lon] = scipy.stats.shapiro(ensemble_values)[1]
    
    return p_values

def save_results(output_dir, variable_name, ensemble_name, date_str, p_values, sigma_levels):
    '''
    A Function to save the p-value data in a new pickle file.

    Inputs:
    -------
    output_dir : string
        Directory to save the pickle file to.
    variable_name : string
        Name of variable.
    ensemble_name : string
        Name of the ensemble, either reference or perturbed.
    p_values : array
        A 3D array of p-values.
    sigma_levels : array
        A 1D array of sigma levels.

    Results:
    --------
    A pickle file of the p-values. 
    '''

    # Code to create the pickle file name.
    output_file=output_dir+'/'+variable_name+'_'+ensemble_name+'_'+date_str+'_pvalues.pkl'

    # Code to create the dictionary to be stored in the pickle file.
    p_results={'date':date_str,'vname':variable_name,'pvalues':p_values,'theoretical pressure':sigma_levels*1000}

    # Code to save dictionary as a pickle file.
    f=open(output_file,'wb')
    pickle.dump(p_results,f)
    f.close()

# Code for command line arguments
days_since=int(sys.argv[1])
ensemble_name=sys.argv[2]
variable_name=sys.argv[3]
output_dir=sys.argv[4]

# Code for the base SPEEDY directory.
base_SPEEDY='/fs/ess/PAS2856/SPEEDY_ensemble_data'

# Code for date string
start_date = datetime(2011, 1, 1)  
current_date = start_date + timedelta(days=days_since)
date_str = current_date.strftime("%Y%m%d%H") 

# Code for the file path.
file_path=base_SPEEDY+'/'+ensemble_name+'/'+date_str+'00.nc'

# Code to pull in sigma levels.
f=nc.Dataset(file_path,'r')
sigma_levels=np.array(f.variables['lev'][:])
f.close()

# Code to call function to calculate the p-values.
p_values=calculate_p_values(file_path,variable_name)

# Code to call function to save results.
save_results(output_dir,variable_name,ensemble_name,date_str,p_values, sigma_levels)