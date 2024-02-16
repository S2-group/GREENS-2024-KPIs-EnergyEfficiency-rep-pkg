import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import probplot
from scipy.stats import shapiro

# Step 1: Read historical data
historical_data = pd.read_excel('./data/data.xlsx', sheet_name='Past and Forecast Data')

# Step 2: Filter data for years 2022 and 2023
historical_data['Year'] = historical_data['Month'].str.split('-').str[1].astype(int)
filtered_historical_data = historical_data[historical_data['Year'].isin([22, 23])]



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


result_data = pd.DataFrame(columns=['Host Name', 'Model','Cluster','Representative Value'])
normality_nodes = filtered_historical_data.groupby('Host Name')['Used Capacity Percentage']

for group_name, subset_data in normality_nodes:
    # Check if there are at least three data points for the current group
    if len(subset_data) < 3:
        print(f"Not enough data points for group {group_name}. Skip normality check.")
        continue

    # Check normality using Shapiro-Wilk test
    _, p_value = shapiro(subset_data)
    print(group_name)
    # print(p_value)
    if p_value > 0.05:
        print(f"The data for group {group_name} appears to be normally distributed.")
        representative_value = subset_data.mean()
    else:
        print(f"The data for group {group_name} does not appear to be normally distributed.")
        representative_value = subset_data.median()

     # Extract 'Model' for the current group
    model = filtered_historical_data.loc[filtered_historical_data['Host Name'] == group_name, 'Model'].iloc[0]
    cluster = filtered_historical_data.loc[filtered_historical_data['Host Name'] == group_name, 'Cluster Name'].iloc[0]
    # Append the result to the new DataFrame
    result_data = pd.concat([result_data, pd.DataFrame({'Host Name': [group_name], 'Model': [model], 'Cluster': [cluster],'Representative Value': [representative_value]})], ignore_index=True)
# Display the result
print(result_data)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Create a box plot for Representative Capacity Utilisation (%) by Node Model - Period 2022-2023
plt.figure(figsize=(12, 8))
sns.boxplot(x='Model', y='Representative Value', data=result_data, color='steelblue')
plt.xlabel('Node Model')
plt.ylabel('Representative Value of Capacity Utilisation (%)')
plt.show()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Create a bar plot for Representative Value of Capacity Utilisation (%) per Node
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Filtering Section (Optional)
# For filtering use the code below with a specific model

# filtered_nodes = filtered_historical_data[filtered_historical_data['Model'] == 'AFF-A700s']
# filtered_historical_data = filtered_nodes
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
plt.figure(figsize=(12, 6))
sns.barplot(x='Host Name', y='Representative Value', hue='Cluster', data=result_data)
plt.xlabel('Node Name')
plt.ylabel('Representative Value')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.legend(title='Model', loc='upper right')
plt.tight_layout()
plt.show()
