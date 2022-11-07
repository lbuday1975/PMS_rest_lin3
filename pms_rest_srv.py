from flask import Flask, request

import pms_command
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'commander':
        return 'pYth0FF1199'
    return None


@auth.error_handler
def unauthorized():
    return {'error': 'Unauthorized access'}


# lv_rc = pms_command.chk_connect()
# print("RET: " + pms_command.get_sys_var('DB8', '\<DEF_HOST\>'))
# print("Change to proc rc:" + str(pms_command.set_sys_var('DB8', '\<DEF_HOST\>', 'p1-lnw_OK')))
# print("RET: " + pms_command.get_sys_var('DB8', '\<DEF_HOST\>'))
# pms_db.get_syslist()

app = Flask(__name__)


@app.route("/api/get_var", methods=['POST', 'GET'])
@auth.login_required
def get_var():
    lv_grc = ""
    if request.method == 'POST':
        ls_sys_name = request.args.get('sys_name')
        ls_var_name = request.args.get('var_name')
        lv_rc = pms_command.chk_connect()
        if lv_rc == 0:
            print(f'ACT: get variable value to {ls_sys_name}-{ls_var_name}')
            print("--> RET: " + pms_command.get_sys_var(f'{ls_sys_name}', f'\<{ls_var_name}\>'))
            lv_grc = 0
        else:
            print("PMS server connection ERROR")
            lv_grc = "PMS server connection ERROR"

    return str(lv_grc)


@app.route("/api/start_cmd", methods=['POST'])
@auth.login_required
def api_start_cmd():
    lv_grc = "PMSRC:-1"
    lv_grc_cmd = ""
    if request.method == 'POST':
        ls_sys_name = request.args.get('sys_name')
        ls_proc_name = request.args.get('proc_name')
        ls_param = request.args.get('param')
        if ls_param == None:
            ls_param = "-"
        lv_rc = pms_command.chk_connect()
        if lv_rc == 0:
            print(f'Act: start command: {ls_sys_name}-{ls_proc_name} with parameter: {ls_param}')
            lv_grc_cmd = pms_command.start_cmd(f'{ls_sys_name}', f'{ls_proc_name}', f'{ls_param}')
            # lv_grc = "PMSRC:" + str(pms_command.start_cmd(f'{ls_sys_name}', f'{ls_proc_name}', f'{ls_param}'))
            print("--> Return : " + lv_grc_cmd)
            if lv_grc_cmd == "2":
                lv_grc = "PMSRC:2"
            else:
                lv_grc = lv_grc_cmd + "PMSRC:0"
        else:
            print("PMS server connection ERROR")
            lv_grc = "PMSRC:3"
    else:
        print("GET method call : NO action")
        lv_grc = "PMSRC:4"

    return str(lv_grc)


@app.route("/api/start_cmd_async", methods=['POST'])
@auth.login_required
def api_start_async_cmd():
    lv_grc = "PMSRC:-1"
    if request.method == 'POST':
        ls_sys_name = request.args.get('sys_name')
        ls_proc_name = request.args.get('proc_name')
        ls_param = request.args.get('param')
        if ls_param == None:
            ls_param = "-"
        lv_rc = pms_command.chk_connect()
        if lv_rc == 0:
            print(f'Act: start command: {ls_sys_name}-{ls_proc_name} with parameter: {ls_param}')
            lv_grc = "PMSRC:" + str(pms_command.start_cmd_async(f'{ls_sys_name}', f'{ls_proc_name}', f'{ls_param}'))
            print("--> RC : " + lv_grc)
        else:
            print("PMS server connection ERROR")
            lv_grc = "PMSRC:3"
    else:
        print("GET method call : NO action")
        lv_grc = "PMSRC:4"

    return str(lv_grc + "\n")


@app.route("/api/check_cmd", methods=['GET'])
@auth.login_required
def api_check_cmd():
    lv_grc = "PMSRC:-1"
    lv_grc_cmd = ""
    if request.method == 'GET':
        ls_sys_name = request.args.get('sys_name')
        ls_proc_name = request.args.get('proc_name')

        # Check if server live
        lv_rc = pms_command.chk_connect()
        if lv_rc == 0:
            print(f'Act: check command: {ls_sys_name}-{ls_proc_name} last run')
            lv_grc_cmd = pms_command.check_cmd(f'{ls_sys_name}', f'{ls_proc_name}')
            print("--> Return : " + lv_grc_cmd)
            if lv_grc_cmd == "2":
                lv_grc = "PMSRC:2"
            else:
                lv_grc = lv_grc_cmd + "PMSRC:0"
        else:
            print("PMS server connection ERROR")
            lv_grc = "PMSRC:3"
    else:
        print("GET method call : NO action")
        lv_grc = "PMSRC:4"

    return str(lv_grc)


@app.route("/api/set_var", methods=['POST'])
@auth.login_required
def api_set_var():
    lv_grc = -1
    if request.method == 'POST':
        ls_sys_name = request.args.get('sys_name')
        ls_var_name = request.args.get('var_name')
        ls_var_value = request.args.get('var_value')
        lv_rc = pms_command.chk_connect()
        if lv_rc == 0:
            print(f'Act: set variable value to {ls_sys_name}-{ls_var_name} value: {ls_var_value}')
            print("--> RC : " + str(pms_command.set_sys_var(f'{ls_sys_name}', f'\<{ls_var_name}\>', f'{ls_var_value}')))
            print("--> RET: " + pms_command.get_sys_var(f'{ls_sys_name}', f'\<{ls_var_name}\>'))
            lv_grc = 0
        else:
            print("PMS server connection ERROR")
            lv_grc = "PMS server connection ERROR"
    else:
        print("GET method call : NO action")
        lv_grc = "GET method call : NO action"

    return str(lv_grc)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
