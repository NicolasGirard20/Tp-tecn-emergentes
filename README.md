## Tener descargado python

## Descargar la herramienta pip

## Instalar las dependencias necesarias
pip install requests groq python-dotenv

## En linux: cada vez que se abra el archivo ejecutar esto para activar el entorno
source venv/bin/activate

## Configurar las API keys para los llm
En https://console.groq.com/ se registra una cuenta y se crea una api key, dependiendo el modelo posee más tokens request disponibles.

## app.py
Un modelo donde en base a la emoción elige un género y a partir de la lista obtenida por la api elige la mejor para el usuario explicando porque

## app2.py
Modelo más económico de token donde el usuario dice la emoción que siente la ia traduce el texto a una palabra y de ahí se filtra la lista de la api.


