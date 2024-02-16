import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.lines as mlines
# Load your CSV data
result_df = []
df = pd.read_excel('./data/data.xlsx', sheet_name='Current Capacity and Efficiency')

#####################################################################

# Sum space-saving columns for each node
space_saving_cols = ['Space Saved by Snapshots (TiB)', 'Space Saved by Clones (TiB)',
                     'Space Saved by Volume Deduplication (TiB)', 'Space Saved by Volume Compression (TiB)',
                     'Space Saved by Compaction, Aggr Deduplication and Compression (TiB)']

df['Sum_Space_Saved_Node'] = df[space_saving_cols].sum(axis=1)

# Sum space-saving columns for each cluster

df['Sum_Space_Saved_Cluster'] = df.groupby('Cluster Name')['Sum_Space_Saved_Node'].transform('sum')
df['Used_Capacity_Cluster'] = df.groupby('Cluster Name')['Used Capacity (TiB)'].transform('sum')
df['Used_Capacity_Ratio'] = (df['Used_Capacity_Cluster'] / (df['Used_Capacity_Cluster'] + df['Sum_Space_Saved_Cluster']))*(1.099511627776)


######################################################################### Melt the dataframe to have a 'Technique' column
melted_df = pd.melt(df, id_vars=['Cluster Name','Model'],value_vars=space_saving_cols, var_name='Technique', value_name='Space Saved')

sum_space_saved = melted_df.groupby(['Cluster Name', 'Technique'])['Space Saved'].sum().reset_index()

# Set seaborn style
sns.set(style="whitegrid")

########################################################################################################
# Create subplots with 1 row and 2 columns
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Plot 1: Box Plot for Space Saved by Technique (excluding 'Space Saved by Snapshots (TiB)')
filtered_df = sum_space_saved[sum_space_saved['Technique'] != 'Space Saved by Snapshots (TiB)']
# Rename specific values in the 'Technique' column
filtered_df['Technique'] = filtered_df['Technique'].replace({'Space Saved by Clones (TiB)': 'T1'})
filtered_df['Technique'] = filtered_df['Technique'].replace({'Space Saved by Compaction, Aggr Deduplication and Compression (TiB)': 'T2'})
filtered_df['Technique'] = filtered_df['Technique'].replace({'Space Saved by Volume Compression (TiB)': 'T3'})
filtered_df['Technique'] = filtered_df['Technique'].replace({'Space Saved by Volume Deduplication (TiB)': 'T4'})
# filtered_df = filtered_df[filtered_df['Technique'] == 'Space Saved by Clones (TiB)']
# print('helllooooooo:')
# print(axes[0])
sns.boxplot(x='Technique', y='Space Saved', data=filtered_df, ax=axes[0],color='steelblue') 

axes[0].set_title('Distribution of Space Saved by Technique')
axes[0].set_xlabel('Other Techniques')
axes[0].set_ylabel('Space Saved (TiB)')
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=10)
legend_labels = ['T1: Space Saved by Clones (TiB)', 
                 'T2: Space Saved by Compaction, \n Aggregate Deduplication and Compression (TiB)', 
                 'T3: Space Saved by Volume Compression (TiB)',
                 'T4: Space Saved by Volume Deduplication (TiB)',
                 'T5: Space Saved by Snapshots (TiB)'
                 ]  
handles = [mlines.Line2D([], [], color='black', marker='o', linestyle='None', label=label) for label in legend_labels]

# Use these handles to create the legend
axes[0].legend(handles=handles, loc='upper left', fontsize='10')
# Plot 2: Box Plot for 'Space Saved by Snapshots (TiB)'
filtered_df_snapshot = sum_space_saved[sum_space_saved['Technique'] == 'Space Saved by Snapshots (TiB)']
filtered_df_snapshot['Technique'] = filtered_df_snapshot['Technique'].replace({'Space Saved by Snapshots (TiB)': 'T5'})
sns.boxplot(x='Technique', y='Space Saved', data=filtered_df_snapshot, ax=axes[1],color='steelblue')
axes[1].set_title('Box Plot for Space Saved by Snapshots (TiB)')
axes[1].set_xlabel('Snapshots Technique')
axes[1].set_ylabel('Space Saved (TiB)')
# Calculate mean, median, and standard deviation
mean_value = filtered_df_snapshot['Space Saved'].mean()
median_value = filtered_df_snapshot['Space Saved'].median()
std_value = filtered_df_snapshot['Space Saved'].std()

# Add mean, median, and standard deviation to the plot
axes[1].axhline(y=mean_value, color='red', linestyle='--', label='Mean')
axes[1].axhline(y=median_value, color='green', linestyle='--', label='Median')
axes[1].axhline(y=mean_value + std_value, color='blue', linestyle='--', label='Mean + 1 SD')
axes[1].axhline(y=mean_value - std_value, color='blue', linestyle='--', label='Mean - 1 SD')

# Show legend
axes[1].legend()
# Adjust layout for better spacing
plt.tight_layout()

# Show the plots
plt.show()

# ###############################################################################################
# Normalize data within each technique
sum_space_saved_normalized = sum_space_saved.copy()
sum_space_saved_normalized['Space Saved'] = sum_space_saved.groupby('Cluster Name')['Space Saved'].transform(lambda x: (x - x.min()) / (x.max() - x.min()))

# Plot: Bar Plot for Sum_Space_Saved_Cluster
plt.figure(figsize=(15, 6))
bar_plot = sns.barplot(x='Cluster Name', y='Space Saved', hue='Technique', data=sum_space_saved_normalized)
plt.xlabel('Cluster Name')
plt.ylabel('Normalized Space Saved')

# Rotate x-axis labels for better visibility
bar_plot.set_xticklabels(bar_plot.get_xticklabels(), rotation=45, horizontalalignment='right')
# Move the legend out of the plot area to the right
plt.legend(bbox_to_anchor=(1.05, 1), loc='lower right', borderaxespad=0., fontsize='small')

# Adjust the layout to optimize space for the plot while accommodating the smaller legend
plt.tight_layout() 
plt.show()

# ################################################################################################
# Normalize data within each technique and model
technique_model_df = melted_df.copy()
technique_model_df['Space Saved'] = technique_model_df.groupby(['Model'])['Space Saved'].transform(lambda x: (x - x.min()) / (x.max() - x.min()))

# Plot: Bar Plot for Space Saved by Technique and Model
plt.figure(figsize=(15, 6))
bar_plot_model = sns.barplot(x='Model', y='Space Saved', hue='Technique', data=technique_model_df, ci=None)
plt.xlabel('Model')
plt.ylabel('Normalized Space Saved')
plt.title('Normalized Space Saved by Technique and Model')

# Rotate x-axis labels for better visibility
bar_plot_model.set_xticklabels(bar_plot_model.get_xticklabels(), rotation=45, horizontalalignment='right')
plt.tight_layout()  # Adjust layout for better spacing
plt.show()
#################################################################################################
