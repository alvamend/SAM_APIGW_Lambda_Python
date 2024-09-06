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
  
  if "Item" in response:
    raise Exception("user already exists")
  
def handle_creation(event):
  body = json.loads(event["body"])
  
  # Validate if user exists
  lookup_user(body["user"]["email"])
  user_created = client.put_item(
    Item={
      'FirstName': {
        'S': body["user"]["first_name"]
      },
      'LastName': {
        'S': body["user"]["last_name"]
      },
      'email': {
        'S': body["user"]["email"]
      }
    },
    TableName=table_name
  )
  
  return True if user_created else False

def lambda_handler(event, context):
  try:
    new_user = handle_creation(event)
  
    if(new_user):
      return {
      "statusCode": 200,
      "body": json.dumps({
        "message": "user created successfully"
      })
    }
  except KeyError as e:
    print(f"missing key {e}")
    return {
      "statusCode": 500,
      "body": json.dumps({
        "message": f"missing key {e}"
      })
    }
  except Exception as e:
    print(str(e))
    return {
      "statusCode": 422,
      "body": json.dumps({
        "message": str(e)
      })
    }
