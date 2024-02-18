import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataframe with Actual Power Consumption of the Whole Cluster
df_power = pd.read_csv('../data/workingenvironment.csv')

# Load the dataframe with the information about nodes and clusters
df_nodes = pd.read_excel('../data/data.xlsx', sheet_name='Current Capacity and Efficiency')
# Convert both 'Cluster Name' columns to lowercase for case-insensitive merge

df_power['Cluster Name'] = df_power['Cluster Name'].str.lower()
df_nodes['Cluster Name'] = df_nodes['Cluster Name'].str.lower()
# ########################################################################## past and forcast data
# Step 1: Read historical data
historical_data = pd.read_excel('../data/data.xlsx', sheet_name='Past and Forecast Data')

# Step 2: Filter data for years 2022 and 2023
historical_data['Year'] = historical_data['Month'].str.split('-').str[1].astype(int)
historical_data['Cluster Name']= historical_data['Cluster Name'].str.lower()
filtered_historical_data = historical_data[historical_data['Year'].isin([22, 23])]

# Step 3: Calculate median Used Capacity Percentage for each node
median_capacity = filtered_historical_data.groupby('Host Name')['Used Capacity (TiB)'].median().reset_index()

median_capacity['Cluster Name']=historical_data['Cluster Name'].str.lower()


# Merge the dataframes on the 'Cluster Name'
merged_df = pd.merge(df_power, df_nodes, on='Cluster Name')


# Calculate Power Consumption per Node
merged_df['Power Consumption per Node'] = merged_df['Actual power kW'] / merged_df.groupby('Cluster Name')['Host Name'].transform('size')
merged_df['Power Consumption per Used TB per Node'] = (merged_df['Power Consumption per Node'] / (merged_df['Used Capacity (TiB)']))*(1.099511627776)
merged_df['Power Consumption per Usable TB per Node'] = (merged_df['Power Consumption per Node'] / (merged_df['Total Usable Capacity (TiB)']))*(1.099511627776)
merged_median= pd.merge(merged_df, median_capacity, on='Host Name')

merged_df['Power Capacity'] = (merged_df['Used Capacity (TiB)'] * 1024/merged_df['Power Consumption per Node']*1000)
merged_median['Median Power Capacity'] = (merged_median['Used Capacity (TiB)_y'] * 1024/merged_median['Power Consumption per Node']*1000)
merged_df['DCeP'] = (merged_df['Used Capacity Percentage']/merged_df['Power Consumption per Node'])

merged_median['Power Consumption per Median Used TB per Node'] = (merged_median['Power Consumption per Node'] / (merged_median['Used Capacity (TiB)_y']))*(1.099511627776)
# ##########################################################################

# Descriptive analysis
# Per Model Consumption
#  Power Per Node
plt.figure(figsize=(20, 6))
sns.barplot(x='Host Name', y='Power Consumption per Node', hue='Model',data=merged_df)
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.xlabel('Node Name')
plt.ylabel('Typical Power Consumption (kW) per Node')
plt.title('Typical Power Consumption (kW) for Each Node')
plt.tight_layout()
plt.show()
# # # #########################################################################
# #  Power Per Node  Box Plot
plt.figure(figsize=(14, 6))
sns.boxplot(x='Model', y='Power Consumption per Node', data=merged_df)
plt.xlabel('Node Model')
plt.ylabel('Typical Power Consumption (kW) per Node')
plt.title('Typical Power Consumption (kW) per Node by Model')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.tight_layout()
plt.show()
# ########################################################################
# # # # power consumption per usable TB  of data diagram

plt.figure(figsize=(20, 4))
sns.barplot(x='Host Name', y='Power Consumption per Usable TB per Node', hue='Model',data=merged_df)
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.xlabel('Node Name')
plt.ylabel('Power Consumption (kW) per Usable TB per Node')
plt.title('Power Consumption (kW) per Usable TB for Each Node  - Oct 2023')

plt.tight_layout()
plt.show()
# ########################################################################
# Capacity per Watt Ratio
plt.figure(figsize=(12, 6))

# Bar plot for power consumption
sns.barplot(x='Host Name', y='Power Capacity', hue='Model', data=merged_df)
plt.xticks(rotation=45, ha='right')
plt.xlabel('Node Name')
plt.ylabel('Capacity per Watt per Node (GB/Watt)')
plt.title('Capacity per Watt per Node (GB/Watt)')
plt.tight_layout()
plt.show()
# #########################################################################

# histogram for identifying power consumption patterns within different models

plt.figure(figsize=(12, 8))
sns.histplot(merged_df['Power Consumption per Node'], kde=False, bins=20)
plt.xlabel('Power Consumption per Node')
plt.ylabel('Frequency')
plt.title('Distribution of Power Consumption per Node')
plt.show()
##########################################################################

# Scatter plot  for capacity utilisation (%) and power consumption
unique_models = merged_df['Model'].unique()

# Create a scatter plot for each model
for model in unique_models:
    model_data = merged_df[merged_df['Model'] == model]
    plt.scatter(x='Used Capacity Percentage', y='Power Consumption per Node', data=model_data, label=model)

# Add labels and title
plt.xlabel('Used Capacity Percentage')
plt.ylabel('Power Consumption per Node')
plt.title('Relation between Used Capacity (%) and Power Consumption by Model')

# Add legend
plt.legend()

# Show the plot
plt.show()
# # #########################################################################
# Scatter plot for capacity utilisation (TiB)  and power consumption
unique_models = merged_df['Model'].unique()

# Create a scatter plot for each model
for model in unique_models:
    model_data = merged_df[merged_df['Model'] == model]
    plt.scatter(x='Used Capacity (TiB)', y='Power Consumption per Node', data=model_data, label=model)

# Add labels and title
plt.xlabel('Used Capacity (TiB)')
plt.ylabel('Power Consumption per Node')
plt.title('Relation between Used Capacity (TiB) and Power Consumption by Model')

# Add legend
plt.legend()

# Show the plot
plt.show()


##########################################################################
# Relation between Space Saved and Power Consumption per Node
power_technique =merged_df
space_saving_cols = ['Space Saved by Snapshots (TiB)', 'Space Saved by Clones (TiB)',
                     'Space Saved by Volume Deduplication (TiB)', 'Space Saved by Volume Compression (TiB)',
                     'Space Saved by Compaction, Aggr Deduplication and Compression (TiB)']
power_technique['Sum_Space_Saved_Node'] = merged_df[space_saving_cols].sum(axis=1)
power_technique['Power Consumption per Node'] = merged_df['Power Consumption per Node']
power_technique['Model'] = merged_df['Model']
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Sum_Space_Saved_Node' , y='Power Consumption per Node' ,data=power_technique,hue='Model', s=100)
plt.xlabel('Sum of Space Saved by Techniques')
plt.ylabel('Power Consumption per Node')
plt.title('Relation between Space Saved and Power Consumption per Node')
plt.show()
