import re
from http import HTTPStatus

from flask import jsonify, request, url_for

from yacut import app, db
from yacut.constants import REGULAR
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


def is_valid_content_type(content_type: str) -> bool:
    """Проверяет корректный Content-Type."""
    return content_type == "application/json"


def is_valid_custom_id(custom_id: str) -> bool:
    """Проверяет валидность пользовательского ID."""
    if not custom_id:
        return True
    return len(custom_id) <= 16 and bool(re.fullmatch(REGULAR, custom_id))


def is_short_id_available(short_id: str) -> bool:
    """Проверяет доступность short_id в БД."""
    return not URLMap.query.filter_by(short=short_id).first()


@app.route("/api/id/", methods=["POST"])
def add_url():
    if not request.data:
        raise InvalidAPIUsage(
            "Отсутствует тело запроса", HTTPStatus.BAD_REQUEST
        )

    if not is_valid_content_type(request.content_type):
        raise InvalidAPIUsage(
            "Content-Type должен быть application/json",
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        )

    try:
        data = request.get_json()
        if data is None:
            raise ValueError
    except ValueError:
        raise InvalidAPIUsage("Невалидный JSON", HTTPStatus.BAD_REQUEST)

    if "url" not in data:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!', HTTPStatus.BAD_REQUEST
        )

    custom_id = data.get("custom_id")

    if custom_id and not is_valid_custom_id(custom_id):
        raise InvalidAPIUsage(
            "Указано недопустимое имя для короткой ссылки",
            HTTPStatus.BAD_REQUEST,
        )

    short = custom_id if custom_id else get_unique_short_id()

    if not is_short_id_available(short):
        if custom_id:
            raise InvalidAPIUsage(
                "Предложенный вариант короткой ссылки уже существует.",
                HTTPStatus.BAD_REQUEST,
            )

        short = get_unique_short_id()
        if not is_short_id_available(short):
            raise InvalidAPIUsage(
                "Не удалось создать уникальную короткую ссылку",
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    url_map = URLMap(original=data["url"], short=short)
    db.session.add(url_map)
    db.session.commit()

    return (
        jsonify(
            {
                "url": data["url"],
                "short_link": url_for(
                    "redirect_view", short_id=short, _external=True
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
