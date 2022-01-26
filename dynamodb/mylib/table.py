from boto3 import resource


def setup_table():
    # pylint: disable=invalid-name
    dynamodb = resource('dynamodb')
    TABLE_NAME = 'Skills'
    return dynamodb.Table(TABLE_NAME)
