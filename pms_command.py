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
                    lv_sdate = lv_line.decode().split(":",1)
                if lv_line.decode().find("Start time:") != -1:
                    lv_stime = lv_line.decode().split(":", 1)
                if lv_line.decode().find("Duration:") != -1:
                    lv_duration = lv_line.decode().split(":", 1)

        if lv_proc.poll() == 0:
            lv_rc = "{'RC':" + str(lv_proc.poll()) + ",'SDATE':'" + lv_sdate[1] + "','STIME':'" + lv_stime[1] + "','DURATION':'" + lv_duration[1] + "'} \n"
        else:
            lv_rc = str(lv_proc.poll())
    except sp.CalledProcessError as lv_ex:
        print("ERROR: " + lv_ex.output.decode())
        lv_rc = 999

    return lv_rc


def start_cmd_async(la_sys_name, la_proc_name, la_param):
    lv_rc = 999

    if la_param == '-' or la_param == "None":
        lv_cmd_add = " -ASYNC true"
    else:
        lv_cmd_add = f"-P \"{la_param}\" -ASYNC true"

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

    lv_cmd = f'/opt/PMS/bin/pms_commander_server.sh -c COMMAND_STATUS -i "{la_sys_name}" -t "{la_proc_name}"'
    print("--> CMD: " + lv_cmd)
    lv_proc = sp.Popen([lv_cmd], stdout=sp.PIPE, shell=True)
    try:
        lv_out, lv_err = lv_proc.communicate()
        lv_sdate="-"
        lv_stime="-"
        lv_duration="-"
        lv_result="-"
        lv_suppress="-"
        lv_running = "-"
        for lv_line in lv_out.splitlines():
            if DEBUG:
                print(lv_line.decode())
                if lv_line.decode().find("Start date:") != -1:
                    if lv_sdate == "-":
                        lv_sdate = lv_line.decode().split(":",1)
                if lv_line.decode().find("Start time:") != -1:
                    if lv_stime == "-":
                        lv_stime = lv_line.decode().split(":", 1)
                if lv_line.decode().find("Duration:") != -1:
                    if lv_duration == "-":
                        lv_duration = lv_line.decode().split(":", 1)
                if lv_line.decode().find("Result:") != -1:
                    if lv_result == "-":
                        lv_result = lv_line.decode().split(":", 1)
                else:
                    lv_result = ['Result', '-2']
                if lv_line.decode().find("Suppressed:") != -1:
                    if lv_suppress == "-":
                        lv_suppress = lv_line.decode().split(":", 1)
                if lv_line.decode().find("Running:") != -1:
                    if lv_running == "-":
                        lv_running = lv_line.decode().split(":", 1)

        if lv_proc.poll() == 0:
            if str(lv_running[1]) == ' true':
                if DEBUG: print(str(lv_result) + "__" + str(lv_running) + "__" + str(lv_suppress) + "__" + str(lv_sdate) + "__" + str(lv_stime))
                lv_rc = "{'RC':" + lv_result[1] + ",'RUNNING':" + lv_running[1] + ",'SUPPRESSED':" + lv_suppress[1] + ",'SDATE':'" + lv_sdate[1] + "','STIME':'" + lv_stime[1] + "','DURATION':'-'} \n"
            else:
                lv_rc = "{'RC':" + lv_result[1] + ",'RUNNING':" + lv_running[1] + ",'SUPPRESSED':" + lv_suppress[1] + ",'SDATE':'" + lv_sdate[1] + "','STIME':'" + lv_stime[1] + "','DURATION':'" + lv_duration[1] + "'} \n"
        else:
            lv_rc = str(lv_proc.poll())
    except sp.CalledProcessError as lv_ex:
        print("ERROR: " + lv_ex.output.decode())
        lv_rc = 999

    return lv_rc