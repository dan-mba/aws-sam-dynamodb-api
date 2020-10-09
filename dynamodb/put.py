import json
import sys
import os
from botocore.exceptions import ClientError

sys.path.append(os.path.join(os.path.dirname(__file__)))
from mylib.response import respond
from mylib.table import setup_table

table = setup_table()

def lambda_handler(event, context):
    if not event.get('body'):
        return respond({"message": "PUT request requires parameters in the body"})

    try:
        body = json.loads(event['body'])
    except:
        return respond({
            "message": "PUT request requires JSON parameters in the body",
            "body": event['body']
        })


    userid = event['requestContext']['authorizer']['jwt']['claims']['username']
    oldrating = body.get('oldrating')
    newrating = body.get('newrating')
    skill = body.get('skill')

    if (not userid) or (not oldrating) or (not newrating) or (not skill):
        return respond({
            'message': 'POST missing required parameter',
            'oldrating': oldrating,
            'newrating': newrating,
            'skill': skill
        })

    try:
        oldrating = int(oldrating)
    except ValueError:
        return respond({'message': 'oldrating is not an integer', 'oldrating': oldrating})

    try:
        newrating = int(newrating)
    except ValueError:
        return respond({'message': 'newrating is not an integer', 'newrating': newrating})

    if oldrating not in range(1, 6):
        return respond({'message': 'oldrating is not between 1 and 5', 'oldrating': oldrating})

    if newrating not in range(1, 6):
        return respond({'message': 'newrating is not between 1 and 5', 'newrating': newrating})

    try:
        table.update_item(Key={'userid': userid, 'rating': oldrating},
                          UpdateExpression='DELETE skills :skill',
                          ExpressionAttributeValues={':skill': set([skill])})
        table.update_item(Key={'userid': userid, 'rating': newrating},
                          UpdateExpression='ADD skills :skill',
                          ExpressionAttributeValues={':skill': set([skill])})
        response = {'message': 'Skill updated'}

    except ClientError as error:
        return respond(error.response['Error'])
    except Exception as error:
        return respond(str(error))

    return respond(None, response)
  