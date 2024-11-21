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

##start with entering dates and making an integer to determine the distance between them

##load the p-values from out pickle file using with method
def load_pvalues(start_date, end_date, ensemble_name, variable_name, days_between, output_dir):


    # make empty space for our pvalues
    pvalues_list = []
    start_date = datetime(year = 2011, month=1, day=1)

    while current_date <= end_date:
        # Create date string
        date_str = current_date.strftime("%Y%m%d%H")
        
        # Define the pickle file path
        pickle_file = "{variable_name}_{ensemble_name}_{date_str}_pvalues.pkl"
        
        # Load the pickle file
        with open(pickle_file, 'rb') as f:
            p_results = pickle.load(f)
        
        # Extract p-values for the current date
        p_values = p_results['pvalues']
        pvalues_list.append(p_values)
        
        # Increment to the next date
        current_date += timedelta(days=1)
    
    # Convert the list of p-values into a 4D numpy array
    p_values_combined = np.array(pvalues_list)
    return p_values_combined


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



###### plots #######

# plotting the number of null hypothesis rejection across latitude, model level, and time

rejection_latitude = np.sum(significance, axis=(0, 2, 3))  # Sum across time, levels, and longitude
rejection_level = np.sum(significance, axis=(0, 1, 3))  # Sum across time, latitudes, and longitude
rejection_time = np.sum(significance, axis=(1, 2, 3))  # Sum across levels, latitudes, and longitude
    

##### lat 
plt.figure(figsize=(10, 6))
plt.plot(np.arange(latitudes), rejection_latitude, label='Rejections by Latitude', color='blue')
plt.xlabel('Latitude index')
plt.ylabel('Number of Null Hypothesis Rejections')
plt.title(f'Null Hypothesis Rejections by Latitude for {variable_name} ({ensemble_name})')
plt.grid(True)
plt.savefig("rejections_by_latitude.png")
plt.close()

### level
plt.figure(figsize=(10, 6))
plt.plot(np.arange(levels), rejection_level, label='Rejections by Level', color='green')
plt.xlabel('Model Level')
plt.ylabel('Number of Null Hypothesis Rejections')
plt.title(f'Null Hypothesis Rejections by Model Level for {variable_name} ({ensemble_name})')
plt.grid(True)
plt.savefig("rejections_by_level.png")
plt.close()


#### time 
plt.figure(figsize=(10, 6))
plt.plot(np.arange(significant_mask.shape[0]), rejection_time, label='Rejections by Time', color='red')
plt.xlabel('Time step')
plt.ylabel('Number of Null Hypothesis Rejections')
plt.title(f'Null Hypothesis Rejections by Time for {variable_name} ({ensemble_name})')
plt.grid(True)
plt.savefig("rejections_by_time.png")
plt.close()


#### plotting comparisons
rejection_reference = np.sum(reference_mask, axis=(0, 1, 2))  # Sum over time, levels, and latitudes
rejection_perturbed = np.sum(perturbed_mask, axis=(0, 1, 2))  # Sum over time, levels, and latitudes


    # plotting the comparison
plt.figure(figsize=(10, 6))
plt.plot(np.arange(len(rejection_reference)), rejection_reference, label='Reference Ensemble', color='blue')
plt.plot(np.arange(len(rejection_perturbed)), rejection_perturbed, label='Perturbed Ensemble', color='orange')
plt.xlabel('Time Step')
plt.ylabel('Number of Null Hypothesis Rejections')
plt.title('Comparison of Null Hypothesis Rejections for {name} (Reference vs. Perturbed Ensemble)')
plt.legend()
plt.grid(True)
plt.savefig("comparison_rejections.png")
plt.close()



##the end