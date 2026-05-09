import boto3
from datetime import datetime

ROLE_PERMISSIONS = {
    "admin": ["put_item", "get_item", "delete_item", "scan"],
    "reader": ["get_item", "scan"],
    "writer": ["put_item", "get_item"]
}

current_user = "othmane"
current_role = "reader"

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

table = dynamodb.Table("SecureStudents")


def log_action(action, status):
    with open("audit.log", "a", encoding="utf-8") as file:
        file.write(
            f"{datetime.now()} | user={current_user} | role={current_role} | action={action} | status={status}\n"
        )


def check_permission(action):
    if action not in ROLE_PERMISSIONS[current_role]:
        log_action(action, "DENIED")
        raise PermissionError(
            f"Accès refusé : le rôle '{current_role}' ne peut pas effectuer '{action}'"
        )
    log_action(action, "AUTHORIZED")


def read_student(student_id):
    check_permission("get_item")
    response = table.get_item(Key={"student_id": student_id})
    return response.get("Item")


def delete_student(student_id):
    check_permission("delete_item")
    table.delete_item(Key={"student_id": student_id})


print("=== Démonstration de sécurité DynamoDB locale ===")
print("Utilisateur :", current_user)
print("Rôle :", current_role)

print("\n1. Lecture autorisée")
student = read_student("S001")
print(student)

print("\n2. Tentative de suppression")
delete_student("S001")