from http import HTTPStatus

from flask import flash, redirect, render_template, url_for

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


def create_short_url(original_url, custom_id=None):
    """Создает короткую ссылку с проверкой уникальности"""
    short = custom_id if custom_id else get_unique_short_id()
    if not URLMap.query.filter_by(short=short).first():
        url_map = URLMap(original=original_url, short=short)
        db.session.add(url_map)
        db.session.commit()
        return short
    if custom_id:
        return None
    short = get_unique_short_id()


@app.route("/", methods=["GET", "POST"])
def index_view():
    form = URLForm()
    short_url = None

    if form.validate_on_submit():
        short = create_short_url(
            original_url=form.original_link.data, custom_id=form.custom_id.data
        )

        if short:
            short_url = url_for(
                "redirect_view", short_id=short, _external=True
            )
            flash(short_url, "success")
        else:
            if form.custom_id.data:
                flash(
                    "Предложенный вариант короткой ссылки уже существует.",
                    "error",
                )
            else:
                flash(
                    "Не удалось создать уникальную ссылку. Попробуйте позже.",
                    "error",
                )

    return (
        render_template("index.html", form=form, short_url=short_url),
        HTTPStatus.OK,
    )


@app.route("/<short_id>")
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
