import json

def lambda_handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    return {
        'statusCode': 200,
        'body': 'Hello, CDK! You have hit {}\n'.format(event['path'])
    }