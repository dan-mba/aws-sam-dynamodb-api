import boto3
import json
import os
from .get import get
from .response import respond

if not dynamodb:
  dynamodb = boto3.resource('dynamodb')

table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)


def lambda_handler(event, context):

  print("Received event: " + json.dumps(event, indent=2))

  """
  operations = {
    'DELETE': lambda dynamo, x: dynamo.delete_item(TableName=table_name, **x),
    'GET': lambda dynamo, x: dynamo.scan(TableName=table_name, **x) if x else dynamo.scan(TableName=table_name),
    'POST': lambda dynamo, x: dynamo.put_item(TableName=table_name, **x),
    'PUT': lambda dynamo, x: dynamo.update_item(TableName=table_name, **x),
  }
  """
  operations = {
    'GET': get,
  }

  operation = event['httpMethod']
  if operation in operations:
    operations[operation](table,event)
  else:
    return respond(ValueError('Unsupported method "{}"'.format(operation)))

  """
  if operation in operations:
    payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
    return respond(None, operations[operation](dynamo, payload))
  """
