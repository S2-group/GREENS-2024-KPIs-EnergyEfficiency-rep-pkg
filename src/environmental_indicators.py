import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
# Read data from Excel file
df = pd.read_csv('workingenvironment.csv')
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy import stats

##########################################################################################

# Load your data
df = pd.read_csv('Workingenvironment.csv')

# Function to perform linear regression and visualize the results
def perform_linear_regression(ax, x, y, xlabel, ylabel):
    # Perform linear regression
    slope, intercept, r_value, _, _ = linregress(x, y)

    # Predict y values based on the regression line
    predicted_y = slope * x + intercept

    # Print the regression parameters
    print(f"Slope: {slope}")
    print(f"Intercept: {intercept}")
    print(f"R-squared: {r_value**2}")

    # Cross-validated R-squared scores
    model = LinearRegression()
    scores = cross_val_score(model, np.array(x).reshape(-1, 1), y, cv=5, scoring='r2')  # 5-fold cross-validation
    print(f'Cross-validated R-squared scores: {scores}')

    # Plot the original data and the regression line
    ax.scatter(x, y, label='Original Data')
    ax.plot(x, predicted_y, label='Regression Line', color='red')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()



# Create subplots
fig, axs = plt.subplots(1, 3, figsize=(12, 5))

# Combination 1: 'Actual power kW' and 'Direct CO2 Usage'
x1 = df['Actual power kW']
y1 = df['Direct CO2 Usage']
perform_linear_regression(axs[0], x1, y1, 'Actual power kW', 'Direct CO2 Usage')
# Calculate correlation coefficients

correlation_direct_co2_power = x1.corr(y1)



print(f"Correlation between Direct CO2 Usage and Actual power kW: {correlation_direct_co2_power}")

# Combination 2: 'Actual power kW' and 'Heat BTU/h'
x2 = df['Actual power kW']
y2 = df['Heat BTU/h']

perform_linear_regression(axs[1], x2, y2, 'Actual power kW', 'Heat BTU/h')
correlation_heat_power = y2.corr(x2)


print(f"Correlation between Heat BTU/h and Actual power kW: {correlation_heat_power}")
# Combination 3: 'Direct CO2 Usage' and 'Heat BTU/h'
x3 = df['Direct CO2 Usage']
y3 = df['Heat BTU/h']
perform_linear_regression(axs[2], x3, y3, 'Direct CO2 Usage', 'Heat BTU/h')

correlation_direct_co2_heat = x3.corr(y3)
print(f"Correlation between Direct CO2 Usage and Heat BTU/h: {correlation_direct_co2_heat}")
# Adjust layout and show plots
plt.tight_layout()
plt.show()
