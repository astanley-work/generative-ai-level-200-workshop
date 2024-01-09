import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import json
import pandas as pd

# Example to give people: https://github.com/aws-samples/semantic-search-with-amazon-opensearch/blob/main/Module%203%20-%20Semantic%20Search.ipynb
# Link to download: https://amazon-pqa.s3.amazonaws.com/amazon_pqa_headsets.json

# STEP 1 - Import dataset JSON file
headsets_dataframe = pd.read_json('./amazon_pqa_headsets.json', lines=True)

# STEP 2 - Pass documents to amazon bedrock Titan Embeddings
bedrock_client = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

vectors = []

i = 0 

for row in headsets_dataframe.iterrows():
    question_text = row[1]['question_text'].replace('"', '')
    answer_text = row[1]['answers'][0]['answer_text'].replace('"', '')
    item_metadata = "Product Brand Name: " + row[1]['brand_name'] + " Product Name: " + row[1]['item_name'] #+ ' Question: ' + row[1]['question_text'] + ' Answer: ' + answer_text + '" }'
    formatted_question_text = '{ "inputText": "' + row[1]['question_text'].replace('"', '') + '" }'

    bytes_question = bytes(formatted_question_text, 'utf-8')

    # text = '"The lazy dog jumps over the quick brown fox"'
    response = bedrock_client.invoke_model(
        body = bytes_question,
        modelId = "amazon.titan-embed-text-v1",
        accept = "*/*",
        contentType = "application/json"
    )

    response_body = response['body'].read()
    response_body_json = json.loads(response_body)
    strip_response = response_body_json['embedding']

    vectors.append([strip_response, question_text, answer_text, item_metadata])

    if (i % 10 == 0):
        print("Documents Embedded: ", i)
        print("Vector: ", vectors[i])

    if (i == 1000):
        break
    
    i+=1

print("Documents Embedded")


# STEP 3 - Create connection to OpenSearch cluster
region = 'us-east-1' 
aos_host = "search-new-york-task-3-demo-domain-hxscangjusa5ttlk4kogqnrin4.aos.us-east-1.on.aws" # Note - do not include "https://" at the start

username = "admin"
password = "$Password123"

auth = (username, password)

index_name = 'question_answer_index_1'

aos_client = OpenSearch(
    hosts = [{'host': aos_host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

# STEP 4 - Create OpenSearch KNN index
knn_index = {
    "settings": {
        "index.knn": True,
        "index.knn.space_type": "cosinesimil",
        "analysis": {
          "analyzer": {
            "default": {
              "type": "standard",
              "stopwords": "_english_"
            }
          }
        }
    },
    "mappings": {
        "properties": {
            "question_vector": {
                "type": "knn_vector",
                "dimension": 1536,
                "store": True
            },
            "question": {
                "type": "text",
                "store": True
            },
            "answer": {
                "type": "text",
                "store": True
            },
            "item_metadata": {
                "type": "text",
                "store": True
            }
        }
    }
}

aos_client.indices.create(index=index_name,body=knn_index,ignore=400)

print("Index Created: ", aos_client.indices.get(index=index_name))


# STEP 5 - Pass document embeddings to OpenSearch cluster
for vector in vectors:

    document_to_ingest = {
        "question_vector": vector[0],
        "question": vector[1],
        "answer": vector[2],
        "item_metadata": vector[3]
    }

    response = aos_client.index(
        index = index_name,
        body = document_to_ingest
    )

    print("Ingestion Response: ", response)


print("Documents Indexed")

