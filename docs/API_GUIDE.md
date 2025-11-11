# ERP Assistant API - Quick Guide

## What is it?
AI-powered M3 implementation assistant accessible via REST API

## How to use it?

### Start the server:
```bash
cd api
python main.py
```

### Test it:
http://localhost:8000/docs

### Example query:
```json
{
  "query": "How do I set up a customer order type?"
}
```

### Example response:
```json
{
  "answer": "To set up a customer order type...",
  "query_type": "configuration",
  "modules": ["OIS"],
  "response_time": 15.2
}
```

## Next: H5 Widget Integration
Coming next week!
