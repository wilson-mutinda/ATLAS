# Identity Module — Use Cases

## 1. Document Information

| Item             | Details                                    |
| ---------------- | ------------------------------------------ |
| Document Name    | Use Cases                                  |
| Module           | Identity                                   |
| Document Path    | `docs/02-modules/identity/04-use-cases.md` |
| Document Version | `0.1.0`                                    |
| Status           | Draft                                      |
| Last Updated     | July 30, 2026                              |

---

## 2. Purpose

This document defines how users and Atlas client applications interact with the Identity module.

Each use case describes:

* The actor involved.
* The purpose of the interaction.
* The conditions required before the interaction begins.
* The normal flow of actions.
* Alternative or failure flows.
* The expected result.

The use cases in this document are derived from:

* `02-business-requirements.md`
* `03-functional-requirements.md`

Implementation must follow the approved use cases before code is written.

---

## 3. Actors

| Actor               | Description                                                                        |
| ------------------- | ---------------------------------------------------------------------------------- |
| Visitor             | A person who does not have an authenticated Atlas session                          |
| Registered User     | A person with an existing Atlas user account                                       |
| Authenticated User  | A registered user with a valid JWT access token                                    |
| Atlas Client        | The Vue frontend, Postman, or another approved application consuming the Atlas API |
| Atlas Identity API  | The Django REST Framework API responsible for identity and authentication          |
| Atlas Administrator | An authorized administrator managing users through Django Admin                    |
| Email Service       | A future service responsible for delivering password-reset messages                |

---

## 4. Use Case Summary

| ID              | Use Case                    | Primary Actor       | Status                |
| --------------- | --------------------------- | ------------------- | --------------------- |
| UC-IDENTITY-001 | Register a User             | Visitor             | Implemented           |
| UC-IDENTITY-002 | Log In                      | Registered User     | Planned               |
| UC-IDENTITY-003 | Refresh an Access Token     | Atlas Client        | Planned               |
| UC-IDENTITY-004 | View Current User Profile   | Authenticated User  | Planned               |
| UC-IDENTITY-005 | Update Current User Profile | Authenticated User  | Planned               |
| UC-IDENTITY-006 | Log Out                     | Authenticated User  | Planned               |
| UC-IDENTITY-007 | Change Password             | Authenticated User  | Planned               |
| UC-IDENTITY-008 | Request Password Reset      | Registered User     | Planned               |
| UC-IDENTITY-009 | Confirm Password Reset      | Registered User     | Planned               |
| UC-IDENTITY-010 | Manage User Accounts        | Atlas Administrator | Partially Implemented |

---

# 5. UC-IDENTITY-001 — Register a User

## 5.1 Use Case Information

| Item             | Details                       |
| ---------------- | ----------------------------- |
| Use Case ID      | `UC-IDENTITY-001`             |
| Use Case Name    | Register a User               |
| Primary Actor    | Visitor                       |
| Supporting Actor | Atlas Identity API            |
| Priority         | Critical                      |
| Status           | Implemented                   |
| API Endpoint     | `POST /api/v1/auth/register/` |

---

## 5.2 Goal

Allow a visitor to create a new Atlas user account using an email address, first name, last name, and password.

---

## 5.3 Preconditions

Before this use case begins:

* The Atlas backend is running.
* The PostgreSQL database is available.
* The Identity module is installed.
* The registration endpoint is available.
* The visitor is not required to provide a JWT access token.

---

## 5.4 Trigger

The visitor submits a completed registration form through the Atlas Vue frontend, Postman, or another approved API client.

---

## 5.5 Main Success Flow

1. The visitor enters an email address.
2. The visitor enters a first name.
3. The visitor enters a last name.
4. The visitor enters a password.
5. The visitor enters the same password as confirmation.
6. The Atlas client sends a `POST` request to:

```text
/api/v1/auth/register/
```

7. The Identity API receives the registration request.
8. The registration serializer validates the submitted data.
9. The system verifies that the email address is valid.
10. The system verifies that the email address is not already registered.
11. The system verifies that the password and password confirmation match.
12. The system applies the configured password-validation rules.
13. The system creates the user account.
14. Django hashes the user's password.
15. The new user is stored in PostgreSQL.
16. The Identity API returns:

```http
HTTP 201 Created
```

17. The Atlas client displays the successful registration result.

---

## 5.6 Example Request

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

## 5.7 Example Success Response

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

## 5.8 Alternative Flows

### A. Required Information Is Missing

1. The visitor submits the registration request without one or more required fields.
2. The serializer detects the missing information.
3. The system returns:

```http
HTTP 400 Bad Request
```

4. The response identifies the affected field or fields.
5. No user account is created.

---

### B. Email Address Is Invalid

1. The visitor submits an incorrectly formatted email address.
2. The serializer rejects the email address.
3. The system returns:

```http
HTTP 400 Bad Request
```

4. No user account is created.

---

### C. Email Address Already Exists

1. The visitor submits an email address already associated with an Atlas account.
2. The system detects the duplicate email address.
3. The system returns:

```http
HTTP 400 Bad Request
```

4. No additional user account is created.

---

### D. Passwords Do Not Match

1. The visitor submits different values for `password` and `password_confirm`.
2. The serializer detects the mismatch.
3. The system returns:

```http
HTTP 400 Bad Request
```

4. No user account is created.

---

### E. Password Fails Validation

1. The visitor submits a password that does not satisfy the configured password rules.
2. Django's password-validation system rejects the password.
3. The system returns:

```http
HTTP 400 Bad Request
```

4. No user account is created.

---

## 5.9 Postconditions

After successful completion:

* A new User record exists in PostgreSQL.
* The user's email address is stored as the account identifier.
* The user's password is stored as a secure hash.
* The plain-text password is not stored.
* The password is not returned in the API response.
* The new user can proceed to the login process when the Login feature is implemented.

---

# 6. UC-IDENTITY-002 — Log In

## 6.1 Use Case Information

| Item             | Details                    |
| ---------------- | -------------------------- |
| Use Case ID      | `UC-IDENTITY-002`          |
| Use Case Name    | Log In                     |
| Primary Actor    | Registered User            |
| Supporting Actor | Atlas Identity API         |
| Priority         | Critical                   |
| Status           | Planned                    |
| API Endpoint     | `POST /api/v1/auth/login/` |

---

## 6.2 Goal

Allow a registered and active Atlas user to authenticate using an email address and password.

---

## 6.3 Preconditions

Before this use case begins:

* The user has an existing Atlas account.
* The user account is active.
* The Atlas backend is running.
* The PostgreSQL database is available.
* The Login API has been implemented.

---

## 6.4 Trigger

The registered user submits their email address and password.

---

## 6.5 Main Success Flow

1. The user enters their registered email address.
2. The user enters their password.
3. The Atlas client sends a `POST` request to:

```text
/api/v1/auth/login/
```

4. The Identity API validates the request data.
5. The system locates the user using the submitted email address.
6. The system verifies the submitted password.
7. The system verifies that the user account is active.
8. The system generates a JWT access token.
9. The system generates a JWT refresh token.
10. The Identity API returns:

```http
HTTP 200 OK
```

11. The Atlas client securely stores the authentication information according to the approved frontend security design.
12. The user is treated as authenticated.
13. The user can access protected Atlas resources.

---

## 6.6 Alternative Flows

### A. Email or Password Is Missing

1. The user submits incomplete login information.
2. The system rejects the request.
3. The system returns:

```http
HTTP 400 Bad Request
```

4. No tokens are issued.

---

### B. Invalid Credentials

1. The submitted email address or password is incorrect.
2. The system rejects the authentication request.
3. The system returns:

```http
HTTP 401 Unauthorized
```

4. The response does not reveal whether the email address or password was incorrect.
5. No tokens are issued.

---

### C. User Account Is Inactive

1. The submitted credentials belong to an inactive account.
2. The system rejects the login request.
3. No authentication tokens are issued.
4. The user cannot access protected Atlas resources.

---

## 6.7 Postconditions

After successful completion:

* The user has a valid JWT access token.
* The user has a valid JWT refresh token.
* The user can access protected Atlas API endpoints.
* The authenticated user is available to backend views through `request.user`.

---

# 7. UC-IDENTITY-003 — Refresh an Access Token

## 7.1 Use Case Information

| Item             | Details                            |
| ---------------- | ---------------------------------- |
| Use Case ID      | `UC-IDENTITY-003`                  |
| Use Case Name    | Refresh an Access Token            |
| Primary Actor    | Atlas Client                       |
| Supporting Actor | Atlas Identity API                 |
| Priority         | Critical                           |
| Status           | Planned                            |
| API Endpoint     | `POST /api/v1/auth/token/refresh/` |

---

## 7.2 Goal

Allow the Atlas client to obtain a new access token using a valid refresh token.

---

## 7.3 Preconditions

* The user previously logged in successfully.
* The Atlas client has a valid refresh token.
* The refresh token has not expired.
* The refresh token has not been invalidated.

---

## 7.4 Main Success Flow

1. The Atlas client detects that the access token is expired or is about to expire.
2. The client sends the refresh token to:

```text
/api/v1/auth/token/refresh/
```

3. The Identity API validates the refresh token.
4. The system generates a new access token.
5. The API returns:

```http
HTTP 200 OK
```

6. The Atlas client replaces the previous access token.
7. The client continues making authenticated requests.

---

## 7.5 Alternative Flows

### A. Refresh Token Is Missing

1. The client sends a request without a refresh token.
2. The system rejects the request.
3. The system returns:

```http
HTTP 400 Bad Request
```

---

### B. Refresh Token Is Invalid or Expired

1. The client submits an invalid or expired refresh token.
2. The system rejects the request.
3. The system returns:

```http
HTTP 401 Unauthorized
```

4. The client clears invalid authentication data.
5. The client directs the user to log in again.

---

## 7.6 Postconditions

After successful completion:

* A new access token is available.
* The user remains authenticated.
* Protected API requests can continue.

---

# 8. UC-IDENTITY-004 — View Current User Profile

## 8.1 Use Case Information

| Item             | Details                   |
| ---------------- | ------------------------- |
| Use Case ID      | `UC-IDENTITY-004`         |
| Use Case Name    | View Current User Profile |
| Primary Actor    | Authenticated User        |
| Supporting Actor | Atlas Identity API        |
| Priority         | High                      |
| Status           | Planned                   |
| API Endpoint     | `GET /api/v1/auth/me/`    |

---

## 8.2 Goal

Allow an authenticated user to retrieve their own Atlas profile information.

---

## 8.3 Preconditions

* The user has a valid JWT access token.
* The user account is active.
* The `/api/v1/auth/me/` endpoint is available.

---

## 8.4 Main Success Flow

1. The authenticated user opens their Atlas profile.
2. The Atlas client sends:

```http
GET /api/v1/auth/me/
Authorization: Bearer <access_token>
```

3. The Identity API validates the JWT access token.
4. The system identifies the current user.
5. The system retrieves the user's approved profile information.
6. The API returns:

```http
HTTP 200 OK
```

7. The Atlas client displays the user's profile.

---

## 8.5 Alternative Flow — Missing or Invalid Token

1. The client sends no token or sends an invalid token.
2. The system rejects the request.
3. The API returns:

```http
HTTP 401 Unauthorized
```

4. No profile information is returned.

---

## 8.6 Postconditions

After successful completion:

* The user receives their approved profile information.
* No password information is exposed.

---

# 9. UC-IDENTITY-005 — Update Current User Profile

## 9.1 Use Case Information

| Item             | Details                     |
| ---------------- | --------------------------- |
| Use Case ID      | `UC-IDENTITY-005`           |
| Use Case Name    | Update Current User Profile |
| Primary Actor    | Authenticated User          |
| Supporting Actor | Atlas Identity API          |
| Priority         | High                        |
| Status           | Planned                     |
| API Endpoint     | `PATCH /api/v1/auth/me/`    |

---

## 9.2 Goal

Allow an authenticated user to update permitted profile information.

---

## 9.3 Main Success Flow

1. The user edits permitted profile information.
2. The Atlas client sends a `PATCH` request to:

```text
/api/v1/auth/me/
```

3. The request includes a valid JWT access token.
4. The Identity API validates the token.
5. The system identifies the current user.
6. The system validates the submitted profile information.
7. The system updates permitted fields.
8. The updated user information is stored in PostgreSQL.
9. The API returns:

```http
HTTP 200 OK
```

10. The Atlas client displays the updated profile.

---

## 9.4 Alternative Flows

### A. Invalid Profile Data

1. The user submits invalid information.
2. The system rejects the invalid field values.
3. The API returns:

```http
HTTP 400 Bad Request
```

4. Invalid changes are not saved.

---

### B. Invalid Authentication

1. The request contains no valid JWT access token.
2. The API returns:

```http
HTTP 401 Unauthorized
```

3. No changes are made.

---

## 9.5 Postconditions

After successful completion:

* Approved profile information is updated.
* Password information remains unchanged.
* Protected account fields remain protected.

---

# 10. UC-IDENTITY-006 — Log Out

## 10.1 Use Case Information

| Item             | Details                     |
| ---------------- | --------------------------- |
| Use Case ID      | `UC-IDENTITY-006`           |
| Use Case Name    | Log Out                     |
| Primary Actor    | Authenticated User          |
| Supporting Actor | Atlas Identity API          |
| Priority         | High                        |
| Status           | Planned                     |
| API Endpoint     | `POST /api/v1/auth/logout/` |

---

## 10.2 Goal

Allow an authenticated user to end their Atlas session.

---

## 10.3 Main Success Flow

1. The user selects **Log Out**.
2. The Atlas client sends a logout request.
3. The client provides the required authentication information.
4. The Identity API validates the request.
5. If refresh-token blacklisting is enabled, the system invalidates the submitted refresh token.
6. The API returns a successful logout response.
7. The Atlas client removes locally stored authentication information.
8. The client redirects the user to the login page.

---

## 10.4 Alternative Flow — Invalid Token

1. The client submits invalid authentication information.
2. The system rejects the request.
3. The client clears local authentication information.
4. The user is directed to the login page.

---

## 10.5 Postconditions

After successful completion:

* The client no longer treats the user as authenticated.
* Local authentication information is removed.
* If token blacklisting is enabled, the refresh token cannot be used again.

---

# 11. UC-IDENTITY-007 — Change Password

## 11.1 Use Case Information

| Item             | Details                              |
| ---------------- | ------------------------------------ |
| Use Case ID      | `UC-IDENTITY-007`                    |
| Use Case Name    | Change Password                      |
| Primary Actor    | Authenticated User                   |
| Supporting Actor | Atlas Identity API                   |
| Priority         | High                                 |
| Status           | Planned                              |
| API Endpoint     | `POST /api/v1/auth/password/change/` |

---

## 11.2 Goal

Allow an authenticated user to replace their current password with a new password.

---

## 11.3 Preconditions

* The user is authenticated.
* The user knows their current password.
* The password-change endpoint is available.

---

## 11.4 Main Success Flow

1. The user enters their current password.
2. The user enters a new password.
3. The user confirms the new password.
4. The Atlas client sends the request to:

```text
/api/v1/auth/password/change/
```

5. The Identity API validates the JWT access token.
6. The system verifies the current password.
7. The system verifies that the new password and confirmation match.
8. The system applies Django password validation.
9. The system securely hashes the new password.
10. The system stores the new password hash.
11. The API returns a successful response.

---

## 11.5 Alternative Flows

### A. Current Password Is Incorrect

1. The submitted current password does not match the user's account.
2. The system rejects the request.
3. The password remains unchanged.

---

### B. New Passwords Do Not Match

1. The new password and confirmation differ.
2. The system rejects the request.
3. The password remains unchanged.

---

### C. New Password Fails Validation

1. The new password does not satisfy the configured rules.
2. The system returns a validation error.
3. The password remains unchanged.

---

## 11.6 Postconditions

After successful completion:

* The new password is securely hashed and stored.
* The previous password no longer authenticates the user.
* No password value is returned by the API.

---

# 12. UC-IDENTITY-008 — Request Password Reset

## 12.1 Use Case Information

| Item             | Details                             |
| ---------------- | ----------------------------------- |
| Use Case ID      | `UC-IDENTITY-008`                   |
| Use Case Name    | Request Password Reset              |
| Primary Actor    | Registered User                     |
| Supporting Actor | Atlas Identity API, Email Service   |
| Priority         | High                                |
| Status           | Planned                             |
| API Endpoint     | `POST /api/v1/auth/password/reset/` |

---

## 12.2 Goal

Allow a user who cannot access their account to begin a secure password-reset process.

---

## 12.3 Main Success Flow

1. The user selects **Forgot Password**.
2. The user enters their email address.
3. The Atlas client sends the email address to the password-reset endpoint.
4. The Identity API processes the request.
5. If the email belongs to an eligible user, the system creates a secure password-reset process.
6. The email service sends reset instructions.
7. The API returns a generic success response.

---

## 12.4 Security Requirement

The response shall not reveal whether the submitted email address is registered.

---

## 12.5 Postconditions

After successful completion:

* The user receives password-reset instructions when eligible.
* The system does not expose account-existence information.

---

# 13. UC-IDENTITY-009 — Confirm Password Reset

## 13.1 Use Case Information

| Item             | Details                |
| ---------------- | ---------------------- |
| Use Case ID      | `UC-IDENTITY-009`      |
| Use Case Name    | Confirm Password Reset |
| Primary Actor    | Registered User        |
| Supporting Actor | Atlas Identity API     |
| Priority         | High                   |
| Status           | Planned                |

---

## 13.2 Goal

Allow a user to create a new password using valid password-reset information.

---

## 13.3 Main Success Flow

1. The user opens the password-reset link or approved reset interface.
2. The user enters a new password.
3. The user confirms the new password.
4. The Atlas client submits the reset information.
5. The system validates the reset information.
6. The system validates the new password.
7. The system securely hashes the new password.
8. The new password hash is stored.
9. The API returns a successful response.
10. The user proceeds to log in using the new password.

---

## 13.4 Alternative Flows

### A. Reset Information Is Invalid

1. The reset information is invalid.
2. The system rejects the request.
3. The password remains unchanged.

---

### B. Reset Information Has Expired

1. The reset information is no longer valid.
2. The system rejects the request.
3. The user must begin a new password-reset request.

---

## 13.5 Postconditions

After successful completion:

* The new password is securely stored.
* The previous password no longer authenticates the user.
* The user can log in using the new password.

---

# 14. UC-IDENTITY-010 — Manage User Accounts

## 14.1 Use Case Information

| Item             | Details               |
| ---------------- | --------------------- |
| Use Case ID      | `UC-IDENTITY-010`     |
| Use Case Name    | Manage User Accounts  |
| Primary Actor    | Atlas Administrator   |
| Supporting Actor | Django Admin          |
| Priority         | Medium                |
| Status           | Partially Implemented |

---

## 14.2 Goal

Allow authorized Atlas administrators to view and manage user accounts through Django Admin.

---

## 14.3 Main Success Flow

1. The administrator signs in to Django Admin.
2. The administrator opens the Identity User management page.
3. The administrator views user records.
4. The administrator performs an authorized management action.
5. Django validates the action.
6. The system saves the approved changes.

---

## 14.4 Postconditions

After successful completion:

* Approved user-account changes are stored.
* Unauthorized users cannot access administrative functions.

---

# 15. Use Case Relationships

```text
Visitor
    │
    └── Register a User
            │
            ▼
      Registered User
            │
            └── Log In
                    │
                    ▼
            Authenticated User
            ├── View Profile
            ├── Update Profile
            ├── Change Password
            └── Log Out

Registered User
    │
    └── Request Password Reset
            │
            ▼
      Confirm Password Reset
            │
            ▼
         Log In
```

---

# 16. Use Case Implementation Order

The Identity use cases shall be implemented in the following order:

| Order | Use Case                              | Status   |
| ----: | ------------------------------------- | -------- |
|     1 | Register a User                       | Complete |
|     2 | Log In                                | Next     |
|     3 | Refresh an Access Token               | Planned  |
|     4 | View Current User Profile             | Planned  |
|     5 | Update Current User Profile           | Planned  |
|     6 | Log Out                               | Planned  |
|     7 | Change Password                       | Planned  |
|     8 | Request Password Reset                | Planned  |
|     9 | Confirm Password Reset                | Planned  |
|    10 | Expand Administrative User Management | Future   |

---

# 17. Traceability

| Use Case        | Functional Requirements             |
| --------------- | ----------------------------------- |
| UC-IDENTITY-001 | FR-IDENTITY-001 to FR-IDENTITY-007  |
| UC-IDENTITY-002 | FR-IDENTITY-008 to FR-IDENTITY-011  |
| UC-IDENTITY-003 | FR-IDENTITY-012 to FR-IDENTITY-014  |
| UC-IDENTITY-004 | FR-IDENTITY-015 and FR-IDENTITY-022 |
| UC-IDENTITY-005 | FR-IDENTITY-016                     |
| UC-IDENTITY-006 | FR-IDENTITY-017                     |
| UC-IDENTITY-007 | FR-IDENTITY-018                     |
| UC-IDENTITY-008 | FR-IDENTITY-019                     |
| UC-IDENTITY-009 | FR-IDENTITY-020                     |
| UC-IDENTITY-010 | FR-IDENTITY-023                     |

---

# 18. Approval

| Role           | Name                   | Status  | Date |
| -------------- | ---------------------- | ------- | ---- |
| Product Owner  | Wilson Kilonzo Mutinda | Pending | —    |
| Lead Developer | Wilson Kilonzo Mutinda | Pending | —    |

---

**Document Version:** `0.1.0`
**Module:** Identity
**Document:** Use Cases
**Status:** Draft
**Last Updated:** July 30, 2026
