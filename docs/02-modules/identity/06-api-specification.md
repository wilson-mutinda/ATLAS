# Identity Module API Specification

## 1. Document Information

| Item            | Details                   |
| --------------- | ------------------------- |
| Module          | Identity                  |
| Document        | API Specification         |
| Document File   | `06-api-specification.md` |
| Module Path     | `backend/apps/identity/`  |
| API Base Path   | `/api/v1/auth/`           |
| API Version     | `v1`                      |
| Current Version | `0.1.0`                   |
| Status          | Draft                     |
| Last Updated    | July 31, 2026             |

---

## 2. Purpose

This document defines the API contracts for the Identity module of Atlas Business Suite.

It specifies:

* Available API endpoints
* HTTP methods
* Request structures
* Request fields
* Authentication requirements
* Validation rules
* Success responses
* Error responses
* Expected HTTP status codes

The API specification acts as the agreement between the Atlas backend and its clients, including:

* The Atlas Vue frontend
* Postman
* Future mobile applications
* Third-party integrations
* Other Atlas modules

All Identity API implementations must follow the contracts defined in this document.

---

## 3. API Base URL

During local development, the Atlas backend runs at:

```text
http://127.0.0.1:8000
```

The Identity API base path is:

```text
/api/v1/auth/
```

Therefore, the complete local API base URL is:

```text
http://127.0.0.1:8000/api/v1/auth/
```

---

## 4. API Conventions

### 4.1 API Versioning

Atlas APIs use URL-based versioning.

The current API version is:

```text
v1
```

Example:

```text
/api/v1/auth/register/
```

The API version allows Atlas to introduce future changes without immediately breaking existing frontend applications or integrations.

---

### 4.2 Data Format

Identity API requests and responses use JSON.

Requests must include:

```http
Content-Type: application/json
```

Example:

```http
Content-Type: application/json
```

---

### 4.3 URL Format

Atlas API URLs use:

* Lowercase letters
* Hyphen-separated words where necessary
* A trailing slash

Example:

```text
/api/v1/auth/password-reset/
```

---

### 4.4 HTTP Methods

The Identity module uses standard HTTP methods.

| Method   | Purpose                               |
| -------- | ------------------------------------- |
| `GET`    | Retrieve information                  |
| `POST`   | Create data or perform an action      |
| `PATCH`  | Partially update existing information |
| `DELETE` | Remove or invalidate a resource       |

---

### 4.5 Response Format

Successful requests return JSON responses.

Example:

```json
{
    "message": "User registered successfully."
}
```

Responses containing user information use a nested `user` object.

Example:

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

Passwords and password hashes must never be returned in API responses.

---

## 5. Authentication

Atlas uses JSON Web Tokens (JWT) for API authentication.

Protected Identity endpoints require a valid JWT access token.

The token is sent using the HTTP `Authorization` header.

Format:

```http
Authorization: Bearer <access_token>
```

Example:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

The following endpoints do not require authentication:

| Endpoint                            | Reason                                                      |
| ----------------------------------- | ----------------------------------------------------------- |
| `POST /api/v1/auth/register/`       | A new user does not yet have an account                     |
| `POST /api/v1/auth/login/`          | The user needs credentials to obtain tokens                 |
| `POST /api/v1/auth/token/refresh/`  | A refresh token is used instead of an access token          |
| `POST /api/v1/auth/password/reset/` | A user may request a password reset without being logged in |

Protected endpoints include:

| Endpoint                             | Authentication |
| ------------------------------------ | -------------- |
| `GET /api/v1/auth/me/`               | Required       |
| `PATCH /api/v1/auth/me/`             | Required       |
| `POST /api/v1/auth/logout/`          | Required       |
| `POST /api/v1/auth/password/change/` | Required       |

---

## 6. Endpoint Summary

| Method  | Endpoint                        | Description                               | Authentication         | Status   |
| ------- | ------------------------------- | ----------------------------------------- | ---------------------- | -------- |
| `POST`  | `/api/v1/auth/register/`        | Create a new Atlas user account           | Not required           | Complete |
| `POST`  | `/api/v1/auth/login/`           | Authenticate a user and issue JWT tokens  | Not required           | Planned  |
| `POST`  | `/api/v1/auth/token/refresh/`   | Generate a new access token               | Refresh token required | Planned  |
| `GET`   | `/api/v1/auth/me/`              | Retrieve the authenticated user's profile | Required               | Planned  |
| `PATCH` | `/api/v1/auth/me/`              | Update the authenticated user's profile   | Required               | Planned  |
| `POST`  | `/api/v1/auth/logout/`          | End the current user session              | Required               | Planned  |
| `POST`  | `/api/v1/auth/password/change/` | Change the authenticated user's password  | Required               | Planned  |
| `POST`  | `/api/v1/auth/password/reset/`  | Request a password-reset process          | Not required           | Planned  |

---

# 7. User Registration API

## 7.1 Endpoint

```http
POST /api/v1/auth/register/
```

Complete local URL:

```text
http://127.0.0.1:8000/api/v1/auth/register/
```

---

## 7.2 Purpose

The registration endpoint creates a new Atlas user account.

The endpoint:

1. Receives the user's registration information.
2. Validates the submitted data.
3. Confirms that the passwords match.
4. Creates the user using the Atlas custom User model.
5. Hashes the password using Django's password-management system.
6. Stores the user in PostgreSQL.
7. Returns the created user's public information.

The password is never returned in the response.

---

## 7.3 Authentication

Authentication is not required.

The request must not require a JWT access token.

| Requirement             | Value        |
| ----------------------- | ------------ |
| Authentication required | No           |
| JWT access token        | Not required |
| Permission level        | Public       |

---

## 7.4 Request Headers

```http
Content-Type: application/json
```

---

## 7.5 Request Body

```json
{
    "email": "admin@atlas.com",
    "first_name": "Wilson",
    "last_name": "Mutinda",
    "password": "SecurePassword123!",
    "password_confirm": "SecurePassword123!"
}
```

---

## 7.6 Request Fields

| Field              | Data Type | Required | Description                     |
| ------------------ | --------- | -------- | ------------------------------- |
| `email`            | String    | Yes      | The user's unique email address |
| `first_name`       | String    | Yes      | The user's first name           |
| `last_name`        | String    | Yes      | The user's last name            |
| `password`         | String    | Yes      | The user's chosen password      |
| `password_confirm` | String    | Yes      | Must match the password         |

---

## 7.7 Request Validation

The registration request must satisfy the following rules:

| Rule                                       | Expected Behavior                                 |
| ------------------------------------------ | ------------------------------------------------- |
| Email is required                          | Reject the request when the email is missing      |
| Email must be valid                        | Reject invalid email formats                      |
| Email must be unique                       | Reject an email already assigned to another user  |
| First name is required                     | Reject the request when the first name is missing |
| Last name is required                      | Reject the request when the last name is missing  |
| Password is required                       | Reject the request when the password is missing   |
| Password confirmation is required          | Reject the request when confirmation is missing   |
| Passwords must match                       | Reject the request when the values differ         |
| Password must meet Django validation rules | Reject weak or invalid passwords                  |

Detailed validation behavior is documented in:

```text
07-validation-rules.md
```

---

## 7.8 Successful Response

### HTTP Status

```http
201 Created
```

### Response Body

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

## 7.9 Successful Response Fields

| Field             | Data Type | Description                               |
| ----------------- | --------- | ----------------------------------------- |
| `message`         | String    | Confirms that registration was successful |
| `user.id`         | Integer   | Unique database identifier of the user    |
| `user.email`      | String    | Registered email address                  |
| `user.first_name` | String    | User's first name                         |
| `user.last_name`  | String    | User's last name                          |

The response must not contain:

* `password`
* `password_confirm`
* Password hashes
* JWT tokens
* Internal security information

---

## 7.10 Validation Error Response

When submitted data is invalid, the API returns:

```http
400 Bad Request
```

Example:

```json
{
    "email": [
        "A user with this email already exists."
    ]
}
```

Another example:

```json
{
    "password_confirm": [
        "Passwords do not match."
    ]
}
```

The exact validation messages are controlled by the Identity serializer and Django validation system.

---

## 7.11 Registration API Status

| Item                    | Status   |
| ----------------------- | -------- |
| Custom User model       | Complete |
| Registration serializer | Complete |
| Registration API view   | Complete |
| Registration URL        | Complete |
| PostgreSQL storage      | Complete |
| Password hashing        | Complete |
| Postman verification    | Complete |
| Automated tests         | Planned  |
| Vue integration         | Planned  |

---

# 8. User Login API

## 8.1 Endpoint

```http
POST /api/v1/auth/login/
```

## Get Current User

### Endpoint

```http
GET /api/v1/auth/me/
```

### Authentication

JWT access token is required.

### Request Header

```http
Authorization: Bearer <access_token>
```

### Success Response

**Status:** `200 OK`

```json
{
    "user": {
        "id": 1,
        "email": "admin@atlas.com",
        "first_name": "Wilson",
        "last_name": "Mutinda"
    }
}
```

### Unauthorized Response

**Status:** `401 Unauthorized`

```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Refresh Access Token

### Endpoint

```http
POST /api/v1/auth/token/refresh/
```

### Authentication

No access token is required. A valid refresh token must be provided in the request body.

### Request

```json
{
    "refresh": "<refresh_token>"
}
```

### Success Response

**Status:** `200 OK`

```json
{
    "access": "<new_access_token>"
}
```

### Failure Response

**Status:** `401 Unauthorized`

```json
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```

### Rules

* The refresh token must be valid.
* The refresh token must not be expired.
* A new access token is generated when the refresh token is accepted.
* The user does not need to enter their email or password again.


---

## 8.2 Purpose

The login endpoint will authenticate a registered Atlas user using an email address and password.

When authentication succeeds, the endpoint will issue:

* A JWT access token
* A JWT refresh token

---

## 8.3 Authentication

Authentication will not be required because the endpoint is used to obtain authentication tokens.

| Requirement             | Value        |
| ----------------------- | ------------ |
| Authentication required | No           |
| JWT access token        | Not required |
| Status                  | Planned      |

---

## 8.4 Planned Request

```json
{
    "email": "admin@atlas.com",
    "password": "SecurePassword123!"
}
```

---

## 8.5 Planned Success Response

```json
{
    "message": "Login successful.",
    "access": "<access_token>",
    "refresh": "<refresh_token>",
    "user": {
        "id": 1,
        "email": "admin@atlas.com",
        "first_name": "Wilson",
        "last_name": "Mutinda"
    }
}
```

---

## 8.6 Planned Success Status

```http
200 OK
```

---

## 8.7 Planned Authentication Error

```http
401 Unauthorized
```

Example:

```json
{
    "detail": "Invalid email or password."
}
```

---

## 8.8 Implementation Status

```text
Planned
```

The Login API must be reviewed and approved before implementation begins.

---

# 9. JWT Token Refresh API

## 9.1 Endpoint

```http
POST /api/v1/auth/token/refresh/
```

---

## 9.2 Purpose

The token-refresh endpoint will accept a valid refresh token and return a new access token.

---

## 9.3 Planned Request

```json
{
    "refresh": "<refresh_token>"
}
```

---

## 9.4 Planned Success Response

```json
{
    "access": "<new_access_token>"
}
```

---

## 9.5 Planned Status

```http
200 OK
```

---

## 9.6 Implementation Status

```text
Planned
```

---

# 10. Authenticated User Profile API

## 10.1 Retrieve Current User

### Endpoint

```http
GET /api/v1/auth/me/
```

### Authentication

Required.

```http
Authorization: Bearer <access_token>
```

### Planned Success Response

```json
{
    "id": 1,
    "email": "admin@atlas.com",
    "first_name": "Wilson",
    "last_name": "Mutinda"
}
```

### Planned Status

```http
200 OK
```

### Implementation Status

```text
Planned
```

---

## 10.2 Update Current User

### Endpoint

```http
PATCH /api/v1/auth/me/
```

### Authentication

Required.

```http
Authorization: Bearer <access_token>
```

### Planned Request

```json
{
    "first_name": "Wilson",
    "last_name": "Kilonzo"
}
```

### Planned Success Status

```http
200 OK
```

### Implementation Status

```text
Planned
```

---

# 11. User Logout API

## Logout

### Endpoint

```text
POST /api/v1/auth/logout/
```

### Authentication

JWT access token required.

### Request Body

```json
{
    "refresh": "<refresh_token>"
}
```

### Success Response

**Status:** `200 OK`

```json
{
    "message": "Logout successful."
}
```

### Failure Responses

**Missing refresh token — `400 Bad Request`**

```json
{
    "refresh": [
        "This field is required."
    ]
}
```

**Invalid or expired refresh token — `400 Bad Request`**

```json
{
    "detail": "Invalid or expired refresh token."
}
```

**Missing or invalid access token — `401 Unauthorized`**

The request is rejected because the logout endpoint requires an authenticated user.

### Behavior

When logout succeeds:

1. The supplied refresh token is added to the JWT blacklist.
2. The refresh token cannot be used to obtain another access token.
3. The client must delete its stored access and refresh tokens.
4. Any existing access token remains valid until it expires.


---

# 12. Password Change API

## 12.1 Endpoint

```http
POST /api/v1/auth/password/change/
```

---

## 12.2 Authentication

Required.

```http
Authorization: Bearer <access_token>
```

---

## 12.3 Planned Request

```json
{
    "current_password": "CurrentPassword123!",
    "new_password": "NewSecurePassword123!",
    "new_password_confirm": "NewSecurePassword123!"
}
```

---

## 12.4 Planned Success Response

```json
{
    "message": "Password changed successfully."
}
```

---

## 12.5 Planned Status

```http
200 OK
```

---

## 12.6 Implementation Status

```text
Planned
```

---

# 13. Password Reset API

## 13.1 Endpoint

```http
POST /api/v1/auth/password/reset/
```

---

## 13.2 Purpose

The password-reset endpoint will allow a user to begin a secure password-reset process using their registered email address.

---

## 13.3 Authentication

Not required.

---

## 13.4 Planned Request

```json
{
    "email": "admin@atlas.com"
}
```

---

## 13.5 Planned Success Response

```json
{
    "message": "If the email address exists, password-reset instructions will be sent."
}
```

---

## 13.6 Planned Status

```http
200 OK
```

---

## 13.7 Implementation Status

```text
Planned
```

---

# 14. Standard HTTP Status Codes

| Status Code                 | Meaning                                       | Identity Usage                                   |
| --------------------------- | --------------------------------------------- | ------------------------------------------------ |
| `200 OK`                    | Request completed successfully                | Login, profile retrieval, profile update, logout |
| `201 Created`               | A new resource was created                    | User registration                                |
| `400 Bad Request`           | Request data failed validation                | Invalid registration or profile data             |
| `401 Unauthorized`          | Authentication failed or is missing           | Invalid credentials or expired token             |
| `403 Forbidden`             | Authenticated user lacks permission           | Future permission-controlled operations          |
| `404 Not Found`             | Requested endpoint or resource does not exist | Invalid API path or missing resource             |
| `500 Internal Server Error` | Unexpected server error                       | Unhandled backend failure                        |

---

# 15. API Error Response Standards

Validation errors are returned as field-based JSON objects.

Example:

```json
{
    "email": [
        "Enter a valid email address."
    ]
}
```

Authentication errors may use the following structure:

```json
{
    "detail": "Authentication credentials were not provided."
}
```

The API must not expose:

* Database passwords
* Django secret keys
* Password hashes
* Internal server paths
* Sensitive configuration values
* Stack traces in production

---

# 16. Postman Verification

The implemented registration endpoint has been tested using Postman.

## Test Configuration

| Setting         | Value                                         |
| --------------- | --------------------------------------------- |
| Method          | `POST`                                        |
| URL             | `http://127.0.0.1:8000/api/v1/auth/register/` |
| Authentication  | None                                          |
| Content Type    | `application/json`                            |
| Expected Status | `201 Created`                                 |

## Verified Request

```json
{
    "email": "admin@atlas.com",
    "first_name": "Wilson",
    "last_name": "Mutinda",
    "password": "SecurePassword123!",
    "password_confirm": "SecurePassword123!"
}
```

## Verified Response

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

## Verification Result

```text
PASS
```

---

# 17. API Implementation Rules

Every new Identity API endpoint must follow this implementation process:

```text
Business Requirement
        ↓
Functional Requirement
        ↓
Use Case
        ↓
Database Design
        ↓
API Specification
        ↓
Validation Rules
        ↓
Permission Design
        ↓
Serializer
        ↓
API View
        ↓
URL Configuration
        ↓
Automated Tests
        ↓
Postman Verification
        ↓
Vue Integration
        ↓
Documentation Update
        ↓
Git Commit
```

No Identity endpoint should be considered complete until it has been:

1. Documented.
2. Implemented.
3. Tested automatically.
4. Verified in Postman.
5. Integrated into the Vue frontend.
6. Updated in the implementation-status document.
7. Committed to Git.

---

# 18. Related Documentation

| Document                        | Purpose                                  |
| ------------------------------- | ---------------------------------------- |
| `README.md`                     | Identity module introduction             |
| `01-overview.md`                | Identity scope and responsibilities      |
| `02-business-requirements.md`   | Business requirements                    |
| `03-functional-requirements.md` | Required system behavior                 |
| `04-use-cases.md`               | User workflows                           |
| `05-database.md`                | User database design                     |
| `07-validation-rules.md`        | Input and business validation            |
| `08-permissions.md`             | Authentication and authorization         |
| `09-testing.md`                 | Automated and Postman tests              |
| `10-implementation-status.md`   | Implementation progress                  |
| `11-changelog.md`               | Documentation and implementation history |

---

# 19. Approval

| Role           | Name                   | Status  | Date |
| -------------- | ---------------------- | ------- | ---- |
| Product Owner  | Wilson Kilonzo Mutinda | Pending | —    |
| Lead Developer | Wilson Kilonzo Mutinda | Pending | —    |

---

**Document Version:** `0.1.0`
**Module:** Identity
**Document:** API Specification
**Status:** Draft
**Last Updated:** July 31, 2026
