from sqladmin import ModelView

from .exception import ChangePasswordException
from core.hashing import hash_password
from tags.models import Tag
from users.models import User


class UserAdmin(ModelView, model=User):
    """
    Administrative interface view for the User model.
    """
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'
    page_size = 50

    column_list = [User.id, User.username, User.email, User.role]
    column_searchable_list = [User.username, User.email]

    async def on_model_change(self, form, model, is_created, *args, **kwargs):
        if is_created and form.get('password'):
            form['password'] = hash_password(form.get('password'))
        elif not is_created and form.get('password') != model.password:
            raise ChangePasswordException('Пароль не может быть изменён')


class TagAdmin(ModelView, model=Tag):
    """
    Administrative interface view for the Tag model.
    """
    name = 'Тег'
    name_plural = 'Теги'
    category = 'Карточки изображений'
    icon = 'fa-solid fa-tag'
    column_list = [Tag.id, Tag.name, Tag.slug]
    column_searchable_list = [Tag.name]
