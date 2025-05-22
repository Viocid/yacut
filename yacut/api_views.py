import re

from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


@app.route("/api/id/", methods=["POST"])
def add_url():
    if not request.data:
        raise InvalidAPIUsage("Отсутствует тело запроса", 400)

    if request.content_type != "application/json":
        raise InvalidAPIUsage("Content-Type должен быть application/json", 415)
    if not request.is_json or request.get_json() is None:
        raise InvalidAPIUsage("Отсутствует тело запроса", 400)
    data = request.get_json()
    if "custom_id" in data and data["custom_id"]:
        if not re.fullmatch("^[a-zA-Z0-9]+$", data["custom_id"]):
            raise InvalidAPIUsage(
                "Указано недопустимое имя для короткой ссылки", 400
            )
    if "url" not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    short = data.get("custom_id") or get_unique_short_id()
    if URLMap.query.filter_by(short=short).first():
        if data.get("custom_id"):
            raise InvalidAPIUsage(
                "Предложенный вариант короткой ссылки уже существует."
            )
        short = get_unique_short_id()
    if len(short) > 16:
        raise InvalidAPIUsage(
            "Указано недопустимое имя для короткой ссылки", 400
        )
    url_map = URLMap(original=data["url"], short=short)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route("/api/id/<short_id>/", methods=["GET"])
def get_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage("Указанный id не найден", 404)
    return jsonify({"url": url_map.original}), 200
