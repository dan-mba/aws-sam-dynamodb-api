import boto3
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))
from methods.get import get
from methods.post import post
from methods.put import put
from methods.delete import delete
from lib.response import respond

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'Skills'
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    operations = {
        'GET': get,
        'POST': post,
        'PUT': put,
        'DELETE': delete
    }

    operation = event['httpMethod']
    if operation in operations:
        return operations[operation](table, event)

    return respond({
        'message': 'Unsupported method',
        'method': operation
    })
