import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from math import sqrt

# Arquivo dataframe que sera analisado
df = pd.read_csv('BTC-USD.csv')                                                                                         #Leitura do arquivo CSV: dados de BTC dos ultimos 5 anos

print(df.shape)                                                                                                         #Exibe a dimensao do datframe
print(df.head())                                                                                                        #Exibe 5 primeiros dados do dataframe

# Elimina a coluna de data
df = df.drop(columns=['Date'])                                                                                          #Elimina a coluna de data

print(df.columns)                                                                                                       #Exibe as colunas atualizadas do dataframe

correlation_matrix = df.corr()                                                                                          #Calculo da matriz de correlacao entre colunas do dataframe

# Filtro para verificar correlacoes entre dados maiores que threshold
threshold = 0.1                                                                                                         #Limite de threshold (constante arbitraria)
high_correlations = correlation_matrix[(abs(correlation_matrix) > threshold)]                                           #Filtro de altas correlacoes (maiores que threshold)

print(high_correlations)                                                                                                #Exibe a matriz com os dados de altas correlacoes

# Plot da matriz de altas correlacoes, com uma formato de mapas de calor
plt.figure()
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', annot_kws={"size": 10})
plt.title('Heatmap da Matriz de Correlação')

X = df.drop(columns=['Close'])                                                                                          #Todas as colunas exceto o 'Close' como features
y = df['Close']                                                                                                         #Variavel de predicao: 'Close'

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.205, random_state=42)                             #Conjunto de dados em treino (80%) e teste (20%)

# Escala os dados para o algoritmo KNN
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Modelo: KNN
knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(X_train_scaled, y_train)

# Previsoes
y_pred_knn = knn.predict(X_test_scaled)

# Avaliacao de modelo: erro quadratico medio (MSE)
mse_knn = mean_squared_error(y_test, y_pred_knn)
rmse_knn = sqrt(mse_knn)
print(f'RMSE de KNN: {rmse_knn}')

# Plot das previsoes vs valores reais
plt.figure()
plt.plot(np.arange(len(y_test)), y_test, label='Valor Real', color='blue')
plt.plot(np.arange(len(y_test)), y_pred_knn, label='Valor Previsto por KNN', linestyle='--', color='red')
plt.title('Previsão de Preço do BTC vs Valores Reais')
plt.xlabel('Amostra')
plt.ylabel('Preço de Fechamento (USD)')
plt.legend()
plt.show()

joblib.dump(knn, 'knn_model.pkl')  # Salva o modelo KNN em um arquivo
joblib.dump(scaler, 'scaler.pkl')  # Salva o escalador em um arquivo

knn_loaded = joblib.load('knn_model.pkl')
scaler_loaded = joblib.load('scaler.pkl')

