import json

def respond(err, res=None):
  return {
    'statusCode': '400' if err else '200',
    'body': err.message if err else json.dumps(res),
    'headers': {
        'Content-Type': 'application/json',
    },
  }
