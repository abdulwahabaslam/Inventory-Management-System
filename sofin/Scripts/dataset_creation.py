import pandas as pd
import numpy as np

# Define the number of data points
num_data_points = 100

# Generate random data for the features
data = {
    'Turnover_Rate': np.random.uniform(1, 10, num_data_points),
    'Holding_Cost': np.random.uniform(100, 1000, num_data_points),
    'Obsolescence_Risk': np.random.uniform(0, 1, num_data_points),
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define a function to label health scores
def label_health_score(row):
    if row['Turnover_Rate'] > 5 and row['Holding_Cost'] < 500 and row['Obsolescence_Risk'] < 0.3:
        return 'Good'
    elif row['Turnover_Rate'] > 3 and row['Holding_Cost'] < 800 and row['Obsolescence_Risk'] < 0.5:
        return 'Average'
    else:
        return 'Bad'

# Apply the function to create the Health_Score column
df['Health_Score'] = df.apply(label_health_score, axis=1)

# Save the dataset as a CSV file
df.to_csv('inventory_health_scores.csv', index=False)
