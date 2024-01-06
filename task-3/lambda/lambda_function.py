import boto3
import json
import datetime
import uuid
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import pandas as pd

# How to install opensearch-py as a lambda layer (see virtual environment step): https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

# Write function to take request from user and return relevant vector store documents
def get_relevant_vector_store_documents(user_request_string):

    ### Step 1 - Embed user query with Amazon Titan embeddings

    ### Step 2 - Connect to opensearch cluster

    ### Step 3 - Query OpenSearch

    ### Step 4 - Parse OpenSearch response and return relevant vector store documents



def count_tokens(input_string):

    string_collection = input_string.split(" ")
    words = len(string_collection)
    tokens = (4 / 3) * words
    output_number = round(tokens, 0)

    return output_number

def lambda_handler(event, context):

    ### OPENSEARCH
    # Create client to connect to OpenSearch
    opensearch_client = boto3.client(
        service_name='opensearch',
        region_name='us-west-2'
    )

    ### BEDROCK
    # Create client to connect to Amazon Bedrock
    bedrock_client = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-west-2'
    )
    
    json_version = json.loads(event['body'])
    user_request = json_version['user_request']

    # Query OpenSearch Cluster for information relevant to user query
    opensearch_results = get_relevant_vector_store_documents(user_request)

    result_1 = opensearch_results[0]
    result_2 = opensearch_results[1]
    result_3 = opensearch_results[2]
    
    # Configuration
    prompt = "You are a helpful support bot for the Call Center Co. customer support team. One of our agents just asked you a question: " + user_request + " Please keep your response short and to the point. The following information may also be useful in your response " + result_1 + ", " + result_2 + ", " + result_3
    
    model_id = "anthropic.claude-v2:1"

    kwargs = {
      "modelId": model_id,
      "contentType": "application/json",
      "accept": "*/*",
      "body": "{\"prompt\":\"Human: " + prompt + " \\nAssistant:\",\"max_tokens_to_sample\":1000,\"temperature\":1,\"top_k\":250,\"top_p\":0.999,\"stop_sequences\":[\"\\n\\nHuman:\"],\"anthropic_version\":\"bedrock-2023-05-31\"}"
    }

    # Invoke bedrock API
    response = bedrock_client.invoke_model(**kwargs)
    response_body = json.loads(response.get('body').read())
    completion = response_body['completion']

    ### DynamoDB
    # Log number of request and response tokens to DynamoDB Table
    dynamodb_client = boto3.client('dynamodb')

    # Generate uuid and other config
    user_id = uuid.uuid4()
    timestamp = datetime.datetime.now()
    input_tokens = count_tokens(prompt)
    output_tokens = count_tokens(completion)
    application_name = "internal-support-chatbot"

    # Put metadata in DDB
    ddb_response = dynamodb_client.put_item(
        TableName='call-center-co-chatbot-logging',
        Item={
            'session_id': {'S': str(user_id)},
            'time_stamp': {'S': str(timestamp)},
            'model_id': {'S': str(model_id)},
            'application_name': {'S': str(application_name)},
            'input_tokens': {'N': str(input_tokens)},
            'output_tokens': {'N': str(output_tokens)},
            'prompt_text':  {'N': str(prompt)},
            'completion_text':  {'N': str(completion)}
        }
    )

    return {
        'statusCode': 200,
        'body': completion
    }
