from botocore.exceptions import ClientError
import json
from lib.response import respond

def post(table, event):
    if not event.get('body'):
        return respond({"message": "POST request requires parameters in the body"})

    try:
        body = json.loads(event['body'])
    except:
        return respond({
            "message": "POST request requires JSON parameters in the body",
            "body": event['body']
        })

    userid = body.get('userid')
    rating = body.get('rating')
    skill = body.get('skill')

    if (not userid) or (not rating) or (not skill):
        return respond({
            'message': 'POST missing required parameter',
            'userid': userid,
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
  