import uuid
from datetime import datetime
from flask import Flask, request, jsonify
import boto3

from config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_DEFAULT_REGION,
    DYNAMODB_ENDPOINT
)
from crypto_utils import encrypt_text, decrypt_text

app = Flask(__name__)

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=DYNAMODB_ENDPOINT,
    region_name=AWS_DEFAULT_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

records_table = dynamodb.Table("SecureRecords")
audit_table = dynamodb.Table("AuditLogs")

USERS = {
    "admin-token": "admin",
    "reader-token": "reader"
}

def get_role_from_token():
    token = request.headers.get("X-API-KEY")
    return USERS.get(token)

def write_audit(action, status, details=""):
    audit_table.put_item(
        Item={
            "log_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "status": status,
            "details": details
        }
    )

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"message": "API is running"}), 200

@app.route("/records", methods=["POST"])
def create_record():
    role = get_role_from_token()
    if role != "admin":
        write_audit("CREATE_RECORD", "DENIED", "Unauthorized create attempt")
        return jsonify({"error": "Access denied"}), 403

    data = request.json
    record_id = str(uuid.uuid4())

    encrypted_secret = encrypt_text(data["secret_data"])

    item = {
        "id": record_id,
        "owner": data["owner"],
        "category": data["category"],
        "secret_data": encrypted_secret,
        "created_at": datetime.utcnow().isoformat()
    }

    records_table.put_item(Item=item)
    write_audit("CREATE_RECORD", "SUCCESS", f"Record {record_id} created")

    return jsonify({
        "message": "Record created successfully",
        "id": record_id
    }), 201

@app.route("/records/<record_id>", methods=["GET"])
def get_record(record_id):
    role = get_role_from_token()
    if role not in ["admin", "reader"]:
        write_audit("READ_RECORD", "DENIED", "Unauthorized read attempt")
        return jsonify({"error": "Access denied"}), 403

    response = records_table.get_item(Key={"id": record_id})
    item = response.get("Item")

    if not item:
        write_audit("READ_RECORD", "FAILED", f"Record {record_id} not found")
        return jsonify({"error": "Record not found"}), 404

    decrypted_secret = decrypt_text(item["secret_data"])

    write_audit("READ_RECORD", "SUCCESS", f"Record {record_id} read")
    return jsonify({
        "id": item["id"],
        "owner": item["owner"],
        "category": item["category"],
        "secret_data": decrypted_secret,
        "created_at": item["created_at"]
    }), 200

@app.route("/audit", methods=["GET"])
def get_audit_logs():
    role = get_role_from_token()
    if role != "admin":
        write_audit("READ_AUDIT", "DENIED", "Unauthorized audit access")
        return jsonify({"error": "Access denied"}), 403

    response = audit_table.scan()
    return jsonify(response.get("Items", [])), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)