import boto3

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

table = dynamodb.Table("SecureStudents")

table.put_item(
    Item={
        "student_id": "S001",
        "name": "Othmane",
        "level": "IACS",
        "email": "othmane@example.com"
    }
)

print("Étudiant ajouté avec succès.")