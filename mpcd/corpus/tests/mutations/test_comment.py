


@pytest.mark.django_db(transaction=True)
def test_create_comment(db, gql_client: GraphQLTestClient):
    query = """
    mutation CreateComment($input: CommentInput!) {
    createComment(input: $input) {
        ... on  Comment{
        text
        user {
            id
        }
        }

        ... on OperationInfo{
        messages{
            kind
            message
            field
        }
        }
    }
    }

    """
    user = UserFactory.create()
    print("USER_FAKER", user, to_base64("User", user.pk))
    res = gql_client.query(
        query,
        {
            "input": {
                "user": {"id": to_base64("User", user.pk)},
                "text": "This is a comment",
            }
        },
    )

    assert res.data == {
        "createComment": {
            "user": {"id": to_base64("User", user.pk)},
            "text": "This is a comment",
        }

    }
    print(res)
