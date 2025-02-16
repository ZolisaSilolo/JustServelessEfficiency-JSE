import json
import os
import boto3
import cohere
from opensearchpy import OpenSearch, RequestsHttpConnection

# Initialize clients
secrets = boto3.client('secrets-manager')

# Get Cohere API key from Secrets Manager
def get_cohere_api_key():
    secret_response = secrets.get_secret_value(SecretId=os.environ['COHERE_SECRET_ARN'])
    secret = json.loads(secret_response['SecretString'])
    return secret['COHERE_API_KEY']

# Initialize OpenSearch client
opensearch = OpenSearch(
    hosts=[{'host': os.environ['OPENSEARCH_DOMAIN'], 'port': 443}],
    http_auth=('admin', 'admin'),  # Replace with proper auth
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

def lambda_handler(event, context):
    # Parse query from request body
    body = json.loads(event['body'])
    query = body.get('query')
    
    if not query:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Query parameter is required'})
        }
    
    # Initialize Cohere client
    co = cohere.Client(get_cohere_api_key())
    
    # Generate embedding for query
    query_embedding = co.embed(texts=[query], model='embed-english-v3.0').embeddings[0]
    
    # Perform k-NN search in OpenSearch
    search_query = {
        "size": 5,
        "query": {
            "knn": {
                "embedding": {
                    "vector": query_embedding,
                    "k": 5
                }
            }
        }
    }
    
    response = opensearch.search(
        index='documents',
        body=search_query
    )
    
    # Extract matched text chunks
    contexts = [hit['_source']['text'] for hit in response['hits']['hits']]
    
    # Generate answer using Cohere
    prompt = f"""Based on the following contexts, answer the question: {query}

Contexts:
{' '.join(contexts)}

Answer:"""
    
    generation = co.generate(
        model='command',
        prompt=prompt,
        max_tokens=300,
        temperature=0.7
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'answer': generation.generations[0].text,
            'sources': contexts
        })
    }