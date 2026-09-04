# Identity Module - Validation Rules

## 1. Purpose
This document defines the validation rules used by the Identity module.
Validation protects data quality, prevents invalid user accounts, and ensures that authentication requests contain the required information.

---
## 2. User Registration Validation
| Field                 | Required              | Validation Rule                                                   |
| --------------------- | --------------------- | ----------------------------------------------------------------- |
| `email`               | Yes                   | Must be a valid email address                                     |
| `email`               | Yes                   | Must be unique                                                    |
| `first_name`          | Yes                   | Must not be empty                                                 |
| `last_name`           | Yes                   | Must not be empty                                                 |
| `password`            | Yes                   | Must satisfy Django password validation                           |
| `password_confirm`    | Yes                   | Must match `password`                                             |

### Registration Rules
1. A user cannot register without an email address.
2. The email address must use a valid email format.
3. An email address can belong to only one Atlas user.
4. The password and password_confirmation  must match.
5. The password must pass the configured Django password validators.
6. Passwords  must never be returned in API responses.
7. Passwords must be stored using Django's password-hashing system.

---

## 3. User Login Validation
| Field             | Required      | Validation Rule                               |
| ----------------- | ------------- | --------------------------------------------- |
| `email`           | Yes           | Must be valid email address                   |
| `password`        | Yes           | Must not be empty                             |

### Login Rules
1. Both email and password are required.
2. The submitted credentials must belong to an existing user.
3. The user account must be active.
4. Invalid credentials must not reveal whether the email address exists.
5. A successful login must return valid JWT access and refresh tokens.

---
## 4. Profile Validation
| Field             | Required        | Validation Rule                         |
| ----------------- | --------------- | --------------------------------------- |
| `email`           | Yes             | Must remain valid and unique            |
| `first_name`      | Yes             | Must not be empty                       |
| `last_name`       | Yes             | Must not be empty                       |

### Profile Rules
1. Only authenticated users can access their profiles.
2. Users can update only permitted profile fields.
3. A user cannot update another user's profile therough the `/me/` endpoint.
4. Any updated emal address must remain unique.

---

## 5. Password Change Validation
| Field                  | Required         | Validation Rule                        |
| ---------------------- | ---------------- | -------------------------------------- |
| `current_password`     | Yes              | Must match the user's current password | 
| `new_password`         | Yes              | Must pass Django password validation   |
| `new_password_Confirm` | Yes              | Must match `new_password`              |

### Password Change Rules
1. The current password must be correct.
2. The new password must pass Django's configured password validators.
3. The new password and confirmation must match.
4. PAssword values must never be returned in API resoonses.

---
## 6. Password Reset Validation
| Field         | Required      | Validation Rule               |
| ------------- | ------------- | ----------------------------- | 
| `email`       | Yes           | Must use a valid email format |

### Password Reset Rules
1. The request must contain  a avalid email address.
2. The response must not reveal whether the email address is registered.
3. Password-reset tokens must be temporary and secure.
4. A reset token must not be accepted after it expires.

---
## 7. JWT Validation
| Item                              | Validation Rule                                   |
| --------------------------------- | ------------------------------------------------- |
| Access token                      | Must be valid and unexpired                       |
| Refresh token                     | Must be valid and unexpired                       |
| Protected endpoint                | Requires a valid access token                     |
| Authorization header              | Must use the Bearer token format                  |

Expected authorization format:
```http
Authorization: Bearer <access_token>
```
---

## 8. Validation Error Format
Validation errors should be returned using standard Django REST Framework responses.
Example: 
```json
{
    "email": [
        "A user with this email already exists."
    ]
}
```
Password mismatch example:
```json
{
    password_mismatch: [
        "Passwords do not match."
    ]
}
```
---

## 9. Logout Validation

| Field        | Rule                                   |
| ------------ | -------------------------------------- |
| `refresh`    | Required                               |
| `refresh`    | Must be a valid JWT refresh token      |
| Access token | Required in the `Authorization` header |

The refresh token must belong to a valid Atlas user and must not already be blacklisted.


## 10. Implementation Status
| Validation Area                       | Status                            |
| ------------------------------------- | --------------------------------- |
| Email format validation               | Implemented                       |
| Email uniqueness                      | Implemented                       |
| Required registration fields          | Implemented                       |
| Password confirmation                 | Implemented                       |
| Password hashing                      | Implemented                       |
| Django password validation            | Implemented                       |
| Login validation                      | Planned                           |
| Profile validation                    | Planned                           |
| Password-reset validation             | Planned                           |
| JWT validation                        | Configured                        |

---

## 11. Review Checklist
Before approving an Identity feature, confir that:
* [ ] Required fields are validated.
* [ ] Invalid data is rejected.
* [ ] Duplicate email adresses are rejected.
* [ ] Password confirmation  is checked.
* [ ] Passwords are never returned by the API.
* [ ] Protected endpoints require authentication.
* [ ] Validation errors are clear and consistent.

---
**Document Version:** `0.1.0`
**Module**: Identity
**Status**: Draft
**Last Updated**: August 7, 2026
