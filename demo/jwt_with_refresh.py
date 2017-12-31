# import json
import requests


def main():
    """

    :return:
    """

    root_url = 'http://127.0.0.1:5000/jwt_ext'
    auth_url = '/login'
    resource = '/protected'
    token_refresh = '/refresh_token'

    # Set header content to indicate auth request data is in JSON format
    headers = {"Content-Type": "application/json"}
    # Dict of auth credentials
    data = {"username": "test",
            "password": "test"}
    # Perform POST request to API auth URL, passing credentials dict to be converted to JSON format and custom header
    resp = requests.post(root_url + auth_url, json=data, headers=headers)
    # check status code for either Client or Server errors and raise exception if needed.
    resp.raise_for_status()
    # convert response to JSON object and hold in python dictionary
    resp_dict = resp.json()
    # Key "access_token" contains the JWT which is required for all future requests so save it.
    access_token = resp_dict.get('access_token')
    refresh_token = resp_dict.get('refresh_token')
    # Let's print it
    print('Access Token: %s' % access_token)
    print('Refresh Token: %s' % refresh_token)
    while True:
        # Example of how to make an HTTP GET request using JWT to a private resource.
        auth_header = {"Authorization": "JWT {}".format(access_token)}
        resp = requests.get(root_url + resource, headers=auth_header)
        # Print GET response text.
        print(resp.json())
        if resp.status_code == 401 and resp.json().get('msg') == 'Token has expired':
            break

    refresh_header = {"Authorization": "JWT {}".format(refresh_token)}
    print(refresh_header)
    resp = requests.get(root_url + token_refresh, headers=refresh_header)
    print(resp.status_code)
    print(resp.json())
    if resp.status_code == 200:
        new_access_token = resp_dict.get('access_token')
        print(new_access_token)
        if new_access_token == access_token:
            print('Access tokens are the same')
            print(access_token)
            print(new_access_token)
        auth_header = {"Authorization": "JWT {}".format(new_access_token)}
        print(auth_header)
        # Print the new Access Token
        print('New Access Token: %s' % new_access_token)
        while True:
            resp = requests.get(root_url + resource, headers=auth_header)
            # Print GET response text
            print(resp.json())
            if resp.status_code == 401 and resp.json().get('msg') == 'Token has expired':
                break
    else:
        print(resp.json())


if __name__ == '__main__':
    main()
