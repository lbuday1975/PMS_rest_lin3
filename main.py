import flask
import pms_db, pms_command

# lv_rc = pms_command.chk_connect()
print("RET: " + pms_command.get_sys_var('DB8', '\<DEF_HOST\>'))

# pms_db.get_syslist()
