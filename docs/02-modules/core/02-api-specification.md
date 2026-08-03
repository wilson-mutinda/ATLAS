# Core API Specification

---

## Health Check

### Endpoint

```
GET /api/v1/health/
```

### Authentication

None

### Description

Returns the operational status of the Atlas backend.

### Request

No request body.

### Success Response

Status Code

```
200 OK
```

Body

```json
{
    "status": "ok",
    "application": "Atlas Business Suite",
    "version": "0.1.0",
    "environment": "development"
}
```

### Errors

None currently.

### Future Improvements

- Database connectivity status
- Cache status
- Storage status
- Queue status
