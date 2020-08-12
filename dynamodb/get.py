import boto3
import json
from .response import respond

def get(table, event):
  print("Get parameters:" + json.dumps(event['pathParameters']))
  respond(None,event['pathParameters'])
  