from django.contrib.auth import get_user_model


@gql.django.type(get_user_model())
class User:
    id: gql.auto
    name: gql.auto
    is_superuser: gql.auto
    is_staff: gql.auto
    email: gql.auto


