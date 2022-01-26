from sys import path
from os.path import dirname, join
from functools import reduce
from collections import defaultdict
from boto3.dynamodb.conditions import Key, And
from botocore.exceptions import ClientError

path.append(join(dirname(__file__)))
from mylib.response import respond
from mylib.table import setup_table

table = setup_table()

"""
DynamoDB return Numbers as Decimal
Convert rating to int for JSON Serialization
Convert skills Set to List for JSON Serialization
"""


def lambda_handler(event, context):
    userid = event['requestContext']['authorizer']['jwt']['claims']['username']
    rating = event.get('pathParameters', {}).get('rating')

    if rating:
        try:
            rating = int(rating)
        except ValueError:
            return respond({'message': 'rating is not an integer', 'rating': rating})

        if rating not in range(1, 6):
            return respond({'message': 'rating is not between 1 and 5', 'rating': rating})

        expression = reduce(And, [Key('PK').eq(userid), Key('SK').begins_with(f'{rating}#')])

        try:
            items = table.query(KeyConditionExpression=expression)
            items = items['Items']

            skills = []
            if len(items) > 0:
                for item in items:
                    skills.append(item['SK'][2:])


            response = {}
            response[rating] = skills

        except ClientError as error:
            return respond(error.response['Error'])
        except Exception as error:
            return respond(str(error))

    else:
        try:
            key_expression = Key('PK').eq(userid)
            items = table.query(KeyConditionExpression=key_expression)
            items = items['Items']

            response = defaultdict(list)
            for item in items:
                rating = item['SK'][0]
                skill = item['SK'][2:]
                response[rating].append(skill)
            response = dict(response)

        except ClientError as error:
            return respond(error.response['Error'])
        except Exception as error:
            return respond(str(error))

    return respond(None, response)
  