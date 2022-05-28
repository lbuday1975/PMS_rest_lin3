import logging
import re
import subprocess as sp

DEBUG = False


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
    lv_txt = {"CHK_RC": -1}
    lv_txt["VAR_VALUE"] = "-"

    try:
        lv_out, lv_err = lv_proc.communicate()
        lv_txt["CHK_RC"] = str(lv_proc.poll())
    except sp.CalledProcessError as lv_ex:
        print("ERROR: " + lv_ex.output.decode())
        lv_out = ""
        lv_txt["CHK_RC"] = 2

    for lv_line in lv_out.splitlines():
        if re.search("VALUE", lv_line.decode()):
            if DEBUG:
                print("DEBUG = " + str(logging.DEBUG))
                print(str(lv_line.decode().split(':')))

            # lv_txt["CHK_RC"] = 0
            lv_txt["VAR_VALUE"] = str(lv_line.decode().split(':')[1])

    return lv_txt


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
                print(str(lv_line.decode()))

        lv_rc = str(lv_proc.poll())
    except sp.CalledProcessError as lv_ex:
        print("ERROR: " + lv_ex.output.decode())
        lv_rc = 999

    return lv_rc


def check_cmd(la_sys_name, la_proc_name):
    lv_rc = 999
    lv_txt = {"CHK_RC": -1}

    lv_cmd = f'/opt/PMS/bin/pms_commander_server.sh -c COMMAND_STATUS -SYS_NAME "{la_sys_name}" -t "{la_proc_name}" '
    print("--> CMD_CHK: " + lv_cmd)
    lv_proc = sp.Popen([lv_cmd], stdout=sp.PIPE, shell=True)
    try:
        lv_out, lv_err = lv_proc.communicate()

        lv_param_first = 0
        for lv_line in lv_out.splitlines():
            if str(lv_line.decode()).startswith("  Parameters"):
                lv_param_first = lv_param_first + 1

            if lv_param_first == 1:
                if str(lv_line.decode()).startswith("    Process:"):
                    lv_txt["PROC_NAME"] = str(lv_line.decode()).replace("    Process: ", "")
                if str(lv_line.decode()).startswith("    Start date:"):
                    lv_txt["PROC_START_DATE"] = str(lv_line.decode()).replace("    Start date: ", "")
                if str(lv_line.decode()).startswith("    Start time:"):
                    lv_txt["PROC_START_TIME"] = str(lv_line.decode()).replace("    Start time: ", "")
                if str(lv_line.decode()).startswith("    Duration:"):
                    lv_txt["PROC_DURATION"] = str(lv_line.decode()).replace("    Duration: ", "")
                if str(lv_line.decode()).startswith("    Result:"):
                    lv_txt["PROC_RC"] = str(lv_line.decode()).replace("    Result: ", "")

            # Check if running
            if str(lv_line.decode()).startswith("Running:"):
                lv_running = str(lv_line.decode()).replace("Running: ", "")
                if lv_running == "false":
                    lv_txt["RUNNING"] = False
                else:
                    lv_txt["RUNNING"] = True

            # Check if suppressed
            if str(lv_line.decode()).startswith("Suppressed:"):
                lv_running = str(lv_line.decode()).replace("Suppressed: ", "")
                if lv_running == "false":
                    lv_txt["SUPPRESSED"] = False
                else:
                    lv_txt["SUPPRESSED"] = True

            if DEBUG:
                print("DEBUG: " + str(lv_line.decode()))

        lv_rc = str(lv_proc.poll())
        lv_txt["CHK_RC"] = lv_rc
    except sp.CalledProcessError as lv_ex:
        print("ERROR: " + lv_ex.output.decode())
        lv_rc = 999
        lv_txt["CHK_RC"] = 999

    return lv_rc, lv_txt
