# Task #2
# Cole Good & Max Abrecht
import sys
import numpy as np
import netCDF4 as nc
import scipy.stats
import pickle
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


##open levels from nc file to use for the levels and lats
def open_file_for_date(ensemble_name, date_str):
    base_SPEEDY = '/fs/ess/PAS2856/SPEEDY_ensemble_data' 
    file_path = f"{base_SPEEDY}/{ensemble_name}/{date_str}00.nc"
    f = nc.Dataset(file_path, 'r') 
    
    ## putting levels and lats into arrrays
    levels = np.array(f.variables['lev'][:])  
    latitudes = np.array(f.variables['lat'][:])  
    
    f.close()
    return levels, latitudes


## function correction applys the specified method to our list of p values
def correction(p_values_combined):

    # faltten values
    new_p_values = p_values_combined.flatten()
    corrected_pvalues = scipy.stats.false_discovery_control(new_p_values, method = 'by')

    ## reshape corrected pvalues back into the 4d array
    corrected_pvalues_reshaped = corrected_pvalues.reshape(p_values_combined.shape)
   ##testing
    print (corrected_pvalues_reshaped.shape)
    
    # our <.05 p values
    significance = corrected_pvalues_reshaped > .05

    print(significance.shape)

    return significance


##attempting to pull the array of levels and lats from the pickle file
def extract_lat_level_data(ensemble_name, start_date, end_date):

    ##initialize empty list
    latitudes_list = []
    levels_list = []
    pvalues_list = []

    ##making end date a datetime so it can be used in <=
    end_date = datetime.strptime(end_date, "%Y%m%d%H")
    start_date = datetime.strptime(start_date, "%Y%m%d%H")
    current_date = start_date

    ##defining these outside the while loop because the levels and lats are constants 
    date_str = current_date.strftime("%Y%m%d%H")
    levels, latitudes = open_file_for_date(ensemble_name, date_str)
    levels_list.append(levels)
    latitudes_list.append(latitudes)

    while current_date <= end_date:
        date_str = current_date.strftime("%Y%m%d%H")
        
        # Load the pickle file
        pickle_file = f"/fs/scratch/PAS2856/AS4194_Project/GoodAlbrecht/{variable_name}_{ensemble_name}_{date_str}_pvalues.pkl"
        with open(pickle_file, 'rb') as f:
            p_results = pickle.load(f)
        
        # Extract p-values
        p_values = p_results['pvalues']
        pvalues_list.append(p_values)
        
        # Increment the date
        current_date += timedelta(days=1)
    
    # Combine all data into numpy arrays
    p_values_combined = np.array(pvalues_list)
    levels_combined = np.array(levels_list)
    latitudes_combined = np.array(latitudes_list)
    return p_values_combined, levels_combined, latitudes_combined

###### plots #######
# plotting the number of null hypothesis rejection across latitude, model level, and time

def plot_rejections_by_latitude(latitudes, rejection_latitude, time_steps, ensemble_name, variable_name):
    
    # Plot the contour: time_steps vs latitudes vs rejection values
    cnf = plt.contourf(time_steps, latitudes, rejection_latitude, cmap='inferno', extend='both')
    plt.colorbar(cnf, label='Number of Null Hypothesis Rejections')
    plt.xlabel('Time Steps')
    plt.ylabel('Latitude')
    plt.title(f'Null Hypothesis Rejections by Latitude for {variable_name} ({ensemble_name})')
    plt.grid(True)
    plt.savefig(f'Null_Hypothesis_Rejections_by_Latitude_{variable_name}_{ensemble_name}.png')
    plt.close()


def plot_rejections_by_level(levels, rejection_level, ensemble_name, variable_name):

    print(f"Shape of rejection_level: {rejection_level.shape}")

    plt.figure(figsize=(10, 6))
    cnf = plt.contourf(np.arange(rejection_level.shape[1]), levels, rejection_level, cmap='inferno', extend='both')
    plt.colorbar(cnf, label='Number of Null Hypothesis Rejections')  
    plt.xlabel('Time Steps')
    plt.ylabel('Model Levels')
    plt.title(f'Null Hypothesis Rejections by Model Level for {variable_name} ({ensemble_name})')
    plt.grid(True)
    plt.savefig(f'Null_Hypothesis_Rejections_by_Level_{variable_name}_{ensemble_name}.png')
    plt.close()

def plot_rejections_by_time(time_steps, rejection_time, ensemble_name, variable_name):


    print(f"Shape of time_steps: {len(time_steps)}")
    print(f"Shape of rejection_time: {rejection_time.shape}")

    plt.figure(figsize=(10, 6))
    cnf = plt.contourf(time_steps, np.arange(rejection_time.shape[1]), rejection_time, cmap='inferno', extend='both')
    plt.colorbar(cnf, label='Number of Null Hypothesis Rejections') 
    plt.xlabel('Time Steps')
    plt.ylabel('Latitude/Model Levels')
    plt.title(f'Null Hypothesis Rejections by Time for {variable_name} ({ensemble_name})')
    plt.grid(True)
    plt.savefig(f'Null_Hypothesis_Rejections_by_Time_{variable_name}_{ensemble_name}.png')
    plt.close()

## use sys.argv tp get command line arguments
ensemble_name = sys.argv[1] 
end_date = sys.argv[2]  
variable_name = sys.argv[3]
start_date = sys.argv[4]


## extract data
p_values_combined, levels_combined, latitudes_combined = extract_lat_level_data(ensemble_name, start_date, end_date)

## perform correction
significance = correction(p_values_combined)

## reverting start date bact to string to be compatible with timedelta
start_date = datetime.strptime(start_date, "%Y%m%d%H")

## using out significance, i create the variable time steps for how many times (days) to get data
time_steps = [start_date + timedelta(days=i) for i in range(len(significance))]


## plot the results (looks very pretty with our functions)
rejection_latitude = np.mean(significance, axis=(0, 1))  ##over levels and time
plot_rejections_by_latitude(latitudes_combined[0], rejection_latitude, time_steps, ensemble_name, variable_name)

rejection_level = np.mean(significance, axis=(0, 2))  ## over latitudes and time
plot_rejections_by_level(np.arange(8), rejection_level, ensemble_name, variable_name)

rejection_time = np.mean(significance, axis=(1, 2))  ## over latitudes and levels
plot_rejections_by_time(time_steps, rejection_time, ensemble_name, variable_name)