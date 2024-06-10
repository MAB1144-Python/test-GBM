import pandas as pd
import sklearn
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# Path to the Excel file
excel_file = 'data_customer_classification 1.xlsx'

# Read the Excel file into a DataFrame
df = pd.read_excel(excel_file)
# Convertir la columna trans_date a tipo datetime
df['trans_date'] = pd.to_datetime(df['trans_date'])
# Calcular la fecha más reciente del conjunto de datos
max_date = df['trans_date'].max()

# Agrupar por customer_id y calcular las características
customer_features = df.groupby('customer_id').agg(
    Frequency=('trans_date', 'count'),
    Recency=('trans_date', lambda x: (max_date - x.max()).days),
    Monetary=('tran_amount', 'sum')
).reset_index()

# Mostrar las primeras filas del nuevo dataframe
print(customer_features.head())
# Crear segmentos basados en el monto total gastado
customer_features['Segment'] = pd.qcut(customer_features['Monetary'], q=3, labels=['Low', 'Medium', 'High'])

# Mostrar las primeras filas con los segmentos
print(customer_features.head())

# Seleccionar características (X) y etiquetas (y)
X = customer_features[['Frequency', 'Recency', 'Monetary']]
y = customer_features['Segment']

# Convertir las etiquetas en categorías
y = pd.get_dummies(y)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalizar los datos
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Definir el modelo
model = Sequential()
model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(y_train.shape[1], activation='softmax'))

# Compilar el modelo
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Resumen del modelo
model.summary()

# Entrenar el modelo
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

# Evaluar el modelo
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Loss: {loss}, Accuracy: {accuracy}')
import numpy as np

# Hacer predicciones
predictions = model.predict(X_test)

# Convertir las predicciones de one-hot encoding a etiquetas
predicted_classes = np.argmax(predictions, axis=1)
true_classes = np.argmax(y_test, axis=1)

# Mostrar las predicciones
print(predicted_classes.shape)

# Pérdida
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.title('Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Precisión
plt.plot(history.history['accuracy'], label='train accuracy')
plt.plot(history.history['val_accuracy'], label='val accuracy')
plt.title('Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()





# Print the DataFrame
print(df)
print(df.columns)
