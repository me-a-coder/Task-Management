import json
import logging
import boto3
import jwt
from jwt import InvalidTokenError
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Tasks')

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")

    try:
        if 'headers' not in event or 'Authorization' not in event['headers']:
            raise KeyError("Authorization header is missing")

        auth_header = event['headers']['Authorization']
        token = auth_header.split()[1]
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        user_id = decoded_token['sub']

        logger.info(f"Get tasks request received for user: {user_id}")

        response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id)
        )

        tasks = response.get('Items', [])

        logger.info(f"Retrieved {len(tasks)} tasks for user: {user_id}")
        return {
            'statusCode': 200,
            'body': json.dumps(tasks)
        }
    except KeyError as e:
        logger.error(f"Unauthorized - {str(e)}")
        return {
            'statusCode': 401,
            'body': json.dumps({'error': 'Unauthorized - Unable to extract user ID'})
        }
    except InvalidTokenError as e:
        logger.error(f"Unauthorized - Invalid token: {str(e)}")
        return {
            'statusCode': 401,
            'body': json.dumps({'error': 'Unauthorized - Invalid token'})
        }
    except Exception as e:
        logger.error(f"Error retrieving tasks: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
