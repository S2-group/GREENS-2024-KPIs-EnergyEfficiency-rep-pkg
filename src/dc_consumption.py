import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

## Load the dataframe with Actual Power Consumption of the Whole Cluster
df_power = pd.read_csv('../data/workingenvironment.csv')

# Calculate Total Power Consumption per Cluster
total_power_dc = df_power['Actual power kW'].sum()

# Assuming each row corresponds to a cluster, you can directly sum the 'Actual power kW' column for each cluster

# Convert Total Power Consumption to TW
total_power_dc = total_power_dc * 0.000001

# Calculate Data Center Energy Consumption for each cluster
time_in_hours_per_month = 30 * 24  # 30 days * 24 hours/day
# Convert Total Power Consumption to TW/h
total_power_dc = total_power_dc * time_in_hours_per_month

# Compare with World's Data Centers Energy Consumption Tw/h
world_data_centers_energy_consumption = 290   # Replace with the actual world's data centers energy consumption

# Visualization
categories = ['Your Data Center', 'World Data Centers']
values = [total_power_dc, world_data_centers_energy_consumption]

# Creating a single bar plot
plt.figure(figsize=(9, 4))  # Adjusted for a single plot
plt.bar(categories, values)
plt.yscale('log')  # Set y-axis to logarithmic scale
plt.ylabel('Power Consumption (TWh)')
plt.title('Comparison of Data Center Energy Consumption')

plt.show()
