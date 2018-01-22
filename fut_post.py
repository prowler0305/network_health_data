import requests
import json, sys, time


def main():
    """

    :return:
    """

    fut_post_url = 'http://127.0.0.1:5000/v1/fut'
    fut_post_data_1 = dict(imsi='311580704895154')
    fut_post_data_2 = dict(imsi='311580707305677')
    fut_post_data_3 = dict(imsi='311580705520444')
    fut_post_data_4 = dict(imsi='311580702595068')
    fut_post_data_5 = dict(imsi='311580704830154')
    fut_post_data_6 = dict(imsi='311580702594425')
    fut_post_data_7 = dict(imsi='311580704830207')
    fut_post_data_8 = dict(imsi='311580704862845')
    fut_post_data_9 = dict(imsi='311580707592017')
    fut_post_data_10 = dict(imsi='311580705869630')
    fut_post_data_11 = dict(imsi='311580706045064')
    fut_headers = {'content-type': 'application/json'}

    fut_post_response = requests.post(fut_post_url, json=fut_post_data_1, headers=fut_headers)
    if fut_post_response.status_code == requests.codes.created:
        print("New IMSI(s) added successful")

    sleep_counter()
    fut_post_response = requests.post(fut_post_url, json=fut_post_data_2, headers=fut_headers)
    if fut_post_response.status_code == requests.codes.created:
        print("New IMSI(s) added successful")

    sleep_counter()
    fut_post_response = requests.post(fut_post_url, json=fut_post_data_3, headers=fut_headers)
    if fut_post_response.status_code == requests.codes.created:
        print("New IMSI(s) added successful")

    sleep_counter()
    fut_post_response = requests.post(fut_post_url, json=fut_post_data_4, headers=fut_headers)
    if fut_post_response.status_code == requests.codes.created:
        print("New IMSI(s) added successful")

    sleep_counter()
    fut_post_response = requests.post(fut_post_url, json=fut_post_data_5, headers=fut_headers)
    if fut_post_response.status_code == requests.codes.created:
        print("New IMSI(s) added successful")

    sleep_counter()
    fut_post_response = requests.post(fut_post_url, json=fut_post_data_6, headers=fut_headers)
    if fut_post_response.status_code == requests.codes.created:
        print("New IMSI(s) added successful")

    sleep_counter()
    fut_post_response = requests.post(fut_post_url, json=fut_post_data_7, headers=fut_headers)
    if fut_post_response.status_code == requests.codes.created:
        print("New IMSI(s) added successful")

    sleep_counter()
    fut_post_response = requests.post(fut_post_url, json=fut_post_data_8, headers=fut_headers)
    if fut_post_response.status_code == requests.codes.created:
        print("New IMSI(s) added successful")

    sleep_counter()
    fut_post_response = requests.post(fut_post_url, json=fut_post_data_9, headers=fut_headers)
    if fut_post_response.status_code == requests.codes.created:
        print("New IMSI(s) added successful")

    sleep_counter()
    fut_post_response = requests.post(fut_post_url, json=fut_post_data_10, headers=fut_headers)
    if fut_post_response.status_code == requests.codes.created:
        print("New IMSI(s) added successful")

    sleep_counter()
    fut_post_response = requests.post(fut_post_url, json=fut_post_data_11, headers=fut_headers)
    if fut_post_response.status_code == requests.codes.created:
        print("New IMSI(s) added successful")


def sleep_counter():
    for x in range(2, 0, -1):
        time.sleep(1)
        sys.stdout.write(str(x))
        sys.stdout.flush()
    print("\n")


if __name__ == '__main__':
    main()
