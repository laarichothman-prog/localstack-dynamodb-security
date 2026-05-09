import boto3

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

table = dynamodb.Table("SecureStudents")

response = table.get_item(
    Key={
        "student_id": "S001"
    }
)

print(response["Item"])