from common.common import Common
import cx_Oracle
import os
import json
import time
import datetime
import sys

from core.network_health_base import NhBase
from core.query_oracle import QueryOracle


def main():
    """
    
    :return: 
    """

    # carrier_smtp_syntax = dict(att='mms.att.net', verizon='vtext.com', uscc='email.uscc.net')

    # svt_rc, svt_dict = Common.read_json_file('svt_tests')
    # if svt_rc:
    #     for test_name in svt_dict.get('test_names'):
    #         print(test_name)

    nh_base = NhBase()
    nh_base.establish_logging(logger_config_json=nh_base.neh_log_config_file)

    if nh_base.exec_env == 'dev':
        nh_status_path = os.environ.get('neh_status')
        nh_lcc_map_path = os.environ.get('neh_lcc_map')
    else:
        nh_status_path = '/neh_status_files/neh_status/neh_test_status'
        nh_lcc_map_path = '/neh_status_files/neh_lcc_config'

    nh_status_rc, nh_status_dict = Common.read_json_file(nh_status_path)
    nh_lcc_rc, nh_lcc_dict = Common.read_json_file(nh_lcc_map_path)
    if not nh_status_rc:
        nh_base.nh_logger.critical("Network Health Status file couldn't be obtained. Path specified: {}".format(nh_status_path))
        return False

    if not nh_lcc_rc:
        nh_base.nh_logger.critical("Network Health LCC configuration map file couldn't be obtained. Path specified: {}".format(nh_lcc_map_path))
        return False

    netcool_db = QueryOracle()
    con = cx_Oracle.connect("automation_ro/automation_ro@shracdev-scan.uscc.com:1521/netcoold")

    cursor = con.cursor()

    cursor.execute("""SELECT c_alarmsource, c_lastoccurrence, c_summary, c_alertkey, c_suppressescl, c_ttnumber 
    FROM netcoold.alerts_status_t WHERE c_lastoccurrence > (SYSTIMESTAMP - .0833) 
    AND c_alertgroup = 'ASCOM Availibility Alarms' ORDER BY 1,4,2 """)

    # Get all the column names for the result set
    column_name_list = [x[0] for x in cursor.description]

    # Join the column names and the data for each row into a dictionary for easier processing.
    result_dicts = [dict(zip(column_name_list, row)) for row in cursor.fetchall()]

    # return False
    # result_dicts = [dict(zip(column_name_list, cursor.fetchone()))]

    # Initialize a dictionary of lists by SVT test name that contains list of LCCs. These lists are used to keep track
    # of what LCCs we updated by removing the LCC for the SVT test name in the result set. At the end of processing the
    # result set any LCCs that didn't get their status updated will be left in the lists and are assumed to have a
    # "COMM AlARM" status that indicates the test didn't run within the last hour. In the status config dictionary this
    # will be replaced with a 'warning' status.
    lcc_tracking_results_dict = dict()
    for test_name in nh_status_dict.keys():
        if test_name != 'last_refreshed':
            temp_list = []
            for lcc in nh_lcc_dict.values():
                if lcc_tracking_results_dict.get(test_name) is None:
                    temp_list.append(lcc)
                    lcc_tracking_results_dict[test_name] = temp_list
                else:
                    if lcc not in lcc_tracking_results_dict.get(test_name):
                        lcc_tracking_results_dict.get(test_name).append(lcc)

    for test_name in nh_status_dict.keys():
        for result in result_dicts:
            if test_name in result.get('C_ALERTKEY'):
                if result.get('C_ALARMSOURCE') in nh_lcc_dict.keys():
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

    nh_status_dict['last_refreshed'] = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    with open(nh_status_path, 'w') as wfh:
        json.dump(nh_status_dict, wfh)
        print("status file updated")

    # time.sleep(300)
    return True


if __name__ == '__main__':
    rc = main()
    if rc:
        sys.exit(0)
    else:
        sys.exit(False)
