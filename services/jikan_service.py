import requests
from config import GENEROS

def obtener_top10_por_genero(genero):
    genero_id = GENEROS[genero]
    url = f"https://api.jikan.moe/v4/anime?genres={genero_id}&order_by=score&sort=desc&limit=10"
    respuesta = requests.get(url)
    animes_limpios = []
    if respuesta.status_code == 200:
        datos = respuesta.json()['data']
        # Evitamos repetir animes con el mismo nombre, ya que pueden aparecer varias versiones (TV, Movie, OVA)
        vistos = set()
        for i, anime in enumerate(datos, 1):
            if anime['title'] in vistos:
                continue
            vistos.add(anime['title'])
            animes_limpios.append({
                "puesto": i,
                "titulo": anime['title'],
                "score": anime.get('score', 'N/A'),
                "generos": [g['name'] for g in anime['genres']],
                "sinopsis": anime.get('synopsis', 'Sin sinopsis')[:300]
            })
    return animes_limpios