# -*- coding: utf-8 -*-
"""RobotTrading.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vldGZrLTtxG0_YhecqgvhFwlwpyLtQGo
"""

# Importar librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from IPython.display import clear_output
import time

# Variables globales
df_bitcoin = pd.DataFrame()
precio_actual = 0.0
tendencia = ""
media_bitcoin = 0.0
algoritmo_decision = ""

# Función para importar el histórico de precios del Bitcoin
def importar_base_bitcoin():
   global df_bitcoin

   # Obtener los datos históricos del Bitcoin (BTC-USD) de los últimos 7 días con intervalos de 5 minutos
   df_bitcoin = yf.download("BTC-USD", period="7d", interval="5m")

# Función para extraer tendencias del precio del Bitcoin
def extraer_tendencias():
   global precio_actual, tendencia

   # Realizar web scraping en CoinMarketCap
   url = "https://coinmarketcap.com/currencies/bitcoin/"
   response = requests.get(url)
   soup = BeautifulSoup(response.content, "html.parser")

   # Encontrar el precio actual del Bitcoin (BTC)
   precio_elem = soup.find("span", class_="sc-f70bb44c-0 jxpCgO base-text")
   if precio_elem:
       precio_actual = float(precio_elem.text.strip().replace("$", "").replace(",", ""))
   else:
       precio_actual = 0.0

   # Encontrar la variación del precio en la última hora (1h %)
   variacion_elem = soup.find("p", class_="sc-4984dd93-0 sc-58c82cf9-1 fwNMDM")
   if variacion_elem:
    variacion_text = variacion_elem.text.strip()
    variacion_text = ''.join(char for char in variacion_text if char.isdigit() or char == '-' or char == '.')
    variacion = float(variacion_text)
    if variacion < 0:
      tendencia = "baja"
    else:
        tendencia = "alta"
   else:
    tendencia = ""

# Función para limpiar los datos del histórico de precios
def limpieza_datos():
   global df_bitcoin_limpio, media_bitcoin

   # Crear una copia de la base original para realizar la limpieza
   df_bitcoin_limpio = df_bitcoin.copy()

   # Tratar duplicados en el índice
   df_bitcoin_limpio = df_bitcoin_limpio[~df_bitcoin_limpio.index.duplicated(keep='first')]

   # Tratar valores nulos en la columna Close
   df_bitcoin_limpio['Close'] = df_bitcoin_limpio['Close'].fillna(method='ffill')

   # Eliminar registros con Volume igual a 0
   df_bitcoin_limpio = df_bitcoin_limpio[df_bitcoin_limpio['Volume'] > 0]

   # Identificar y eliminar outliers en la columna Close
   q1 = df_bitcoin_limpio['Close'].quantile(0.25)
   q3 = df_bitcoin_limpio['Close'].quantile(0.75)
   iqr = q3 - q1
   rango_aceptable = (q1 - 1.5 * iqr, q3 + 1.5 * iqr)
   df_bitcoin_limpio = df_bitcoin_limpio[(df_bitcoin_limpio['Close'] >= rango_aceptable[0]) & (df_bitcoin_limpio['Close'] <= rango_aceptable[1])]

   # Calcular el precio promedio
   media_bitcoin = df_bitcoin_limpio['Close'].mean()

# Función para tomar decisiones de compra o venta de Bitcoin
def tomar_decisiones():
   global algoritmo_decision

   if precio_actual >= media_bitcoin and tendencia == "baja":
       algoritmo_decision = "Vender"
   elif precio_actual < media_bitcoin and tendencia == "alta":
       algoritmo_decision = "Comprar"
   else:
       algoritmo_decision = "Esperar"

# Función para visualizar los datos y la decisión
def visualizacion():
   # Agregar la columna Promedio al dataframe original
   df_bitcoin['Promedio'] = media_bitcoin

   # Configurar el gráfico
   plt.figure(figsize=(12, 6))
   plt.title("Evolución del precio de Bitcoin y decisión de Compra/Venta")
   plt.xlabel("Fecha")
   plt.ylabel("Precio (USD)")

   # Dibujar las líneas
   df_bitcoin['Close'].plot()
   plt.axhline(y=media_bitcoin, color="r", linestyle="--", label="Precio promedio")
   # df_bitcoin['Promedio'].plot()

   # Agregar anotación con la decisión
   ultima_fecha = df_bitcoin.index[-1]
   ultimo_precio = df_bitcoin['Close'].iloc[-1]
   plt.annotate(algoritmo_decision, xy=(ultima_fecha, ultimo_precio), xytext=(10, 10), textcoords="offset points")

   # Mostrar el gráfico
   plt.show()

# Función principal
while True:
   clear_output()
   importar_base_bitcoin()
   extraer_tendencias()
   limpieza_datos()
   tomar_decisiones()
   visualizacion()
   time.sleep(300)
