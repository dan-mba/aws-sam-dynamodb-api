import boto3

def setup_table():
    # pylint: disable=invalid-name
    dynamodb = boto3.resource('dynamodb')
    TABLE_NAME = 'Skills'
    return dynamodb.Table(TABLE_NAME)
