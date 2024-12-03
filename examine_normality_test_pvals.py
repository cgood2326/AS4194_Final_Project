# Task #2
# Cole Good & Max Abrecht
import sys
import numpy as np
import netCDF4 as nc
import scipy.stats
import pickle
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


# load a pickle file containing p-values for a specific ensemble, 
# 'theoretical pressure' values are extracted as a numpy array
pickle_file = f"/fs/scratch/PAS2856/AS4194_Project/GoodAlbrecht/t_reference_ens_2011010100_pvalues.pkl"
with open(pickle_file, 'rb') as f:
    p_results = pickle.load(f)
    pressure = np.array(p_results['theoretical pressure'][:])  # extract theoretical pressure values

## function to open netcdf file for a specific date, extracting pressure levels and latitudes
def open_file_for_date(ensemble_name, date_str):
    base_SPEEDY = '/fs/ess/PAS2856/SPEEDY_ensemble_data'  # base directory for speedy data
    file_path = f"{base_SPEEDY}/{ensemble_name}/{date_str}00.nc"  # construct file path using date
    f = nc.Dataset(file_path, 'r')  # open the netcdf file for reading
    
    # extract pressure levels and latitudes from the file
    levels = np.array(f.variables['lev'][:])  
    latitudes = np.array(f.variables['lat'][:])  
    
    f.close()  # close the netcdf file
    return levels, latitudes  # return extracted data

## function to apply false discovery correction on the p-values
def correction(p_values_combined):
    # flatten the 4d array of p-values
    new_p_values = p_values_combined.flatten()
    
    # apply the benjamini-hochberg correction method to control false discovery rate
    corrected_pvalues = scipy.stats.false_discovery_control(new_p_values, method = 'by')

    # reshape corrected p-values back into the original 4d shape
    corrected_pvalues_reshaped = corrected_pvalues.reshape(p_values_combined.shape)
    
    # print the shape for debugging
    print(corrected_pvalues_reshaped.shape)
    
    # identify where p-values are above the threshold of 0.05 (i.e., not significant)
    significance = corrected_pvalues_reshaped > .05

    return significance  # return the binary significance array

## function to extract latitude, level, and p-value data for a given date range
def extract_lat_level_data(ensemble_name, start_date, end_date):
    ## initialize empty lists to hold data
    latitudes_list = []
    levels_list = []
    pvalues_list = []

    ## convert string dates to datetime objects for easy comparison
    end_date = datetime.strptime(end_date, "%Y%m%d%H")
    start_date = datetime.strptime(start_date, "%Y%m%d%H")
    current_date = start_date  # start from the provided start date

    ## load the first date's data for levels and latitudes (constants across time)
    date_str = current_date.strftime("%Y%m%d%H")
    levels, latitudes = open_file_for_date(ensemble_name, date_str)
    levels_list.append(levels)
    latitudes_list.append(latitudes)

    ## iterate through each day in the date range
    while current_date <= end_date:
        date_str = current_date.strftime("%Y%m%d%H")
        
        # load the pickle file for the current date
        pickle_file = f"/fs/scratch/PAS2856/AS4194_Project/GoodAlbrecht/{variable_name}_{ensemble_name}_{date_str}_pvalues.pkl"
        with open(pickle_file, 'rb') as f:
            p_results = pickle.load(f)
        
        # extract p-values for the current date
        p_values = p_results['pvalues']
        pvalues_list.append(p_values)
        
        # increment the date by 1 day
        current_date += timedelta(days=1)
    
    # combine the extracted data into numpy arrays
    p_values_combined = np.array(pvalues_list)
    levels_combined = np.array(levels_list)
    latitudes_combined = np.array(latitudes_list)
    return p_values_combined, levels_combined, latitudes_combined  # return combined data

###### plotting functions #######

# plot the number of null hypothesis rejections across latitudes and time steps
def plot_rejections_by_latitude(latitudes, rejection_latitude, time_steps, ensemble_name, variable_name):
    # create contour plot: time_steps vs latitudes vs rejection values
    cnf = plt.contourf(time_steps, latitudes, rejection_latitude.T, cmap='inferno', extend='both')
    plt.colorbar(cnf, label='Number of Null Hypothesis Rejections')  # add color bar
    plt.title(f"Rejection by Latitude: {ensemble_name} - {variable_name}")  # title
    plt.xlabel("Time Steps")  # x-axis label
    plt.ylabel("Latitudes")  # y-axis label
    plt.savefig(f'null_hypothesis_rejections_by_latitiude_{variable_name}_{ensemble_name}.png')  # save the plot
    plt.show()  # display the plot

# plot the number of null hypothesis rejections across model levels and time steps
def plot_rejections_by_level(pressure, rejection_level, ensemble_name, variable_name):
    plt.figure(figsize=(10, 6))  # set figure size
    cnf = plt.contourf(np.arange(rejection_level.shape[0]), pressure, rejection_level.T, cmap='inferno', extend='both')
    plt.colorbar(cnf, label='Number of Null Hypothesis Rejections')  # add color bar with label
    plt.ylim((950,20))  # set y-axis limits for pressure (from 950 to 20 hPa)
    plt.xlabel('Time Steps')  # x-axis label
    plt.ylabel('Theoretical Pressure (HPa)')  # y-axis label
    plt.title(f'Null Hypothesis Rejections by Model Level for {variable_name} ({ensemble_name})')  # title
    plt.grid(True)  # add grid lines
    plt.savefig(f'null_hypothesis_rejections_by_level_{variable_name}_{ensemble_name}.png')  # save the plot
    plt.close()  # close the plot

# plot the number of null hypothesis rejections across time steps
def plot_rejections_by_time(time_steps, rejection_time, ensemble_name, variable_name):
    print(rejection_time.shape)  # print shape for debugging
    print(time_steps.shape)  # print shape for debugging

    plt.figure(figsize=(10, 6))  # set figure size
    cnf = plt.contourf(time_steps, np.arange(rejection_time.shape[1]), rejection_time.T, cmap='inferno', extend='both')
    plt.colorbar(cnf, label='Number of Null Hypothesis Rejections')  # add color bar with label
    plt.xlabel('Time Steps')  # x-axis label
    plt.ylabel('Latitude/Model Levels')  # y-axis label
    plt.title(f'Null Hypothesis Rejections by Time for {variable_name} ({ensemble_name})')  # title
    plt.grid(True)  # add grid lines
    plt.savefig(f'null_hypothesis_rejections_by_time_{variable_name}_{ensemble_name}.png')  # save the plot
    plt.close()  # close the plot

## use sys.argv to get command line arguments
ensemble_name = sys.argv[1]  # ensemble name
end_date = sys.argv[2]  # end date
variable_name = sys.argv[3]  # variable name
start_date = sys.argv[4]  # start date

# extract p-values, levels, and latitudes from the specified date range
p_values_combined, levels_combined, latitudes_combined = extract_lat_level_data(ensemble_name, start_date, end_date)
# apply the correction to the p-values
significance = correction(p_values_combined)

# convert start_date to datetime object before creating time_steps
start_date = datetime.strptime(start_date, "%Y%m%d%H")

# creating time steps (days incremented by 1)
time_steps = [start_date + timedelta(days=i) for i in range(len(significance))]
time_steps = np.array(time_steps)

# calculate rejections by latitude, level, and time
rejection_latitude = np.mean(significance, axis=(1, 3))  # average over levels and grid points (axis 2 and 3)
plot_rejections_by_latitude(latitudes_combined[0], rejection_latitude, time_steps, ensemble_name, variable_name)

rejection_level = np.mean(significance, axis=(2, 3))  ## average over latitudes and grid points
plot_rejections_by_level(pressure, rejection_level, ensemble_name, variable_name)

rejection_time = np.mean(significance, axis=(1, 2))  ## average over latitudes, levels, and grid points
plot_rejections_by_time(time_steps, rejection_time, ensemble_name, variable_name)