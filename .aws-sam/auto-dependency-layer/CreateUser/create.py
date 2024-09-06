import json
import boto3
import os

region_name = os.environ["REGION_NAME"]
table_name = os.environ["TABLE_NAME"]
client = boto3.client("dynamodb")

# Look for user in dynamodb
def lookup_user(email):
  response = client.get_item(
    Key={
      'email': {
        'S': email
      }
    },
    TableName=table_name
  )
  print(response)
  
def handle_creation(event):
  user_exists = lookup_user(event["user"]["email"])

def lambda_handler(event, context):
  try:
    new_user = handle_creation(event)
  
    return {
      "statusCode": 200,
      "body": json.dumps({
        "message": "user created successfully"
      })
    }
  except KeyError as e:
    return {
      "statusCode": 500,
      "body": json.dumps({
        "message": f"missing key {e}"
      })
    }
