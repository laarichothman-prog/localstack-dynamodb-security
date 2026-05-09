import boto3
from cryptography.fernet import Fernet

# Génération de la clé
key = Fernet.generate_key()

cipher = Fernet(key)

# Connexion DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

table = dynamodb.Table("SecureStudents")

# Donnée sensible
email = "othmane@example.com"

# Chiffrement
encrypted_email = cipher.encrypt(email.encode()).decode()

# Insertion dans DynamoDB
table.put_item(
    Item={
        "student_id": "S002",
        "name": "Mohamed",
        "level": "IACS",
        "email": encrypted_email
    }
)

print("Email chiffré :")
print(encrypted_email)

# Lecture des données
response = table.get_item(
    Key={"student_id": "S002"}
)

stored_email = response["Item"]["email"]

# Déchiffrement
decrypted_email = cipher.decrypt(
    stored_email.encode()
).decode()

print("\nEmail déchiffré :")
print(decrypted_email)