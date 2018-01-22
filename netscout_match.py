import json
import os, datetime, sys
import requests
from os import path
import time


def main():
    """

    :return:
    """
    list_o_subscriber_ids = []
    fut_subscribers_file = '/home/aspea002/IdeaProjects/USCC_ENG_API/data_only/FUT-subscribers'

    with open(fut_subscribers_file) as fut_fh:
        for line in fut_fh:
            line = line.rstrip('\n')
            list_o_subscriber_ids.append(line)

    filepath = '/home/aspea002/IdeaProjects/USCC_ENG_API/local_test_library/netscout_match.json'
    with open(filepath) as fh:
        netscout_data = fh.read()
        netscout_data_dict = json.loads(json.loads(netscout_data))
        subscriber_id = str(netscout_data_dict.get('subscriber_id'))

        if subscriber_id is None or subscriber_id not in list_o_subscriber_ids:
            pass
        elif (15500 <= netscout_data_dict.get('response_code') <= 15598 and netscout_data_dict.get('application_id') == 50467780
              and netscout_data_dict.get('message_id') == 4) or (netscout_data_dict.get('application_id') == 58903971
                                                                 and netscout_data_dict.get('message_id') == 131085):
            print(subscriber_id)
        else:
            pass


if __name__ == '__main__':
    main()
