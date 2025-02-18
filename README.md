# 🚀 Serverless Document Q&A System with GenAI

A serverless solution for document question-answering powered by **AWS Serverless Services** and **Cohere's Generative AI**. Automatically process documents, generate embeddings, and answer natural language queries with AI-driven insights.

---

## ✨ Features

- **Auto-Processing Pipeline**: Upload PDF/text files to S3 for automatic indexing.
- **Semantic Search**: Find relevant content using Cohere embeddings.
- **AI-Powered Answers**: Generate human-like responses via Cohere's LLM.
- **Serverless Architecture**: Built with AWS Lambda, API Gateway, and OpenSearch.

---

## 📦 System Architecture

### 1. Document Ingestion Pipeline
- **Trigger**: S3 bucket upload (PDF/text files).
- **Processing**: Text extraction, chunking, and embedding generation via Cohere.
- **Storage**: Embeddings indexed in Amazon OpenSearch.

### 2. Query Processing
- **API Endpoint**: REST API through API Gateway.
- **Workflow**: 
  1. Convert user queries to embeddings.
  2. Semantic search in OpenSearch.
  3. Generate answers using Cohere's generative model.

![Architecture Diagram](https://via.placeholder.com/600x300?text=Architecture+Diagram+Here) *Add your diagram later*

---

## 🛠️ Prerequisites

- AWS Account with IAM permissions for:
  - Lambda, S3, API Gateway, OpenSearch, CloudFormation
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Python 3.9
- [Cohere API Key](https://dashboard.cohere.com/api-keys)

---

## 🚀 Deployment

### 1. Configure Secrets
Update `template.yaml` with your Cohere API key:
```yaml
Resources:
  CohereApiSecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: cohere-api-key
      SecretString: YOUR_API_KEY_HERE  # 🔑 Replace this

##Build & Deploy
sam build --use-container  # Builds Lambda functions in a container
sam deploy --guided        # Follow prompts to configure stack

*Note:* SAM CLI will prompt for stack name, AWS region, and confirm IAM role changes.

---

## 📖 Usage

### 1. Upload Documents
- Upload PDF or text files to the S3 bucket created during deployment.
- Documents are automatically processed (check CloudWatch logs for errors).

### 2. Ask Questions
```bash
curl -X POST "https://YOUR_API_ENDPOINT/Prod/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the main topic of the document?"}'
```

**Sample Response:**
```json
{
  "answer": "The document discusses...",
  "source_documents": ["s3://your-bucket/doc.pdf"]
}
```

---

## 🔧 Troubleshooting

- **Embedding Failures**: Ensure Cohere API key is valid and has sufficient credits.
- **S3 Trigger Issues**: Verify Lambda has `s3:ObjectCreated:*` permission.
- **Slow Responses**: Check OpenSearch cluster performance metrics.

---

## 📜 License

Apache 2.0 | [Please do Report Issues when you find them]--->^