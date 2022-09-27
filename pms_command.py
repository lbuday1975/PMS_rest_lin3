import logging
import re
import subprocess as sp

DEBUG = True


# Check connection to PMS server
def chk_connect():
    lv_cmd = '/opt/PMS/bin/pms_commander_server.sh -c SYSTEM_LIST'
    lv_rc = 999

    lv_proc = sp.Popen([lv_cmd], stdout=sp.PIPE, shell=True)
    try:
        lv_out, lv_err = lv_proc.communicate()
        lv_rc = lv_proc.poll()
    except sp.CalledProcessError as lv_ex:
        print("ERROR: " + lv_ex.output.decode())
        lv_rc = 999

    return lv_rc


def get_sys_var(la_sys_name, la_sys_var):
    lv_cmd = f'/opt/PMS/bin/pms_commander_server.sh -c GET_VARIABLE -SYS_NAME {la_sys_name} -VAR_NAME {la_sys_var}'
    lv_proc = sp.Popen([lv_cmd], stdout=sp.PIPE, shell=True)
    lv_rc = "ERROR"
    try:
        lv_out, lv_err = lv_proc.communicate()
        lv_rc = str(lv_proc.poll())
    except sp.CalledProcessError as lv_ex:
        print("ERROR: " + lv_ex.output.decode())
        lv_out = ""
        lv_rc = "ERROR"

    for lv_line in lv_out.splitlines():
        if re.search("VALUE", lv_line.decode()):
            if DEBUG:
                print("DEBUG = " + str(logging.DEBUG))
                print(str(lv_line.decode().split(':')))
            lv_rc = str(lv_line.decode().split(':')[1])

    return lv_rc


def set_sys_var(la_sys_name, la_sys_var, la_value):
    lv_rc = 999
    lv_cmd = f'/opt/PMS/bin/pms_commander_server.sh -c SET_VARIABLE -SYS_NAME {la_sys_name} -VAR_NAME {la_sys_var} -VALUE {la_value}'
    lv_proc = sp.Popen([lv_cmd], stdout=sp.PIPE, shell=True)
    try:
        lv_out, lv_err = lv_proc.communicate()
        lv_rc = str(lv_proc.poll())
    except sp.CalledProcessError as lv_ex:
        print("ERROR: " + lv_ex.output.decode())
        lv_rc = 999

    return lv_rc


def start_cmd(la_sys_name, la_proc_name, la_param):
    lv_rc = 999

    if la_param == '-' or la_param == "None":
        lv_cmd_add = ""
    else:
        lv_cmd_add = f"-P \"{la_param}\""

    lv_cmd = f'/opt/PMS/bin/pms_commander_server.sh -c START_COMMAND -SYS_NAME "{la_sys_name}" -t "{la_proc_name}" ' + lv_cmd_add
    print("--> CMD: " + lv_cmd)
    lv_proc = sp.Popen([lv_cmd], stdout=sp.PIPE, shell=True)
    try:
        lv_out, lv_err = lv_proc.communicate()

        for lv_line in lv_out.splitlines():
            if DEBUG:
                print(lv_line.decode())
                if lv_line.decode().find("Start date:") != -1:
                    lv_sdate = lv_line.decode().split(": ",1)
                if lv_line.decode().find("Start time:") != -1:
                    lv_stime = lv_line.decode().split(": ", 1)
                if lv_line.decode().find("Duration:") != -1:
                    lv_duration = lv_line.decode().split(": ", 1)


        lv_rc = "{'RC':" + str(lv_proc.poll()) + ", 'SDATE': '" + lv_sdate[1] + "', 'STIME': '" + lv_stime[1] + "', 'DURATION': '" + lv_duration[1] + "'} \n"
    except sp.CalledProcessError as lv_ex:
        print("ERROR: " + lv_ex.output.decode())
        lv_rc = 999

    return lv_rc