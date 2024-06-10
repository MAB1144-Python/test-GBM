import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

excel_file = 'data_customer_classification 1.xlsx'

# Read the Excel file into a DataFrame
df = pd.read_excel(excel_file)

# Preview the data
print(df.head())

# Calcular los días entre transacciones para cada cliente
df.sort_values(by=['customer_id', 'trans_date'], inplace=True)
df['prev_trans_date'] = df.groupby('customer_id')['trans_date'].shift(1)
df['days_between'] = (df['trans_date'] - df['prev_trans_date']).dt.days

# Agregar datos para obtener características por cada cliente
customer_features = df.groupby('customer_id').agg({
    'trans_date': [lambda x: (x.max() - x.min()).days,  # frecuencia de compra (total de días)
                   lambda x: (pd.Timestamp.now() - x.max()).days],  # recencia de la compra
    'tran_amount': ['mean', 'max', 'var', 'count'],  # gasto promedio, gasto máximo, varianza del gasto, número de transacciones
    'days_between': 'var'  # varianza de la frecuencia de compra
}).reset_index()

# Renombrar columnas para mayor claridad
customer_features.columns = [
    'customer_id', 'shopping_frequency', 'recency', 
    'avg_spending', 'max_spending', 'spending_variance', 
    'transaction_count', 'frequency_variance'
]

# Rellenar valores NaN en la varianza del gasto y varianza de frecuencia (pueden ocurrir si el cliente tiene solo una transacción)
customer_features['spending_variance'].fillna(0, inplace=True)
customer_features['frequency_variance'].fillna(0, inplace=True)

# Normalizar las características

scaler = StandardScaler()
customer_features_scaler = customer_features.copy()
customer_features_scaler[['shopping_frequency', 'recency', 'avg_spending', 'max_spending', 'spending_variance', 'transaction_count', 'frequency_variance']] = scaler.fit_transform(customer_features[['shopping_frequency', 'recency', 'avg_spending', 'max_spending', 'spending_variance', 'transaction_count', 'frequency_variance']])

print(customer_features_scaler.head())

# From the elbow plot, choose the optimal number of clusters (assume k=3 for this case)
kmeans = KMeans(n_clusters=3, random_state=42)
customer_features['cluster'] = kmeans.fit_predict(customer_features_scaler[['shopping_frequency', 'avg_spending', 'max_spending','frequency_variance']])

print(customer_features.groupby('cluster').count())

# # Analyze the resulting clusters
# cluster_summary = customer_features.groupby('cluster').mean()
# #print(cluster_summary)

# Visualize the clusters

sns.pairplot(customer_features, hue='cluster', vars=['shopping_frequency', 'recency', 'avg_spending', 'max_spending', 'transaction_count', 'frequency_variance'])
plt.tight_layout()

# Visualize the clusters in 3D
fig = plt.figure()

# First subplot
ax1 = fig.add_subplot(221, projection='3d')
x1 = customer_features['shopping_frequency']
y1 = customer_features['avg_spending']
z1 = customer_features['max_spending']
c1 = customer_features['cluster']
ax1.scatter(x1, y1, z1, c=c1, cmap='viridis')
ax1.set_xlabel('Shopping Frequency')
ax1.set_ylabel('Average Spending')
ax1.set_zlabel('Max Spending')
ax1.set_title('Cluster Analysis')

# Second subplot
customer_features_0 = customer_features[customer_features['cluster'] == 0]
ax2 = fig.add_subplot(222, projection='3d')
x2 = customer_features_0['shopping_frequency']
y2 = customer_features_0['avg_spending']
z2 = customer_features_0['max_spending']
c2 = customer_features_0['cluster']
ax2.scatter(x2, y2, z2, c=c2, cmap='viridis')
ax2.set_xlabel('Shopping Frequency')
ax2.set_ylabel('Average Spending')
ax2.set_zlabel('Max Spending')
ax2.set_title('Cluster High value customers')

# Third subplot
customer_features_1 = customer_features[customer_features['cluster'] == 1]
ax3 = fig.add_subplot(223, projection='3d')
x3 = customer_features_1['shopping_frequency']
y3 = customer_features_1['avg_spending']
z3 = customer_features_1['max_spending']
c3 = customer_features_1['cluster']
ax3.scatter(x3, y3, z3, c=c3, cmap='viridis')
ax3.set_xlabel('Shopping Frequency')
ax3.set_ylabel('Average Spending')
ax3.set_zlabel('Max Spending')
ax3.set_title('Cluster Low value customers')

# Fourth subplot
customer_features_2 = customer_features[customer_features['cluster'] == 2]
ax4 = fig.add_subplot(224, projection='3d')
x4 = customer_features_2['shopping_frequency']
y4 = customer_features_2['avg_spending']
z4 = customer_features_2['max_spending']
c4 = customer_features_2['cluster']
ax4.scatter(x4, y4, z4, c=c4, cmap='viridis')
ax4.set_xlabel('Shopping Frequency')
ax4.set_ylabel('Average Spending')
ax4.set_zlabel('Max Spending')
ax4.set_title('Cluster medium value customers')

plt.show()

