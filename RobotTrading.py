# Importar librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from time import sleep

# Función para obtener datos históricos de la API de CoinDesk
def obtener_datos_historicos(fecha_inicio, fecha_final):
    url = f"https://api.coindesk.com/v1/bpi/historical/close.json?start={fecha_inicio}&end={fecha_final}"
    respuesta = requests.get(url)
    data = respuesta.json()
    df = pd.DataFrame.from_dict(data["bpi"], orient="index")
    df.index = pd.to_datetime(df.index)
    return df

# Función para realizar web scraping y obtener precio actual y tendencia
def obtener_datos_actuales():
    url = "https://www.coindesk.com/price/bitcoin/"
    respuesta = requests.get(url)
    soup = BeautifulSoup(respuesta.content, "html.parser")

    # Obtener precio actual
    precio_actual = soup.find("span", class_="currency-pricestyles__Price-sc-1v249sx-0 fcfNRE").text.strip()

    # Obtener tendencia
    tendencia = soup.find("div", class_="price-valuestyles__PriceValueWrapper-sc-h5ehzl-0 gZsLZm")
    if tendencia.text.strip() == "▲":
        tendencia = "alta"
    else:
        tendencia = "baja"

    return float(precio_actual.replace(",", "")), tendencia

# Función para limpiar y procesar los datos
def preproceso_datos(df):
    # Eliminar outliers
    df = df[np.abs(df - df.mean()) <= (3 * df.std())]

    # Tratar valores nulos
    df = df.fillna(method="ffill")

    # Calcular precio promedio
    precio_promedio = df.mean()[0]

    return df, precio_promedio

# Función para tomar decisiones de trading
def tomar_decision(precio_actual, tendencia, precio_promedio):
    if precio_actual >= precio_promedio and tendencia == "baja":
        decision = "Vender"
    elif precio_actual < precio_promedio and tendencia == "alta":
        decision = "Comprar"
    else:
        decision = "Mantener"

    return decision

# Función para visualizar los datos y la decisión
def visualizacion_datos(df, precio_promedio, decision):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df[0], label="Precio de Bitcoin")
    plt.axhline(y=precio_promedio, color="r", linestyle="--", label="Precio promedio")
    plt.xlabel("Fecha")
    plt.ylabel("Precio (USD)")
    plt.title("Evolución del precio de Bitcoin")
    plt.legend()

    # Agregar anotación con la decisión
    ultima_fecha = df.index[-1]
    ultimo_precio = df[0].iloc[-1]
    plt.annotate(decision, xy=(ultima_fecha, ultimo_precio), xytext=(10, 10), textcoords="offset points")

    plt.show()

# Función principal
def main():
    # Obtener datos históricos
    fecha_inicio = "2024-01-01"
    fecha_final = "2024-04-02"
    datos_historicos = obtener_datos_historicos(fecha_inicio, fecha_final)

    while True:
        # Obtener precio actual y tendencia
        precio_actual, tendencia = obtener_datos_actuales()

        # Limpiar y procesar los datos
        limpiar_datos, precio_promedio = preproceso_datos(datos_historicos)

        # Tomar decisión de trading
        decision = tomar_decision(precio_actual, tendencia, precio_promedio)

        # Visualizar los datos y la decisión
        visualizacion_datos(limpiar_datos, precio_promedio, decision)

        # Esperar 5 minutos antes de la siguiente iteración
        sleep(300)

if __name__ == "__main__":
    main()
