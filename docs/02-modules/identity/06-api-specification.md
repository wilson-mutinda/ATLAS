# Identity Module — API Specification

## API Information

| Item           | Value                 |
| -------------- | --------------------- |
| API Version``  | v1                    |
| Base Path      | `/api/v1/auth/`       |
| Format         | JSON                  |
| Authentication | JWT                   |
| Backend        | Django REST Framework |

---

## Public Endpoints

| Method | Endpoint                   | Purpose                |
| ------ | -------------------------- | ---------------------- |
| POST   | `/register/`               | Create user account    |
| POST   | `/login/`                  | Authenticate user      |
| POST   | `/token/refresh/`          | Refresh access token   |
| POST   | `/password/reset/`         | Request password reset |
| POST   | `/password/reset/confirm/` | Set new password       |

---

## Protected Endpoints

| Method | Endpoint            | Purpose               |
| ------ | ------------------- | --------------------- |
| GET    | `/me/`              | Retrieve current user |
| PATCH  | `/me/`              | Update current user   |
| POST   | `/logout/`          | Logout                |
| POST   | `/password/change/` | Change password       |

Protected requests use:

```http
Authorization: Bearer <access_token>
```

---

## Registration

### Request

```json
{
    "email": "admin@atlas.com",
    "first_name": "Wilson",
    "last_name": "Mutinda",
    "password": "SecurePassword123!",
    "password_confirm": "SecurePassword123!"
}
```

### Success

```http
201 Created
```

```json
{
    "message": "User registered successfully.",
    "user": {
        "id": 1,
        "email": "admin@atlas.com",
        "first_name": "Wilson",
        "last_name": "Mutinda"
    }
}
```

---

## Login

### Request

```json
{
    "email": "admin@atlas.com",
    "password": "SecurePassword123!"
}
```

### Success

```http
200 OK
```

Returns:

```text
access
refresh
user
```

---

## Current User

```http
GET /api/v1/auth/me/
```

Returns the authenticated user's public profile.

---

## Update Profile

```http
PATCH /api/v1/auth/me/
```

Accepts user profile fields such as:

```json
{
    "first_name": "Wilson",
    "last_name": "Mutinda"
}
```

---

## Change Password

```http
POST /api/v1/auth/password/change/
```

Requires the authenticated user's current password and a valid new password.

---

## Password Reset

### Request

```http
POST /api/v1/auth/password/reset/
```

The endpoint does not reveal whether an email address exists.

### Confirmation

```http
POST /api/v1/auth/password/reset/confirm/
```

Requires:

```text
uid
token
new_password
new_password_confirm
```

---

## Logout

```http
POST /api/v1/auth/logout/
```

Invalidates the supplied refresh token according to the configured JWT logout strategy.

---

## Standard Responses

```text
200 OK
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
500 Internal Server Error
```

---

## Security Rules

The API must never return:

* Plain-text passwords
* Password hashes
* Django secret keys
* Database credentials
* Internal server paths
* Production stack traces

---

## Implementation Status

```text
Identity API: COMPLETE
```
