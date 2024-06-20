from bson import ObjectId
from flask import Blueprint, jsonify, request
from models.music_model import MusicModel
from utils.map_http_status import HTTP

musics_controller = Blueprint("musics", __name__)

def _get_all_musics():
  musics = MusicModel.find()
  return [music.to_dict() for music in musics]

def _get_music(id: str):
  return MusicModel.find_one({ "_id": ObjectId(id) })


@musics_controller.route("/", methods=["GET"])
def all_musics():
  musics_list = _get_all_musics()
  return jsonify(musics_list), HTTP.OK


@musics_controller.route("/random", methods=["GET"])
def random_music():
  music = MusicModel.get_random()

  if music in None:
    return jsonify({ "error": "No musics available" }), HTTP.NO_CONTENT
  
  return jsonify(music.to_dict()), HTTP.OK


@musics_controller.route("/", methods=["POST"])
def post_music():
  new_music = MusicModel(request.json)
  new_music.save()
  return jsonify(new_music.to_dict()), HTTP.CREATED