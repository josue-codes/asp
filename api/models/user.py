from mongoengine import Document, StringField, EmailField, ListField

from api.roles import Roles


class User(Document):
    given_name = StringField(required=True)
    surname = StringField(required=True)
    email = EmailField(required=True, unique=True)
    hashed_password = StringField(required=False)
    roles = ListField(required=True, default=Roles.client.value)

    def dict(self) -> dict:
        return {
            'given_name': self.given_name,
            'surname': self.surname,
            'email': self.email,
            'roles': self.roles,
        }


if __name__ == '__main__':  # pragma: no cover
    pass
