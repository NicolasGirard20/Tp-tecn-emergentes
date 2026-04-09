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
    
    Respondé ÚNICAMENTE con el nombre exacto del género más adecuado que ayude a calmar o sanar esta emoción.
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



def top_animes_por_genero(genero, cantidad=5):
    """Obtiene los animes mejor puntuados de un género específico"""
    print(f"⏳ Obteniendo los top {cantidad} animes de {genero}...")
    
    genero_id = GENEROS[genero]
    url = f"https://api.jikan.moe/v4/anime?genres={genero_id}&order_by=score&sort=desc&limit={cantidad}"
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        datos = respuesta.json()['data']
        return [{
            "titulo": anime['title'],
            "generos": [g['name'] for g in anime['genres']],
            "sinopsis": anime.get('synopsis', 'Sin sinopsis')[:300]
        } for anime in datos]
    
    return []

def elegir_anime_con_ia(emocion, genero, lista_animes):
    """La IA elige el mejor anime de la lista filtrada"""
    print("\n🎬 Eligiendo el mejor anime para vos...")
    
    prompt = f"""
    El usuario se siente así: "{emocion}"
    Ya determinamos que el género ideal es: {genero}
    
    Aquí tienes los mejores animes de ese género:
    {json.dumps(lista_animes, indent=2, ensure_ascii=False)}
    
    Tu tarea:
    1. Elige EL MEJOR anime de la lista para esta persona.
    2. Respondele con empatía, decile qué anime elegiste y explicale por qué le ayudará 
       basándote en su estado de ánimo, la sinopsis y los géneros del anime.
    3. Responde con un párrafo corto, claro y amigable, sin tecnicismos ni spoilers.
    """
    
    respuesta = cliente_ia.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return respuesta.choices[0].message.content

def recomendar_anime():
    print("\n" + "="*50)
    print("🤖 BIENVENIDO AL RECOMENDADOR DE ANIME EMOCIONAL")
    print("="*50)
    emocion_usuario = input("Escribe cómo te sientes hoy o qué tuviste que pasar: ")
    
    try:
        # Paso 1: IA elige el género
        genero = elegir_genero_con_ia(emocion_usuario)
        
        # Paso 2: Jikan filtra animes por ese género
        lista_animes = [anime['titulo'] for anime in obtener_animes_por_genero(genero)]
        print(f"Se encontraron {(lista_animes)}.")
        
        if not lista_animes:
            print("No se encontraron animes para ese género, intentá de nuevo.")
            return
        
        # Paso 3: IA elige el mejor anime de esa lista
        recomendacion = elegir_anime_con_ia(emocion_usuario, genero, lista_animes)
        
        print("\n🎬 RECOMENDACIÓN PARA VOS:")
        print("-" * 50)
        print(recomendacion)
        print("-" * 50)
        
    except Exception as e:
        print(f"Hubo un error: {e}")

if __name__ == "__main__":
    # recomendar_anime()
    top_animes_por_genero