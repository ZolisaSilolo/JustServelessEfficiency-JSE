# Serverless Document Q&A System

This project implements a serverless document Q&A system using AWS services and the Cohere API. The system consists of two main components:

1. Document Ingestion (Lambda Function):
   - Triggers on S3 uploads
   - Processes PDF/text documents
   - Generates embeddings using Cohere
   - Indexes content in OpenSearch

2. Query Processing (Lambda Function):
   - Exposes REST API via API Gateway
   - Processes user queries
   - Performs semantic search using embeddings
   - Generates answers using Cohere

## Prerequisites

- AWS SAM CLI
- Python 3.9
- Cohere API key
- AWS account with appropriate permissions

## Deployment

1. Update the CohereApiSecret in template.yaml with your actual Cohere API key
2. Build and deploy using SAM:
```bash
sam build
sam deploy --guided
```

## Usage

1. Upload documents:
   - Upload PDF or text files to the created S3 bucket
   - Documents will be automatically processed and indexed

2. Query the system:
   ```bash
   curl -X POST https://your-api-endpoint/Prod/query \
        -H "Content-Type: application/json" \
        -d '{"query": "Your question here"}'
   ```