import json
import sys
import os
import boto3
from botocore.exceptions import ClientError

sys.path.append(os.path.join(os.path.dirname(__file__)))
from mylib.response import respond
from mylib.table import setup_table

table = setup_table()


def lambda_handler(event, context):
    if not event.get('body'):
        return respond({"message": "DELETE request requires parameters in the body"})

    try:
        body = json.loads(event['body'])
    except:
        return respond({
            "message": "DELETE request requires JSON parameters in the body",
            "body": event['body']
        })

    userid = event['requestContext']['authorizer']['jwt']['claims']['username']
    rating = body.get('rating')
    skill = body.get('skill')
    confirm = body.get('confirm')

    if not userid:
        return respond({
            'message': 'DELETE requires userid parameter'
        })

    if not confirm:
        if (not rating) or (not skill):
            return respond({
                'message': 'DELETE missing required parameter',
                'rating': rating,
                'skill': skill,
                'confirm': confirm
            })

        try:
            rating = int(rating)
        except ValueError:
            return respond({'message': 'rating is not an integer', 'rating': rating})

        if rating not in range(1, 6):
            return respond({'message': 'rating is not between 1 and 5', 'rating': rating})

        try:
            table.update_item(
                Key={'userid': userid, 'rating': rating},
                UpdateExpression='DELETE skills :skill',
                ExpressionAttributeValues={':skill': set([skill])})
            response = {'message': 'Skill deleted'}

        except ClientError as error:
            return respond(error.response['Error'])
        except Exception as error:
            return respond(str(error))

        return respond(None, response)

    if confirm != "YES":
        return respond({
            'message': 'removing all skills for a user requires confirm set to YES'
        })

    try:
        expression = boto3.dynamodb.conditions.Key("userid").eq(userid)
        query_results = table.query(KeyConditionExpression=expression)

        with table.batch_writer() as batch:
            for item in query_results['Items']:
                batch.delete_item(
                    Key={'userid': userid, 'rating': item['rating']})

        response = {'message': 'deleted all skills for this user'}

    except ClientError as error:
        return respond(error.response['Error'])
    except Exception as error:
        return respond(str(error))

    return respond(None, response)
