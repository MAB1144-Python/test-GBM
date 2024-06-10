import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

excel_file = 'data_customer_classification 1.xlsx'

# Read the Excel file into a DataFrame
df = pd.read_excel(excel_file)

# Preview the data
print(df.head())

# Convert 'trans_date' to datetime
df['trans_date'] = pd.to_datetime(df['trans_date'])
# Aggregate data to get features for each customer
customer_features = df.groupby('customer_id').agg({
    'trans_date': lambda x: (x.max() - x.min()).days,  # shopping frequency
    'tran_amount': ['mean', 'max']  # average spending and max spending
}).reset_index()

# Rename columns for clarity
customer_features.columns = ['customer_id', 'shopping_frequency', 'avg_spending', 'max_spending']

# Normalize the features

scaler = StandardScaler()
customer_features[['shopping_frequency', 'avg_spending', 'max_spending']] = scaler.fit_transform(customer_features[['shopping_frequency', 'avg_spending', 'max_spending']])

#print(customer_features.head())

# From the elbow plot, choose the optimal number of clusters (assume k=3 for this case)
kmeans = KMeans(n_clusters=3, random_state=42)
customer_features['cluster'] = kmeans.fit_predict(customer_features[['shopping_frequency', 'avg_spending', 'max_spending']])

#print(customer_features)

# From the elbow plot, choose the optimal number of clusters (assume k=3 for this case)
kmeans = KMeans(n_clusters=3, random_state=42)
customer_features['cluster'] = kmeans.fit_predict(customer_features[['shopping_frequency', 'avg_spending', 'max_spending']])

print(customer_features.groupby('cluster').count())

# # Analyze the resulting clusters
# cluster_summary = customer_features.groupby('cluster').mean()
# #print(cluster_summary)

# Visualize the clusters

sns.pairplot(customer_features, hue='cluster', vars=['shopping_frequency', 'avg_spending', 'max_spending'])
plt.show()

# Save the model and scaler for future use
# import joblib

# joblib.dump(kmeans, 'kmeans_model.pkl')
# joblib.dump(scaler, 'scaler.pkl')
