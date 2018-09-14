from common.common import Common
import cx_Oracle
import os
import json

def main():
    """
    
    :return: 
    """

    # carrier_smtp_syntax = dict(att='mms.att.net', verizon='vtext.com', uscc='email.uscc.net')

    # svt_rc, svt_dict = Common.read_json_file('svt_tests')
    # if svt_rc:
    #     for test_name in svt_dict.get('test_names'):
    #         print(test_name)
    """
    "netcool": {
        "host": "shracdev-scan.uscc.com:1521",
        "user": "automation_ro",
        "passwd": "automation_ro",
        "db": "netcoold"
    },
    "netcool_prod": {
        "host": "shrac-scan.uscc.com:1521",
        "user": "automation_ro",
        "passwd": "automation_ro",
        "db": "netcool"
    }
    """
    nh_status_path = os.environ.get('neh_status')
    nh_lcc_map_path = os.environ.get('neh_lcc_map')
    nh_status_rc, nh_status_dict = Common.read_json_file(nh_status_path)
    nh_lcc_rc, nh_lcc_dict = Common.read_json_file(nh_lcc_map_path)
    if not nh_status_rc:
        print("Network Health Status file couldn't be obtained.")
        return False

    if not nh_lcc_rc:
        print("Network Health LCC Map file couldn't be obtained.")
        return False

    con = cx_Oracle.connect("automation_ro/automation_ro@shracdev-scan.uscc.com:1521/netcoold")

    cursor = con.cursor()
    cursor.execute("""SELECT c_alarmsource, c_lastoccurrence, c_summary, c_alertkey, c_suppressescl, c_ttnumber 
    FROM netcoold.alerts_status_t WHERE c_lastoccurrence > (CURRENT_TIMESTAMP - .0833) 
    AND c_alertgroup = 'ASCOM Availibility Alarms' ORDER BY 1,4,2 """)

    # Get all the column names for the result set
    column_name_list = [x[0] for x in cursor.description]

    # Join the column names and the data for each row into a dictionary for easier processing.
    result_dicts = [dict(zip(column_name_list, row)) for row in cursor.fetchall()]
    # result_dicts = [dict(zip(column_name_list, cursor.fetchone()))]

    # Initialize a dictionary of lists by SVT test name that contains list of LCCs. These lists are used to keep track
    # of what LCCs we updated by removing the LCC for the SVT test name in the result set. At the end of processing the
    # result set any LCCs that didn't get their status updated will be left in the lists and are assumed to have a
    # "COMM AlARM" status that indicates the test didn't run. In the status config dictionary this will be replaced
    # with a 'warning' status.
    lcc_tracking_results_dict = dict()
    for test_name in nh_status_dict:
        lcc_tracking_results_dict[test_name] = list(nh_lcc_dict.values())

    for test_name in nh_status_dict.keys():
        for result in result_dicts:
            if test_name in result.get('C_ALERTKEY'):
                if nh_lcc_dict.get(result.get('C_ALARMSOURCE')) in lcc_tracking_results_dict.get(test_name):
                    lcc_tracking_results_dict.get(test_name).remove(nh_lcc_dict.get(result.get('C_ALARMSOURCE')))

                if 'Success' in result.get('C_SUMMARY'):
                    nh_status_dict[test_name][nh_lcc_dict.get(result.get('C_ALARMSOURCE'))] = "success"
                elif 'Failure' in result.get('C_SUMMARY'):
                    nh_status_dict[test_name][nh_lcc_dict.get(result.get('C_ALARMSOURCE'))] = "failure"
                elif 'Comm Alarm' in result.get('C_SUMMARY'):
                    nh_status_dict[test_name][nh_lcc_dict.get(result.get('C_ALARMSOURCE'))] = "warning"
                else:
                    nh_status_dict[test_name][nh_lcc_dict.get(result.get('C_ALARMSOURCE'))] = ""

    for tracking_test_name, no_lcc_status_list in lcc_tracking_results_dict.items():
        for location in no_lcc_status_list:
            nh_status_dict.get(tracking_test_name)[location] = 'warning'

    with open(nh_status_path, 'w') as wfh:
        json.dump(nh_status_dict, wfh)

    return True


if __name__ == '__main__':
    main()
