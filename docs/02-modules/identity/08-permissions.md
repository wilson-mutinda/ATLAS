# Identity Module — Permissions

## 1. Purpose

This document defines who can access Identity module endpoints and what actions they are allowed to perform.

Atlas uses JWT authentication to identify users and protect restricted resources.

---

## 2. Access Levels

| Access Level  | Description                                 |
| ------------- | ------------------------------------------- |
| Public        | No authentication is required               |
| Authenticated | A valid JWT access token is required        |
| Administrator | Reserved for future administrative features |

---

## 3. Endpoint Permissions

| Endpoint                        | Method  | Access        |
| ------------------------------- | ------- | ------------- |
| `/api/v1/auth/register/`        | `POST`  | Public        |
| `/api/v1/auth/login/`           | `POST`  | Public        |
| `/api/v1/auth/token/refresh/`   | `POST`  | Public        |
| `/api/v1/auth/me/`              | `GET`   | Authenticated |
| `/api/v1/auth/me/`              | `PATCH` | Authenticated |
| `/api/v1/auth/logout/`          | `POST`  | Authenticated |
| `/api/v1/auth/password/change/` | `POST`  | Authenticated |
| `/api/v1/auth/password/reset/`  | `POST`  | Public        |

---

## 4. Public Access

The following actions do not require a JWT access token:

* Registering a new user.
* Logging in.
* Refreshing an access token.
* Requesting a password reset.

Public endpoints must still validate all submitted data.

---

## 5. Authenticated Access

The following actions require a valid JWT access token:

* Viewing the current user's profile.
* Updating the current user's profile.
* Logging out.
* Changing the current user's password.

The access token must be included in the request header:

```text
Authorization: Bearer <access_token>
```

If the token is missing, invalid, or expired, the API must deny access.

---

## 6. User Access Rules

An authenticated user:

* Can view their own profile.
* Can update permitted fields in their own profile.
* Can change their own password.
* Cannot access or modify another user's profile through the `/me/` endpoint.
* Cannot perform administrative actions unless granted the required permissions.

---

## 7. Default API Security

Atlas uses the following default permission:

```python
"DEFAULT_PERMISSION_CLASSES": (
    "rest_framework.permissions.IsAuthenticated",
)
```

This means that API endpoints require authentication by default.

Public endpoints must explicitly allow unauthenticated access:

```python
from rest_framework.permissions import AllowAny
```

Example:

```python
permission_classes = [AllowAny]
```

---

## 8. Permission Response

When a user attempts to access a protected endpoint without valid authentication, the API should return:

```json
{
    "detail": "Authentication credentials were not provided."
}
```

Expected HTTP status:

```text
401 Unauthorized
```

---

## 9. Logout Permission

| Endpoint                    | Authentication | Permission               |
| --------------------------- | -------------- | ------------------------ |
| `POST /api/v1/auth/logout/` | Required       | Authenticated users only |

The logout endpoint uses:

```python
IsAuthenticated
```

The client must send:

```text
Authorization: Bearer <access_token>
```


## 10. Future Permissions

The following features are planned for future Atlas versions:

* Role-based access control.
* Organization-level permissions.
* Branch-level permissions.
* Module-specific permissions.
* Custom user roles.
* Permission management through the Atlas administration interface.

These features are outside the current Identity module implementation.

---

## 11. Implementation Status

| Permission Feature              | Status   |
| ------------------------------- | -------- |
| JWT authentication configured   | Complete |
| Default authentication required | Complete |
| Public registration endpoint    | Complete |
| Public login endpoint           | Planned  |
| Authenticated `/me/` endpoint   | Planned  |
| Authenticated logout endpoint   | Planned  |
| Role-based access control       | Future   |

---

## 12. Review Checklist

* [ ] Public endpoints explicitly allow unauthenticated access.
* [ ] Protected endpoints require a valid JWT access token.
* [ ] Users can access only their own profile.
* [ ] Invalid or expired tokens are rejected.
* [ ] Permission failures return the correct HTTP response.
* [ ] Future permissions remain separate from the current implementation.

---

**Document Version:** `0.1.0`
**Module:** Identity
**Status:** Draft
**Last Updated:** August 3, 2026
