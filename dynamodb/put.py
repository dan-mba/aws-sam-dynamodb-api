from json import loads
from sys import path
from os.path import join, dirname
from functools import reduce
from boto3.dynamodb.conditions import Key, And
from botocore.exceptions import ClientError

path.append(join(dirname(__file__)))
from mylib.response import respond
from mylib.table import setup_table

table = setup_table()
def lambda_handler(event, context):
    if not event.get('body'):
        return respond({"message": "PUT request requires parameters in the body"})

    try:
        body = loads(event['body'])
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

    sk_old = f'{oldrating}#{skill}'
    sk_new = f'{newrating}#{skill}'
    keycondition = reduce(And, [Key('PK').eq(userid), Key('SK').eq(sk_old)])

    try:
        response = table.query(KeyConditionExpression=keycondition)
        response = response['Items']
        if len(response) == 0:
            return respond({'message': 'Skill does not exist with this rating'})

        table.delete_item(Key={'PK': userid, 'SK': sk_old})
        table.put_item(Item={'PK': userid, 'SK': sk_new})
        response = {'message': 'Skill updated'}

    except ClientError as error:
        return respond(error.response['Error'])
    except Exception as error:
        return respond(str(error))

    return respond(None, response)
  