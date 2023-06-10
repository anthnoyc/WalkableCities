import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import openpyxl

df = pd.read_excel("/Users/fondahu/Desktop/WalkableScoreFinal.xlsx")


# Data for scatter plot
with_mortgage = df["With Mortgage"]
without_mortgage = df["Without Mortgage"]
walk_score = df["Walk Score"]

# Concatenating the data into a single array
data = np.array([with_mortgage, without_mortgage, walk_score]).T

# Function to remove outliers based on the interquartile range (IQR)
def remove_outliers(data, threshold=1.5):
    q1 = np.percentile(data, 25, axis=0)
    q3 = np.percentile(data, 75, axis=0)
    iqr = q3 - q1
    lower_bound = q1 - threshold * iqr
    upper_bound = q3 + threshold * iqr
    mask = np.all((data >= lower_bound) & (data <= upper_bound), axis=1)
    return data[mask]

# Removing outliers from the data
filtered_data = remove_outliers(data)

# Separating the filtered data
filtered_with_mortgage, filtered_without_mortgage, filtered_walk_score = filtered_data.T

# Calculating trend lines with filtered data
with_mortgage_trend = np.polyfit(filtered_with_mortgage, filtered_walk_score, 1,full=True)
without_mortgage_trend = np.polyfit(filtered_without_mortgage, filtered_walk_score, 1,full=True)


# Extracting slope and intercept values
with_mortgage_slope, with_mortgage_intercept = with_mortgage_trend[0]
without_mortgage_slope, without_mortgage_intercept = without_mortgage_trend[0]

# Creating regression lines
with_mortgage_regression = np.poly1d([with_mortgage_slope, with_mortgage_intercept])
without_mortgage_regression = np.poly1d([without_mortgage_slope, without_mortgage_intercept])

# Plotting the scatter plot
plt.scatter(with_mortgage, walk_score, c='royalblue', label='With Mortgage')
plt.scatter(without_mortgage, walk_score, c='skyblue', label='Without Mortgage')

# Plotting trend lines
plt.plot(with_mortgage, with_mortgage_regression(with_mortgage), 'darkorange', label='With Mortgage Trend')
plt.plot(without_mortgage, without_mortgage_regression(without_mortgage), 'gold', label='Without Mortgage Trend')

# Adding labels and title
plt.xlabel('Median Housing Cost ($)')
plt.ylabel('Walk Score')
plt.title('Walk Score vs Housing Cost')

plt.ylim(0)

# Adding legend
plt.legend()
plt.legend(loc='upper right', bbox_to_anchor=(1.5, 1))

# Displaying the scatter plot
plt.show()






