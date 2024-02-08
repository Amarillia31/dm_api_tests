import requests


def post_v1_account():
    """
    Register new user
    :return:
    """
    url = "http://5.63.153.31:5051/v1/account"

    payload = {
        "login": "user_04",
        "email": "user_04@user_04",
        "password": "user_04%"
    }
    headers = {
        'X-Dm-Auth-Token': '<string>',
        'X-Dm-Bb-Render-Mode': '<string>',
        'Content-Type': 'application/json',
        'Accept': 'text/plain'
    }

    response = requests.request(
        method="POST",
        url=url,
        headers=headers,
        json=payload
    )
    return response


response = post_v1_account()
print(response)
