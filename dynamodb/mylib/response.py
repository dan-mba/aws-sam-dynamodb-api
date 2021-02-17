import json


def respond(err, res=None):
    if err:
        body = json.dumps(err)
    else:
        body = json.dumps(res)

    return {
        'statusCode': '400' if err else '200',
        'body': body,
        'headers': {
            'Content-Type': 'application/json'
        },
    }
