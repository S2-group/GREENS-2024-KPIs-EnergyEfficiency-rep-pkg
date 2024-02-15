import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

## Load the dataframe with Actual Power Consumption of the Whole Cluster
df_power = pd.read_csv('workingenvironment.csv')

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
fig, axes = plt.subplots(1, 2, figsize=(18, 8))

# Bar Plot
axes[0].bar(['Your Data Center', 'World Data Centers'], [total_power_dc, world_data_centers_energy_consumption])
axes[0].set_yscale('log')  # Set y-axis to logarithmic scale
axes[0].set_ylabel('Power Consumption (TWh)')
axes[0].set_title('Comparison of Data Center Energy Consumption')

# Pie Chart
labels = ['Your Data Center', 'World Data Centers 2022']
sizes = [total_power_dc, world_data_centers_energy_consumption - total_power_dc]

# Plot pie chart
axes[1].pie(sizes, labels=labels, autopct='%1.5f%%', startangle=90)
axes[1].set_title('Comparison of Data Center Energy Consumption')

plt.show()
