# ERP Implementation Assistant API

FastAPI backend for the AI-powered M3 implementation assistant.

## Quick Start

### Start Server
```bash
cd api
python main.py
```

Server starts at: `http://localhost:8000`

### API Documentation

Interactive docs: `http://localhost:8000/docs`

## Endpoints

### GET /health

Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "ERP Implementation Assistant API",
  "version": "1.0.0"
}
```

---

### POST /api/query

Main endpoint for querying the assistant.

**Request:**
```json
{
  "query": "How do I set up a customer order type?",
  "user_context": {
    "company": "100",
    "division": "200",
    "user_id": "JDOE",
    "language": "en"
  },
  "conversation_history": []
}
```

**Response:**
```json
{
  "answer": "To set up a customer order type...",
  "query_type": "configuration",
  "modules": ["OIS", "PPS"],
  "sources": ["M3 Documentation"],
  "response_time": 15.23
}
```

---

### POST /api/query/stream

Streaming version using Server-Sent Events (SSE).

**Usage:**
```javascript
const eventSource = new EventSource('/api/query/stream');
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

---

### GET /api/metadata

Get API capabilities and metadata.

**Response:**
```json
{
  "version": "1.0.0",
  "capabilities": {
    "query_types": ["configuration", "troubleshooting", "best_practices"],
    "modules": ["OIS", "PPS", "MMS", "CRS"],
    "streaming": true
  },
  "model": "gpt-4o-mini",
  "knowledge_base": {
    "documents": 4,
    "chunks": 6360
  }
}
```

## Configuration

### Environment Variables

Create `.env` file:
```
OPENAI_API_KEY=your-key
ALLOWED_ORIGINS=http://localhost:8080,https://your-m3-server
MODEL_NAME=gpt-4o-mini
LOG_LEVEL=INFO
```

## Deployment

### Docker (Coming Soon)

### ION API Gateway (Coming Soon)

## Testing

### Using curl
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I set up a customer order?"}'
```

### Using Python
```python
import requests

response = requests.post(
    "http://localhost:8000/api/query",
    json={
        "query": "How do I configure a purchase order type?",
        "user_context": {
            "company": "100",
            "user_id": "TEST"
        }
    }
)

print(response.json()["answer"])
```

### Using JavaScript (H5 Widget)
```javascript
fetch('http://localhost:8000/api/query', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    query: "How do I set up a customer order?",
    user_context: {
      company: userContext.currentCompany,
      user_id: userContext.USID
    }
  })
})
.then(res => res.json())
.then(data => console.log(data.answer));
```

## Error Handling

All endpoints return standard HTTP status codes:

- `200` - Success
- `400` - Bad Request (invalid input)
- `500` - Internal Server Error

Error response format:
```json
{
  "error": "Error description",
  "status_code": 500
}
```

## Next Steps

1. Deploy to production server
2. Configure CORS for M3 domain
3. Add authentication
4. Implement rate limiting
5. Add caching layer
