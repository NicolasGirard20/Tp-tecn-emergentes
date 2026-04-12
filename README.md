## Pasos
- Tener descargado python
- Descargar la herramienta pip

- En linux: cada vez que se abra el archivo ejecutar esto para activar el entorno virtual
source venv/bin/activate

- Instalar las dependencias necesarias
pip install -r requeriments.txt

- Configurar las API keys para los llm
En https://console.groq.com/ se registra una cuenta y se crea una api key, dependiendo el modelo posee más tokens request disponibles.

- app.py
Servicio de API que devuelve un texto JSON integrando dos api, donde con el tipo de petción el usuario puede pedir, listado de generos, top10 animes en base a promt o un anime recomendado por la LLm en base a la promt

## Funcionamiento
- Habilitar API
python app.py

- En otra consola
-- Top 10 animes por prompt
``` 
curl -X POST http://localhost:5000/top10   -H "Content-Type: application/json"   -d '{"emocion": "me siento triste y solo"}'
```
-- Recomendación específica de IA 
``` 
curl -X POST http://localhost:5000/recomendar   -H "Content-Type: application/json"   -d '{"emocion": "me siento triste y solo"}'
```
-- Listar generos disponibles
``` 
curl -X POST http://localhost:5000/generos   -H "Content-Type: application/json"   -d '{"emocion": "me siento triste y solo"}'
```


## Estructura de la API

APIrest/
│
├── app.py                  # Punto de entrada, solo inicializa y corre Flask
├── .env
├── requirements.txt
│
├── config.py               # Variables globales (GENEROS, cliente_ia)
│
├── routes/
│   └── anime_routes.py     # Los endpoints
│
└── services/
    ├── ia_service.py       # Funciones que llaman a Groq
    └── jikan_service.py    # Funciones que llaman a Jikan API
