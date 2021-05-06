from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.database import SessionLocal
from app.models.film import Film
from app.models.review import Review
from app.models.user import User

app = Flask(__name__)
app.secret_key = 'very secret key'
admin = Admin(app, name='Film rating service', template_mode='bootstrap3')


class FilmView(ModelView):
    form_excluded_columns = ['reviews']
    column_display_pk = True
    column_searchable_list = ['title', 'year']
    column_filters = ['title', 'year']
    form_columns = ['title', 'year']
    page_size = 10


class UserView(ModelView):
    can_create = False
    column_display_pk = True
    column_list = ['id', 'login', 'reviews']
    form_columns = ['login', 'reviews']
    column_hide_backrefs = False
    page_size = 10


class ReviewView(ModelView):
    column_display_pk = True
    page_size = 10


admin.add_view(FilmView(Film, SessionLocal))
admin.add_view(UserView(User, SessionLocal))
admin.add_view(ReviewView(Review, SessionLocal))
