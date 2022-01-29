from flask import Flask
import marshmallow, jsonify
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
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


@app.route("/get_var")
@auth.login_required
def get_var():
    print("kokokokk")
    return "Adom maar...."


if __name__ == "__main__":
    app.run(debug=True)