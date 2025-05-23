import random
import string

from yacut.constants import MAX_LENGHT_SHORT
from yacut.models import URLMap

ALLOWED_CHARS = string.ascii_letters + string.digits


def get_unique_short_id(length=MAX_LENGHT_SHORT):
    while True:
        short_id = "".join(random.choices(ALLOWED_CHARS, k=length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
