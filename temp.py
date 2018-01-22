import json
from os import path
import time


def main():

    event_router_data = dict(event_id='1', node_id='2', opt_parms=None)

    netscout_subdata = dict(cal_timestamp_time=None, device_ip_address=None,
                            controlplane_transaction_status_id=None,
                            device_interface_number=None,
                            subscriber_id=None,
                            application_id=None,
                            message_id=None, response_code=None,
                            controlplane_transaction_start_time=None
                            )

    database_data = dict(cal_timestamp_time=None,
                         device_ip_address=None,
                         device_interface_number=None,
                         subscriber_id=None,
                         application_id=None,
                         message_id=None,
                         userequipment_imeisv=None,
                         controlplane_transaction_status_id=None,
                         response_code=None,
                         controlplane_transaction_start_time=None,
                         subscriber_msisdn=None,
                         cell_id=None,
                         cell_mcc=None,
                         cell_mnc=None,
                         userequipment_sv=None,
                         handset_id=None,
                         device_name=None,
                         application_name=None,
                         message_protocol_type_code=None,
                         message_name=None,
                         handset_name=None,
                         apn_name=None,
                         controlplane_transaction_status_name=None
                         )

    # Initialize a list of Imzis
    list_o_subscriber_ids = []
    # filepath location
    fut_subscribers_file = '/home/aspea002/IdeaProjects/USCC_ENG_API/data_only/FUT-subscribers'
    # Init modification date
    mod_date = None

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

    # TODO: replace the with open code to the 'if subscriber_id...' statemenet with your 'for message in consumer'
    filepath = '/home/aspea002/IdeaProjects/USCC_ENG_API/local_test_library/netscout_match.json'
    with open(filepath) as fh:
        netscout_data = fh.read()
        netscout_data_dict = json.loads(json.loads(netscout_data))
        subscriber_id = str(netscout_data_dict.get('subscriber_id'))
        if subscriber_id not in list_o_subscriber_ids:
            pass  # This would be your continue
        elif (15500 <= netscout_data_dict.get('response_code') <= 15598 and netscout_data_dict.get('application_id') == 50467780
              and netscout_data_dict.get('message_id') == 4) or (netscout_data_dict.get('application_id') == 58903971
                                                                 and netscout_data_dict.get('message_id') == 131085):
            for key in netscout_subdata.keys():
                netscout_subdata[key] = netscout_data_dict.get(key)
            for key in database_data.keys():
                database_data[key] = netscout_data_dict.get(key)
            event_router_data['opt_parms'] = netscout_subdata
        else:
            pass  # This will be continue

    print("Netscout Subdata Extracted:")
    for key, data in netscout_subdata.items():
        print('%s:%s' % (key, data))

    print("\nDatabase data:")
    for key, data in database_data.items():
        print('%s:%s' % (key, data))

    # Replace these print statements with code to post to alarm
    print(json.dumps(event_router_data))
    print(json.dumps(database_data))

    return json.dumps(event_router_data)


def process_event_router_data(event_router_json):
    """
    Sets up the dictionary to needed to "send an event"

    :param event_router_json:
    :return:
    """

    # init dictionary
    event_data = dict(event_id=None, node_id=None)
    # Convert json object to dictionary
    user_sent_data = json.loads(event_router_json)
    for key in user_sent_data:
        if key == 'node_id' or key == 'event_id':
            event_data[key] = user_sent_data.get(key)
        elif key == 'opt_parms':
            opt_parm_dict = user_sent_data.get(key)
            i = 1
            for opt_parm_key, opt_parm_value in opt_parm_dict.items():
                event_data['field_' + str(i)] = opt_parm_key
                event_data['value_' + str(i)] = opt_parm_value
                i += 1
        else:
            continue
    print(json.dumps(event_data))
    for key, value in event_data.items():
        print('%s: %s' % (key, value))


if __name__ == '__main__':
    event_router_json_obj = main()
    process_event_router_data(event_router_json_obj)
