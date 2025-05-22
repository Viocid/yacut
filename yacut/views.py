from flask import flash, redirect, render_template, url_for

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


@app.route("/", methods=["GET", "POST"])
def index_view():
    form = URLForm()
    short_url = None

    if form.validate_on_submit():
        short = form.custom_id.data or get_unique_short_id()
        if URLMap.query.filter_by(short=short).first():
            flash(
                "Предложенный вариант короткой ссылки уже существует.", "error"
            )
        else:
            url_map = URLMap(original=form.original_link.data, short=short)
            db.session.add(url_map)
            db.session.commit()
            short_url = url_for(
                "redirect_view", short_id=short, _external=True
            )
            flash(short_url, "success")

    return render_template("index.html", form=form, short_url=short_url), 200


@app.route("/<short_id>")
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
