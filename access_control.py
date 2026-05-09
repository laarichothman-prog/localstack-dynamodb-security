import boto3

ROLE_PERMISSIONS = {
    "admin": ["put_item", "get_item", "delete_item", "scan"],
    "reader": ["get_item", "scan"],
    "writer": ["put_item", "get_item"]
}

current_role = "admin"

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

table = dynamodb.Table("SecureStudents")


def check_permission(action):
    if action not in ROLE_PERMISSIONS[current_role]:
        raise PermissionError(
            f"Accès refusé : le rôle '{current_role}' n'a pas la permission '{action}'"
        )


def read_student(student_id):
    check_permission("get_item")

    response = table.get_item(
        Key={"student_id": student_id}
    )

    return response.get("Item")


def add_student(student_id, name, level, email):
    check_permission("put_item")

    table.put_item(
        Item={
            "student_id": student_id,
            "name": name,
            "level": level,
            "email": email
        }
    )

    print("Étudiant ajouté avec succès.")


def delete_student(student_id):
    check_permission("delete_item")

    table.delete_item(
        Key={"student_id": student_id}
    )

    print("Étudiant supprimé avec succès.")


print("Rôle actuel :", current_role)

print("Lecture autorisée :")
student = read_student("S001")
print(student)

print("Tentative de suppression :")
delete_student("S001")