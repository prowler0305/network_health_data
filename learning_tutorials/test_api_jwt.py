# import json
import requests


def main():
    """

    :return:
    """

    root_url = 'http://127.0.0.1:5000/jwt_simple'
    auth_url = '/login'
    resource = '/protected'

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
    uscc_eng_parser_api_jwt = resp_dict.get('jwt')
    # Let's print it
    print('JSON Web Token received: %s' % uscc_eng_parser_api_jwt)
    # Example of how to make an HTTP GET request using JWT to a private resource.
    auth_header = {"Authorization": "JWT {}".format(uscc_eng_parser_api_jwt)}
    resp = requests.get(root_url + resource, headers=auth_header)
    # Check again for Server or Client Errors and raise exception if needed.
    resp.raise_for_status()
    # Print GET response text.
    print(resp.content)
    print(resp.json())
    print(resp.json().get('hello_from'))


    # # Post a new subscriber
    # payload = {'name': 'Christian Spear', 'email': 'cspear@gmail.com', 'id': '3'}
    # req = requests.post(url=subscribers_collection_req, data=payload)
    # print_api_status_code(req)
    #
    # # Query a for a single subscribers
    # req = requests.get(url=subscribers_collection_req + '/3')
    # print_api_status_code(req)
    #
    # # Delete a single subscriber
    # req = requests.delete(subscribers_collection_req + '/2')
    # print_api_status_code(req)
    #
    # # Query the whole list of subscribers
    # print_api_status_code(requests.get(subscribers_collection_req))


def print_api_status_code(request):
    """

    :param request: api request instance
    :return: None
    """
    if request.status_code == requests.codes.ok:
        print('Got to root URL')
    print(request.status_code)
    print(request.text)


if __name__ == '__main__':
    main()
