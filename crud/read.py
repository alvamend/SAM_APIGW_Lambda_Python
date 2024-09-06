import os
import boto3
import json

client = boto3.client('dynamodb')
table_name = os.environ["TABLE_NAME"]
region = os.environ["REGION_NAME"]

def lookup_user(email):
  response = client.get_item(
    Key={
      'email': {
        'S': email
      }
    },
    TableName=table_name
  )
  if 'Item' in response:
    return response["Item"]
  else:
    return False
    

def lambda_handler(event, context):
  try:
    email = event["queryStringParameters"]["email"]
    user_found = lookup_user(email)
    
    if(user_found):
      return{
        "statusCode": 200,
        "body": json.dumps({
          "user": user_found
        })
      }
    else:
      return{
        "statusCode": 404,
        "body": json.dumps({
          "message": "user not found"
        })
      }
    
  except KeyError as e:
    print(f"missing key {e}")
  except Exception as e:
    return{
      "statusCode": 422,
      "body": json.dumps({
        "message": str(e)
      })
    }
