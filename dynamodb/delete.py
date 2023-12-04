from json import loads
from sys import path
from os.path import join, dirname
from urllib.parse import unquote
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

path.append(join(dirname(__file__)))
from mylib.response import respond
from mylib.table import setup_table

table = setup_table()


def lambda_handler(event, context):
    userid = event['requestContext']['authorizer']['jwt']['claims']['username']
    name = event.get('pathParameters', {}).get('name')

    if not userid:
        return respond({
            'message': 'DELETE requires userid parameter'
        })

    if not name:
        return respond({
            'message': 'DELETE missing required parameter'
        })
    
    name = unquote(name);

    if name != 'ALL_SKILLS':
        try:
            table.delete_item(Key={'PK': userid, 'SK': name})
            response = {'message': 'Skill deleted', 'name': name }

        except ClientError as error:
            return respond(error.response['Error'])
        except Exception as error:
            return respond(str(error))

        return respond(None, response)

    try:
        expression = Key('PK').eq(userid)
        query_results = table.query(KeyConditionExpression=expression)

        with table.batch_writer() as batch:
            for item in query_results['Items']:
                batch.delete_item(
                    Key={'PK': userid, 'SK': item['SK']})

        response = {'message': 'deleted all skills for this user'}

    except ClientError as error:
        return respond(error.response['Error'])
    except Exception as error:
        return respond(str(error))

    return respond(None, response)
