import boto3
from botocore.exceptions import ClientError
import json, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__)))
from lib.response import respond
from lib.table import setup_table

table = setup_table()

"""
DynamoDB return Numbers as Decimal
Convert rating to int for JSON Serialization
Convert skills Set to List for JSON Serialization
"""
def convert_item_json(db_item):
    db_item['rating'] = int(str(db_item['rating']))
    db_item['skills'] = list(db_item.get('skills',[]))
    db_item.pop('userid')


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

        try:
            response = table.get_item(Key={"userid": userid, "rating": rating})
            response = response.get('Item')

            if not response:
                response = {
                    "rating": rating,
                    "skills": []
                }
            else:
                convert_item_json(response)

        except ClientError as error:
            return respond(error.response['Error'])
        except Exception as error:
            return respond(str(error))

    else:
        try:
            key_expression = boto3.dynamodb.conditions.Key("userid").eq(userid)
            filter_expression = boto3.dynamodb.conditions.Attr("skills").size().gt(0)
            response = table.query(KeyConditionExpression=key_expression, FilterExpression=filter_expression)
            response = response['Items']
            for item in response:
                convert_item_json(item)

        except ClientError as error:
            return respond(error.response['Error'])
        except Exception as error:
            return respond(str(error))

    return respond(None, response)
  