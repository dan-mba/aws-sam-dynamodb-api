from json import dumps


def respond(err, res=None):
    if err:
        body = dumps(err)
    else:
        body = dumps(res)

    return {
        'statusCode': '400' if err else '200',
        'body': body,
        'headers': {
            'Content-Type': 'application/json'
        },
    }
