# Task #2
# Cole Good & Max Abrecht
import sys
import numpy as np
import netCDF4 as nc
import scipy.stats
import pickle
from datetime import datetime, timedelta
import matplotlib.pyplot as plt



## use this for the adjustment of p values
#    scipy.stats.false_discovery_control


##open levels from nc file to use for the levels and lats
def open_file_for_date(ensemble_name, date_str):
    base_SPEEDY='/fs/ess/PAS2856/SPEEDY_ensemble_data'
    file_path = f"{base_SPEEDY}/{ensemble_name}/{date_str}00.nc"

    f = nc.Dataset(file_path, 'r')  # This will raise an error if the file does not exist
    levels = np.array(f.variables['lev'][:])  # Extract sigma levels
    f.close()
    return levels



##load the p-values from out pickle file using with method
def load_pvalues(start_date, end_date, ensemble_name, variable_name, days_between, output_dir):


    # make empty space for our pvalues
    pvalues_list = []
    start_date = datetime(2011,1,1)
    end_date = datetime(2011,1,6)

    while current_date <= end_date:
        # Create date string
        date_str = current_date.strftime("%Y%m%d%H")
        
        # Define the pickle file path
        pickle_file = "/fs/scratch/PAS2856/AS4194_Project/GoodAlbrecht"
        
        # Load the pickle file
        with open(pickle_file, 'rb') as f:
            p_results = pickle.load(f)
        
        # Extract p-values for the current date
        p_values = p_results['pvalues']
        pvalues_list.append(p_values)
        
        # Increment to the next date
        current_date = 0
        current_date += timedelta(days=1)
    
    # Convert the list of p-values into a 4D numpy array
    p_values_combined = np.array(pvalues_list)
    return p_values_combined




file_path = 't_reference_ens_2011122400_pvalues.pkl'
with open(file_path, 'rb') as file:
    data = pickle.load(file)

print(data)

def correction(p_values_combined):

    # faltten values
    new_p_values = p_values_combined.flatten()
    corrected_pvalues = scipy.stats.false_discovery_control(new_p_values, method = 'by')

    ## reshape corrected pvalues back into the 4d array
    corrected_pvalues_reshaped = corrected_pvalues.reshape(p_values_combined.shape)
    print (corrected_pvalues_reshaped.shape)
    
    # our <.05 p values
    significance = corrected_pvalues < .05

    
    return significance


days_since=int(sys.argv[1])
ensemble_name=sys.argv[2]
variable_name=sys.argv[3]
output_dir=sys.argv[4]

significance = correction(load_pvalues())

###### plots #######
# plotting the number of null hypothesis rejection across latitude, model level, and time

rejection_latitude = np.sum(significance, axis=(0, 2, 3))  # Sum across time, levels, and longitude
rejection_level = np.sum(significance, axis=(0, 1, 3))  # Sum across time, latitudes, and longitude
rejection_time = np.sum(significance, axis=(1, 2, 3))  # Sum across levels, latitudes, and longitude


def plot_rejections_by_latitude(latitudes, rejection_latitude, ensemble_name, variable_name):
    plt.figure(figsize=(10, 6))
    plt.plot(np.arange(latitudes), rejection_latitude, label='Rejections by Latitude', color='blue')
    plt.xlabel('Latitude index')
    plt.ylabel('Number of Null Hypothesis Rejections')
    plt.title(f'Null Hypothesis Rejections by Latitude for {variable_name} ({ensemble_name})')
    plt.grid(True)
    plt.savefig("rejections_by_latitude.png")
    plt.close()

def plot_rejections_by_level(levels, rejection_level, ensemble_name, variable_name):
    plt.figure(figsize=(10, 6))
    plt.plot(np.arange(levels), rejection_level, label='Rejections by Level', color='green')
    plt.xlabel('Model Level')
    plt.ylabel('Number of Null Hypothesis Rejections')
    plt.title(f'Null Hypothesis Rejections by Model Level for {variable_name} ({ensemble_name})')
    plt.grid(True)
    plt.savefig("rejections_by_level.png")
    plt.close()


def plot_rejections_by_time(time_steps, rejection_time, ensemble_name, variable_name):
    plt.figure(figsize=(10, 6))
    plt.plot(np.arange(significant_mask.shape[0]), rejection_time, label='Rejections by Time', color='red')
    plt.xlabel('Time step')
    plt.ylabel('Number of Null Hypothesis Rejections')
    plt.title(f'Null Hypothesis Rejections by Time for {variable_name} ({ensemble_name})')
    plt.grid(True)
    plt.savefig("rejections_by_time.png")
    plt.close()


def plot_comparison(reference_rejections, perturbed_rejections):
    plt.figure(figsize=(10, 6))
    plt.plot(np.arange(len(reference_rejections)), reference_rejections, label='Reference Ensemble', color='blue')
    plt.plot(np.arange(len(perturbed_rejections)), perturbed_rejections, label='Perturbed Ensemble', color='orange')
    plt.xlabel('Time Step')
    plt.ylabel('Number of Null Hypothesis Rejections')
    plt.legend()
    plt.grid(True)
    plt.savefig("comparison_rejections.png")
    plt.close()




#make function to pull lat and levels from coles path

#make function to extract data from pickle files for set number of days (nested for loops)

##the end