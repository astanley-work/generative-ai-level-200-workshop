import boto3
import json
import datetime
import uuid

def count_tokens(input_string):

    string_collection = input_string.split(" ")
    words = len(string_collection)
    tokens = (4 / 3) * words
    output_number = round(tokens, 0)

    return output_number

def lambda_handler(event, context):
    
    ### BEDROCK
    # Create client to connect to Amazon Bedrock
   
    # Bedrock configuration variables

    # Invoke bedrock API

    ### DynamoDB
    # Log number of request and response tokens to DynamoDB Table

    # Generate uuid and other config

    # Put metadata in DDB

    return {
        'statusCode': 200,
        'body': "Hello World"
    }
