import os
import requests
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("¡Error! No se encontró la API Key.")

cliente_ia = Groq(api_key=API_KEY)

# Géneros disponibles en Jikan con su ID
GENEROS = {
    "Action": 1, "Adventure": 2, "Comedy": 4, "Drama": 8,
    "Fantasy": 10, "Horror": 14, "Mystery": 7, "Romance": 22,
    "Sci-Fi": 24, "Slice of Life": 36, "Sports": 30,
    "Supernatural": 37, "Thriller": 41
}

def elegir_genero_con_ia(emocion):
    """La IA analiza la emoción y elige el género más adecuado"""
    print("\n🧠 La IA está analizando tu emoción...")
    
    prompt = f"""
    El usuario se siente así: "{emocion}"
    
    Géneros de anime disponibles: {", ".join(GENEROS.keys())}
    
    Respondé ÚNICAMENTE con el nombre exacto del género más adecuado para esta emoción.
    Sin explicaciones, sin puntos, solo el nombre del género.
    """
    
    respuesta = cliente_ia.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    genero = respuesta.choices[0].message.content.strip()
    
    # Verificamos que el género devuelto sea válido
    if genero not in GENEROS:
        # Buscamos el más parecido por si la IA devolvió algo ligeramente distinto
        for g in GENEROS.keys():
            if g.lower() in genero.lower():
                genero = g
                break
        else:
            genero = "Drama"  # Fallback por defecto
    
    print(f"🎭 Género elegido por la IA: {genero}")
    return genero



def obtener_top10_por_genero(genero):
    """Obtiene el top 10 animes filtrados por género ordenados por score"""
    print(f"⏳ Buscando top 10 animes de {genero}...")
    
    genero_id = GENEROS[genero]
    url = f"https://api.jikan.moe/v4/anime?genres={genero_id}&order_by=score&sort=desc&limit=10"
    respuesta = requests.get(url)
    
    animes_limpios = []
    if respuesta.status_code == 200:
        datos = respuesta.json()['data']
        for i, anime in enumerate(datos, 1):
            animes_limpios.append({
                "puesto": i,
                "titulo": anime['title'],
                "score": anime.get('score', 'N/A'),
                "generos": [g['name'] for g in anime['genres']],
                "sinopsis": anime.get('synopsis', 'Sin sinopsis')[:300]
            })
    
    return animes_limpios

emocion = input("Escribe una emoción que te describa: ")
genero = elegir_genero_con_ia(emocion)
top10 = obtener_top10_por_genero(genero)

# Mostrar la lista
print(f"\n🏆 TOP 10 ANIMES DE {genero.upper()}:")
print("-" * 50)
for anime in top10:
    print(f"{anime['puesto']}. {anime['titulo']} ⭐ {anime['score']}")
print("-" * 50)