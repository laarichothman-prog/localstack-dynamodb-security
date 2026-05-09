import boto3

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

table = dynamodb.create_table(
    TableName="SecureStudents",
    KeySchema=[
        {
            "AttributeName": "student_id",
            "KeyType": "HASH"
        }
    ],
    AttributeDefinitions=[
        {
            "AttributeName": "student_id",
            "AttributeType": "S"
        }
    ],
    BillingMode="PAY_PER_REQUEST"
)

table.wait_until_exists()

print("Table SecureStudents créée avec succès.")