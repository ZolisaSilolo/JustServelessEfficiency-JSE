import json
import os
import boto3
import cohere
from opensearchpy import OpenSearch, RequestsHttpConnection
from PyPDF2 import PdfReader
import io

# Initialize clients
s3 = boto3.client('s3')
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
    # Get bucket and key from event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Download file from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    file_content = response['Body'].read()
    
    # Extract text based on file type
    if key.lower().endswith('.pdf'):
        pdf = PdfReader(io.BytesIO(file_content))
        text = '\n'.join(page.extract_text() for page in pdf.pages)
    else:
        text = file_content.decode('utf-8')
    
    # Split text into chunks (simple approach)
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    
    # Initialize Cohere client
    co = cohere.Client(get_cohere_api_key())
    
    # Generate embeddings for each chunk
    for i, chunk in enumerate(chunks):
        embedding = co.embed(texts=[chunk], model='embed-english-v3.0').embeddings[0]
        
        # Index document in OpenSearch
        doc = {
            'text': chunk,
            'embedding': embedding,
            'document_id': key,
            'chunk_id': i
        }
        
        opensearch.index(
            index='documents',
            body=doc,
            id=f"{key}-{i}"
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Processed {len(chunks)} chunks from {key}')
    }