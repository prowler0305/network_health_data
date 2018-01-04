import requests


def main():
    """

    :return:
    """

    root_url = 'http://127.0.0.1:5000/api/v1/'
    # list_of_requests = [
    #     root_url,
    #     (root_url + 'articles'),
    #     (root_url + 'articles/123'),
    #     (root_url + 'hello'),
    #     (root_url + 'hello?name=Andrew'),
    #     (root_url + 'data'),
    #     (root_url + 'users/3'),
    #     (root_url + 'users/4'),
    # ]

    # for req in list_of_requests:
    #     print(req)
    #     req_rc = requests.get(req)
    #     print_api_status_code(req_rc)

    subscribers_collection_req = root_url + 'subscribers'
    # Query entire list of subscribers
    print_api_status_code(requests.get(subscribers_collection_req))

    # Post a new subscriber
    payload = {'name': 'Christian Spear', 'email': 'cspear@gmail.com', 'id': '3'}
    req = requests.post(url=subscribers_collection_req, data=payload)
    print_api_status_code(req)

    # Query a for a single subscribers
    req = requests.get(url=subscribers_collection_req + '/3')
    print_api_status_code(req)

    # Delete a single subscriber
    req = requests.delete(subscribers_collection_req + '/2')
    print_api_status_code(req)

    # Query the whole list of subscribers
    print_api_status_code(requests.get(subscribers_collection_req))


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


