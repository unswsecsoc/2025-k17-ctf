from flask import Flask, request, abort, make_response, render_template
import time
import game_pb2
from hashlib import sha256
import hmac
import uuid
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024
SIGNING_KEY = os.environ["SIGNING_KEY"].encode()
FLAG = os.environ.get("FLAG", "K17{local_testing_flag}")


def parse_message(msg_type, msg_bytes_hex, sig_hex=None):
    msg = msg_type()
    try:
        msg_bytes = bytes.fromhex(msg_bytes_hex)
        msg.ParseFromString(msg_bytes)
        if sig_hex is None or verify(msg_bytes, sig_hex):
            return msg
    except Exception as e:
        print(e)
        abort(make_response(
            {"error": f"Got missing or invalid parameters when parsing {msg_type.__name__}"}, 400))
    abort(make_response(
        {"error": f"Invalid signature for {msg_type.__name__}"}, 400))


def sign(serialized_msg):
    return hmac.new(SIGNING_KEY, serialized_msg, sha256).hexdigest()


def verify(serialized_msg, sig):
    return sign(serialized_msg) == sig


@app.route('/register', methods=['POST'])
def register_account():
    data = request.json
    account_details = parse_message(
        game_pb2.AccountDetails, data.get("account_details"))
    registration_invite = parse_message(
        game_pb2.RegistrationInvite, data.get("registration_invite"))

    if registration_invite.expires_at < time.time():
        return {"error": "Expired invite"}, 400

    registration = game_pb2.Registration()
    registration.MergeFromString(registration_invite.SerializeToString())
    registration.MergeFromString(account_details.SerializeToString())
    # TODO: log the registration

    account_token = game_pb2.AccountToken()
    account_token.user_id = str(uuid.uuid4())
    account_token.username = registration.username
    account_token.is_verified = registration.is_verified
    account_token.is_admin = False

    serialized_token = account_token.SerializeToString()

    # TODO: save users in a database
    return {
        "token": serialized_token.hex(),
        "signature": sign(serialized_token)
    }


@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.json
    score = data.get('score')

    if not (score and isinstance(score, int)):
        return {"error": "score is required and must be an integer"}, 400

    account_token_sig = data.get("account_token_sig")
    if account_token_sig is None:
        return {"error": "Missing signature"}, 400
    account_token = parse_message(
        game_pb2.AccountToken, data.get("account_token"), account_token_sig)

    # TODO: implement verification
    if not account_token.is_verified:
        return {"error": "Account is unverified"}, 403

    score_entry = game_pb2.HighScore()
    score_entry.user_id = account_token.user_id
    score_entry.score = score
    score_entry.timestamp = int(time.time())

    serialized_score = score_entry.SerializeToString()

    # TODO: display scores on a leaderboard
    return {
        "score": serialized_score.hex(),
        "signature": sign(serialized_score)
    }


@app.route('/rename', methods=['POST'])
def update_username():
    data = request.json
    new_username = data.get('new_username')

    old_token = data.get("old_user_token")
    old_token_sig = data.get("old_user_token_sig")
    if old_token_sig is None:
        return {"error": "Missing signature"}, 400
    account_token = parse_message(
        game_pb2.AccountToken, old_token, old_token_sig)
    if not account_token.is_verified:
        return {"error": "Account is unverified"}, 403

    # preserve token history
    new_data = game_pb2.AccountToken()
    new_data.username = new_username
    new_data.is_admin = False
    serialized_token = bytes.fromhex(old_token)[:1024] + new_data.SerializePartialToString()

    return {
        "token": serialized_token.hex(),
        "signature": sign(serialized_token)
    }


@app.route('/admin/verify-connection', methods=['GET'])
def verify_connection():
    # implement 2FA using the admin's machine IP
    # even if the admin isn't on their main machine they can still get a connection
    # token from the server and send it to their device!!! i'm so smart!!!!!
    if request.remote_addr == "192.168.1.139":
        new_data = game_pb2.SecureConnectionDetails()
        new_data.is_local_ip = True
        new_data.id = str(uuid.uuid4())
        serialized_secure_connection_details = new_data.SerializePartialToString()

        return {
            "secure_connection_details": serialized_secure_connection_details.hex(),
            "signature": sign(serialized_secure_connection_details)
        }

    return {"error": "Connection is insecure"}, 401


@app.route('/admin', methods=['POST'])
def admin_flag():
    data = request.json

    account_token_sig = data.get("account_token_sig")
    secure_connection_details_sig = data.get('secure_connection_details_sig')
    if not (account_token_sig and secure_connection_details_sig):
        return {"error": "Missing signature"}, 400
    account_token = parse_message(
        game_pb2.AccountToken, data.get("account_token"), account_token_sig)
    secure_connection_details = parse_message(game_pb2.SecureConnectionDetails, data.get(
        "secure_connection_details"), secure_connection_details_sig)

    if not account_token.is_verified:
        return {"error": "Forbidden (unverified)"}, 403

    if not account_token.is_admin:
        return {"error": "Forbidden (non-admin account)"}, 403

    if not secure_connection_details.is_local_ip:
        return {"error": "Invalid secure connection verification"}, 403

    return {
        "flag": FLAG
    }


@app.route('/admin', methods=['GET'])
def admin_panel():
    return render_template("admin.html")


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/account', methods=['GET'])
def account():
    return render_template("account.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)
