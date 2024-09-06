import json
import boto3
from boto3.dynamodb.conditions import Key
import logging
import jwt
from jwt import InvalidTokenError

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

        logger.info(f"Update task request received for user: {user_id}")
        
        if 'body' not in event:
            raise ValueError("Request body is missing")
        
        body = json.loads(event['body'])
        logger.info(f"Request body: {body}")
        
        if 'pathParameters' not in event or 'taskId' not in event['pathParameters']:
            raise ValueError("taskId is missing in path parameters")
        task_id = event['pathParameters']['taskId']
        
        updates = body
        
        update_expression = "SET "
        expression_attribute_values = {}
        expression_attribute_names = {}
        
        for key, value in updates.items():
            update_expression += f"#{key} = :{key}, "
            expression_attribute_values[f":{key}"] = value
            expression_attribute_names[f"#{key}"] = key
        
        update_expression = update_expression.rstrip(", ")
        
        logger.info(f"Update expression: {update_expression}")
        logger.info(f"Expression attribute values: {expression_attribute_values}")
        logger.info(f"Expression attribute names: {expression_attribute_names}")
        
        response = table.update_item(
            Key={
                'user_id': user_id,
                'task_id': task_id
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="ALL_NEW"
        )
        
        updated_task = response['Attributes']
        
        logger.info(f"Task updated successfully: {task_id}")
        logger.info(f"Updated task: {updated_task}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(updated_task)
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
    except ValueError as e:
        logger.error(f"Bad Request - {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Bad Request - {str(e)}'})
        }
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }