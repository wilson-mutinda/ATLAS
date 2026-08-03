# Core Testing

## Endpoint

```
GET /api/v1/health/
```

## Test Tool

Postman

## Test Cases

### Test 1

Description

Health endpoint returns success.

Expected Result

HTTP 200

Status

Passed

---

### Response

```json
{
    "status": "ok",
    "application": "Atlas Business Suite",
    "version": "0.1.0",
    "environment": "development"
}
```

## Result

Passed