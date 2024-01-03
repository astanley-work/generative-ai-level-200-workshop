import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import json
import pandas as pd

# Example to help: https://github.com/aws-samples/semantic-search-with-amazon-opensearch/blob/main/Module%203%20-%20Semantic%20Search.ipynb
# Dataset download link: https://amazon-pqa.s3.amazonaws.com/amazon_pqa_headsets.json

### STEP 1 - Import dataset JSON file
headsets_dataframe = pd.read_json('./amazon_pqa_headsets.json', lines=True)

### STEP 2 - Pass documents to amazon bedrock Titan Embeddings
# Bedrock config

# Embed Documents


### STEP 3 - Create connection to OpenSearch cluster
# Opensearch config variables
region = 'us-west-2' 
aos_host = # Add your domain endpoint

username = # Add your domain username
password = # Add your domain password

auth = (username, password)

index_name = # Choose an index name


# Create connection
aos_client = OpenSearch(
    hosts = [{'host': aos_host, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

### STEP 4 - Create OpenSearch KNN index
# Configure Index
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
            "dataset_row_vector": {
                "type": "knn_vector",
                "dimension": 1536,
                "store": True
            },
            "dataset_row": {
                "type": "text",
                "store": True
            }
        }
    }
}

# Create index based on configuration

# STEP 5 - Pass document embeddings to OpenSearch cluster
