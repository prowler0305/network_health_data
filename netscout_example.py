import json
import os, datetime, sys
import requests
from os import path
import time


def main():
    """

    :return:
    """

    netscout_data_by_subscriber_1 = dict(controlplane_transaction_start_time=None,
                                         device_interface_type=None,
                                         device_name=None,
                                         subscriber_id=None
                                         )

    netscout_data_by_subscriber_2 = dict(application_id=None,
                                         message_id=None,
                                         )

    netscout_data_by_subscriber_3 = dict(your_name=None,
                                         email=None,
                                         )

    # netscout_data_by_subscriber = {
    #     "device_interface_type": "S1_MME",
    #     "device_name": "mocolu01-netscout-pr03:if4",
    #     "subscriber_id": 311580704895154,
    #     "controlplane_transaction_start_time": "2018-01-15 15:17:52.846000 UTC"
    # }

    list_o_netscout_data_fields_to_extract = [
        'controlplane_transaction_start_time',
        'device_interface_type',
        'device_name',
        'application_id',
        'message_id'
    ]
    list_dictionary_data_return = []

    list_times = []
    total_exec_time = 0
    # TODO: Start of code to detect if Imsi tracking file/list changed and create new list if changed
    # Initialize a list of Imzis
    list_o_subscriber_ids = []
    # filepath location
    fut_subscribers_file = '/home/aspea002/IdeaProjects/USCC_ENG_API/data_only/FUT-subscribers'
    # Init modification date
    mod_date = None
    # print(datetime.datetime.fromtimestamp(mod_date))
    # TODO: for loop is just for demo
    for i in range(12):
        print("%s time through the loop" % str(i + 1))
        # if modification date is None (first time reading from file only) or saved mod_date is earlier than current mod date
        # we need to rebuild our list of tracked IMSIs.
        if mod_date is None or mod_date < path.getmtime(fut_subscribers_file):
            start_time = time.time()  # temp code for timing
            # Clear/Init the list of IMSI's for rebuilding
            list_o_subscriber_ids = []
            # print("file has changed building the list of subscribers")
            # Open the file and for every line(ID) add it to the list.
            with open(fut_subscribers_file) as fut_fh:
                mod_date = path.getmtime(fut_subscribers_file)
                for line in fut_fh:
                    line = line.rstrip('\n')
                    # if line not in list_o_subscriber_ids:
                    list_o_subscriber_ids.append(line)
            single_exec_time = time.time() - start_time
            # print("--- %s seconds ---" % single_exec_time)
            list_times.append(single_exec_time)
            # for subscriber_id in list_o_subscriber_ids:
            #     print(subscriber_id)
        for x in range(2, 0, -1):
            time.sleep(1)
            sys.stdout.write(str(x))
            sys.stdout.flush()
        print("\n")
    time.sleep(10)
    for subscriber_id in list_o_subscriber_ids:
        print(subscriber_id)

    for single_time in list_times:
        total_exec_time = single_time + total_exec_time
    average_time = total_exec_time/len(list_times)
    print("Average execution time = %s" % str(average_time))

    filepath = '/home/aspea002/IdeaProjects/USCC_ENG_API/local_test_library/netscout.json'
    with open(filepath) as fh:
        netscout_data = fh.read()
        netscout_data_dict = json.loads(netscout_data)
        # print(netscout_data_dict)
        # TODO: Here down is code Bill needs in his fut_imsi_check.py
        subscriber_id = netscout_data_dict.get('subscriber_id')
        if subscriber_id is not None and str(subscriber_id) in list_o_subscriber_ids:
            print("Matching subscriber ID found - %s" % subscriber_id)
            print("Updating subscriber_id in output data")
            netscout_data_by_subscriber_1['subscriber_id'] = subscriber_id
            for index in list_o_netscout_data_fields_to_extract:
                if netscout_data_dict.get(index) is not None:
                    print("\nUpdating '%s' in netscout databy subscriber dictionary..." % index)
                    if index in ['controlplane_transaction_start_time', 'device_interface_type', 'device_name']:
                        netscout_data_by_subscriber_1[index] = netscout_data_dict.get(index)
                    else:
                        netscout_data_by_subscriber_2[index] = netscout_data_dict.get(index)
            netscout_data_by_subscriber_3['your_name'] = 'Andrew Spear'
            netscout_data_by_subscriber_3['email'] = 'Andrew.Spear@uscellular.com'
            print("\nConverting netscout_data_by_subscriber dictionary to JSON object for transmitting")
            list_dictionary_data_return.append(netscout_data_by_subscriber_1)
            list_dictionary_data_return.append(netscout_data_by_subscriber_2)
            list_dictionary_data_return.append(netscout_data_by_subscriber_3)
    return json.dumps(list_dictionary_data_return)


def process_netscout_data(json_data):
    """

    :param json_data:
    :return:
    """
    print(json_data)
    list_of_dict = json.loads(json_data)
    print("Printing each separate dictionary from the list:")
    for netscout_data_dict in list_of_dict:
        print(netscout_data_dict)


if __name__ == '__main__':
    netscout_json_data = main()
    process_netscout_data(netscout_json_data)



