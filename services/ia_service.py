from config import cliente_ia, GENEROS
import json

def elegir_genero_con_ia(emocion):
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
    if genero not in GENEROS:
        for g in GENEROS.keys():
            if g.lower() in genero.lower():
                genero = g
                break
        else:
            genero = "Drama"
    return genero

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

