import re
import subprocess as sp


# Check connection to PMS server
def chk_connect():
    lv_cmd = '/opt/PMS/bin/pms_commander_server.sh -c SYSTEM_LIST'
    lv_rc = -1

    lv_proc = sp.Popen([lv_cmd], stdout=sp.PIPE, shell=True)
    try:
        lv_out, lv_err = lv_proc.communicate()
        lv_rc = lv_proc.poll()
    except sp.CalledProcessError as lv_ex:
        print("ERROR: " + lv_ex.output.decode())
        lv_rc = 9

    return lv_rc


def get_sys_var(la_sys_name, la_sys_var):
    lv_cmd = f'/opt/PMS/bin/pms_commander_server.sh -c GET_VARIABLE -SYS_NAME {la_sys_name} -VAR_NAME {la_sys_var}'
    lv_proc = sp.Popen([lv_cmd], stdout=sp.PIPE, shell=True)
    try:
        lv_out, lv_err = lv_proc.communicate()
        lv_rc = str(lv_proc.poll())
    except sp.CalledProcessError as lv_ex:
        print("ERROR: " + lv_ex.output.decode())
        lv_rc = "9"

    for lv_line in lv_out.splitlines():
        if re.search("VALUE", lv_line.decode()):
            print(str(lv_line.decode().split(':')))
            lv_rc = str(lv_line.decode().split(':')[1])

    return lv_rc
