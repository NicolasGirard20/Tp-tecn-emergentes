from flask import Blueprint, jsonify, request
from services.ia_service import elegir_anime_con_ia, elegir_genero_con_ia
from services.jikan_service import obtener_top10_por_genero
from config import GENEROS

# Este archivo define los endpoints relacionados con anime, utilizando los servicios de IA y Jikan.
anime_bp = Blueprint('anime', __name__)

# Endpoint para obtener el top 10 de animes según la emoción del usuario.
@anime_bp.route('/top10', methods=['POST'])
def top10_por_emocion():
    datos = request.get_json()
    if not datos or 'emocion' not in datos:
        return jsonify({"error": "Falta el campo 'emocion'"}), 400

    emocion = datos['emocion']
    genero = elegir_genero_con_ia(emocion)
    top10 = obtener_top10_por_genero(genero)

    return jsonify({
        "emocion": emocion,
        "genero_elegido": genero,
        "animes": top10
    })

# Endpoint para listar los géneros disponibles.
@anime_bp.route('/generos', methods=['GET'])
def listar_generos():
    return jsonify({"generos": list(GENEROS.keys())})

# Endpoint para recomendar animes con IA, dado una emoción y un género específico.
@anime_bp.route('/recomendar', methods=['POST'])
def recomendar_anime():
    datos = request.get_json()
    if not datos or 'emocion' not in datos:
        return jsonify({"error": "Faltan los campos 'emocion' y/o 'genero'"}), 400

    emocion = datos['emocion']
    genero = elegir_genero_con_ia(emocion)  # La IA puede ajustar el género si el usuario no lo especificó bien

    if genero not in GENEROS:
        return jsonify({"error": f"Género '{genero}' no válido. Géneros disponibles: {', '.join(GENEROS.keys())}"}), 400

    
    top10 = obtener_top10_por_genero(genero)
    recomendacion = elegir_anime_con_ia(emocion, genero, top10)

    return jsonify({
        "emocion": emocion,
        "genero": genero,
        "recomendacion": recomendacion
    })
    