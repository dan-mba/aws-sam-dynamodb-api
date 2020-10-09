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
        return respond({"message": "POST request requires parameters in the body"})

    try:
        body = json.loads(event['body'])
    except:
        return respond({
            "message": "POST request requires JSON parameters in the body",
            "body": event['body']
        })

    userid = event['requestContext']['authorizer']['jwt']['claims']['username']
    rating = body.get('rating')
    skill = body.get('skill')

    if (not rating) or (not skill):
        return respond({
            'message': 'POST missing required parameter',
            'rating': rating,
            'skill': skill
        })

    try:
        rating = int(rating)
    except ValueError:
        return respond({'message': 'rating is not an integer', 'rating': rating})

    if rating not in range(1, 6):
        return respond({'message': 'rating is not between 1 and 5', 'rating': rating})

    try:
        table.update_item(Key={'userid': userid, 'rating': rating},
                          UpdateExpression='ADD skills :skill',
                          ExpressionAttributeValues={':skill': set([skill])})
        response = {'message': 'Skill added'}

    except ClientError as error:
        return respond(error.response['Error'])
    except Exception as error:
        return respond(str(error))

    return respond(None, response)
  