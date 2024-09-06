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
        logger.info(f"Authorization header: {auth_header}")

        auth_parts = auth_header.split()
        if len(auth_parts) != 2 or auth_parts[0].lower() != 'bearer':
            raise KeyError("Invalid Authorization header format")
        token = auth_parts[1]

        decoded_token = jwt.decode(token, options={"verify_signature": False})
        logger.info(f"Decoded token: {decoded_token}")

        if 'sub' not in decoded_token:
            raise KeyError("User ID (sub) not found in the token")
        user_id = decoded_token['sub']

        logger.info(f"Get task by ID request received for user: {user_id}")

        task_id = event['pathParameters']['taskId']

        response = table.get_item(
            Key={
                'user_id': user_id,
                'task_id': task_id
            }
        )

        task = response.get('Item')

        if not task:
            logger.warning(f"Task not found: {task_id}")
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Task not found'})
            }

        logger.info(f"Task retrieved successfully: {task_id}")
        return {
            'statusCode': 200,
            'body': json.dumps(task)
        }
    except KeyError as e:
        logger.error(f"Unauthorized - {str(e)}")
        return {
            'statusCode': 401,
            'body': json.dumps({'error': f'Unauthorized - {str(e)}'})
        }
    except InvalidTokenError as e:
        logger.error(f"Unauthorized - Invalid token: {str(e)}")
        return {
            'statusCode': 401,
            'body': json.dumps({'error': 'Unauthorized - Invalid token'})
        }
    except Exception as e:
        logger.error(f"Error retrieving task: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }