import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("¡Error! No se encontró la API Key.")

cliente_ia = Groq(api_key=API_KEY)

GENEROS = {
    "Action": 1, "Adventure": 2, "Comedy": 4, "Drama": 8,
    "Fantasy": 10, "Horror": 14, "Mystery": 7, "Romance": 22,
    "Sci-Fi": 24, "Slice of Life": 36, "Sports": 30,
    "Supernatural": 37, "Thriller": 41
}