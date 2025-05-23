import re
from http import HTTPStatus

from flask import jsonify, request, url_for

from yacut import app, db
from yacut.constants import REGULAR
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


def validate_request_data():
    """Валидация входящего запроса и данных"""
    if not request.data:
        raise InvalidAPIUsage(
            "Отсутствует тело запроса", HTTPStatus.BAD_REQUEST
        )

    if request.content_type != "application/json":
        raise InvalidAPIUsage(
            "Content-Type должен быть application/json",
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        )

    try:
        data = request.get_json()
        if data is None:
            raise ValueError
        return data
    except ValueError:
        raise InvalidAPIUsage("Невалидный JSON", HTTPStatus.BAD_REQUEST)


def validate_custom_id(custom_id: str):
    """Валидация пользовательского short_id"""
    if custom_id and not re.fullmatch(REGULAR, custom_id):
        raise InvalidAPIUsage(
            "Указано недопустимое имя для короткой ссылки",
            HTTPStatus.BAD_REQUEST,
        )
    if custom_id and len(custom_id) > 16:
        raise InvalidAPIUsage(
            "Указано недопустимое имя для короткой ссылки",
            HTTPStatus.BAD_REQUEST,
        )


def create_url_map(original_url: str, custom_id: str = None) -> URLMap:
    """Создает и возвращает новый URLMap объект"""
    short = custom_id if custom_id else get_unique_short_id()

    if not URLMap.query.filter_by(short=short).first():
        return URLMap(original=original_url, short=short)
    if custom_id:
        raise InvalidAPIUsage(
            "Предложенный вариант короткой ссылки уже существует.",
            HTTPStatus.BAD_REQUEST,
        )
    short = get_unique_short_id()

    raise InvalidAPIUsage(
        "Не удалось создать уникальную короткую ссылку",
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )


@app.route("/api/id/", methods=["POST"])
def add_url():
    data = validate_request_data()

    if "url" not in data:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!', HTTPStatus.BAD_REQUEST
        )

    custom_id = data.get("custom_id")
    validate_custom_id(custom_id)

    url_map = create_url_map(data["url"], custom_id)
    db.session.add(url_map)
    db.session.commit()

    return (
        jsonify(
            {
                "url": data["url"],
                "short_link": url_for(
                    "redirect_view", short_id=url_map.short, _external=True
                ),
            }
        ),
        HTTPStatus.CREATED,
    )


@app.route("/api/id/<short_id>/", methods=["GET"])
def get_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage("Указанный id не найден", HTTPStatus.NOT_FOUND)
    return jsonify({"url": url_map.original}), HTTPStatus.OK
