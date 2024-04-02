# RobotTrading

1. **Configuración del ambiente**:
   - Puedes utilizar Google Colab, que proporciona un entorno de Jupyter Notebook listo para usar con Python 3 preinstalado.
   - Necesitaras instalar las siguientes librerías: pandas, numpy, matplotlib, requests (para hacer solicitudes web), beautifulsoup4 (para web scraping).

2. **Obtención de datos**:
   - El proyecto utiliza la API pública de CoinDesk (https://www.coindesk.com/api/) para obtener los datos históricos de precios de Bitcoin en formato JSON.
   - Se realiza el web scraping en un sitio web de noticias financieras (CoinDesk) para obtener el precio actual de Bitcoin y los indicadores de tendencia.

3. **Limpieza de datos**:
   - Cargado de los datos históricos en un DataFrame de Pandas.
   - Identificación y eliminación de valores atípicos (outliers) utilizando técnicas estadísticas.
   - Tratamiento de los valores nulos y duplicados en la base de datos.
   - Calcula el precio promedio del Bitcoin en el período seleccionado.

4. **Tomar decisiones**:
   - Se compara el precio actual obtenido por web scraping con el precio promedio calculado.
   - Si el precio actual es mayor o igual que el promedio y la tendencia es a la baja, la decisión será "Vender".
   - Si el precio actual es menor que el promedio y la tendencia es al alza, la decisión será "Comprar".
   - En caso contrario, la decisión será "Mantener".

5. **Visualización**:
   - Creación de un gráfico de líneas con matplotlib que muestre la evolución del precio del Bitcoin en el período seleccionado.
   - Trazo de una línea horizontal que represente el precio promedio.
   - Anotación al gráfico que indique la decisión actual ("Vender", "Comprar" o "Mantener").

6. **Automatización**:
   - Utilización de la librería time de Python para programar la ejecución del algoritmo de decisión cada 5 minutos.
   - Actualización del gráfico con los nuevos datos y la nueva decisión en cada iteración.
  
   - ![Captura de pantalla 2024-04-02 110428](https://github.com/saulwadeleon/RobotTrading/assets/128748724/e09686f1-6543-482c-8970-4dae762fe18c)
