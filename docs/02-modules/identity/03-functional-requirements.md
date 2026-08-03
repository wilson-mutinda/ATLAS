# Identity Module — Functional Requirements

## 1. Document Information

| Item             | Details                                                  |
| ---------------- | -------------------------------------------------------- |
| Document Name    | Functional Requirements                                  |
| Module           | Identity                                                 |
| Document Path    | `docs/02-modules/identity/03-functional-requirements.md` |
| Document Version | `0.1.0`                                                  |
| Status           | Draft                                                    |
| Last Updated     | July 29, 2026                                            |

---

## 2. Purpose

This document defines the functional behavior required from the Atlas Identity module.

The requirements describe what the Identity module must do from the perspective of users, client applications, and other Atlas modules.

These requirements provide the implementation contract for Identity features. Each approved requirement must be reflected in the database design, Django models, serializers, API views, URL configuration, automated tests, Postman tests, frontend integration, and implementation-status documentation.

---

## 3. Functional Requirement Status

| Requirement Area               | Status      |
| ------------------------------ | ----------- |
| Custom User Model              | Implemented |
| User Registration              | Implemented |
| User Login                     | Planned     |
| JWT Access Token Issuance      | Planned     |
| JWT Refresh Token Issuance     | Planned     |
| Token Refresh                  | Planned     |
| Authenticated User Profile     | Planned     |
| User Profile Update            | Planned     |
| User Logout                    | Planned     |
| Password Change                | Planned     |
| Password Reset                 | Planned     |
| User Account Status Management | Planned     |
| Role-Based Access Control      | Future      |

---

# 4. User Account Requirements

## FR-IDENTITY-001 — Custom User Model

**Priority:** Critical
**Status:** Implemented

The system shall use a custom Django User model as the primary authentication model for Atlas Business Suite.

The custom User model shall:

* Use email as the primary user identifier.
* Store the user's first name.
* Store the user's last name.
* Store a securely hashed password.
* Store user account status information.
* Support Django administrative functions.
* Support authentication through Django and Django REST Framework.
* Support future Atlas authorization requirements.

The Atlas project shall define the custom user model through:

```python
AUTH_USER_MODEL = "identity.User"
```

The custom User model shall be configured before production user data is created.

---

## FR-IDENTITY-002 — Email as User Identity

**Priority:** Critical
**Status:** Implemented

The system shall use an email address as the unique identifier for each Atlas user.

The system shall:

* Require an email address during registration.
* Reject registration requests without an email address.
* Reject duplicate email addresses.
* Normalize email addresses using the User model and serializer validation process.
* Use the email address during login.
* Allow the email address to identify the authenticated user.

The system shall not require a username for Atlas authentication.

---

## FR-IDENTITY-003 — User Account Creation

**Priority:** Critical
**Status:** Implemented

The system shall allow an unauthenticated client to create a new Atlas user account.

The registration process shall:

1. Receive user registration information.
2. Validate the submitted information.
3. Verify that the email address is not already registered.
4. Verify that the password confirmation matches the password.
5. Create a new User record.
6. Hash the password using Django's password-management system.
7. Store the new user in PostgreSQL.
8. Return a successful registration response.

The registration endpoint shall be:

```text
POST /api/v1/auth/register/
```

The registration endpoint shall not require JWT authentication.

---

## FR-IDENTITY-004 — Secure Password Storage

**Priority:** Critical
**Status:** Implemented

The system shall never store a user's password as plain text.

When a user account is created or a password is changed, the system shall use Django's password-hashing mechanism.

The system shall:

* Use `create_user()` or `set_password()` when setting a password.
* Store only the generated password hash.
* Never return a password in an API response.
* Never return a password hash in an API response.
* Never expose password values through serializers intended for API responses.

---

# 5. Registration Requirements

## FR-IDENTITY-005 — Registration Request Data

**Priority:** Critical
**Status:** Implemented

The registration API shall accept the following fields:

| Field              | Required | Type   | Description                         |
| ------------------ | -------: | ------ | ----------------------------------- |
| `email`            |      Yes | String | User's unique email address         |
| `first_name`       |      Yes | String | User's first name                   |
| `last_name`        |      Yes | String | User's last name                    |
| `password`         |      Yes | String | User's chosen password              |
| `password_confirm` |      Yes | String | Confirmation of the chosen password |

Example request:

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

## FR-IDENTITY-006 — Registration Validation

**Priority:** Critical
**Status:** Implemented

Before creating a user account, the system shall validate all registration data.

The system shall:

* Verify that all required fields are present.
* Verify that the email address has a valid format.
* Verify that the email address is unique.
* Verify that the password is provided.
* Verify that `password` and `password_confirm` are identical.
* Apply Django password validation rules.
* Reject invalid registration data.
* Return validation errors using Django REST Framework's standard error-response format.

A user account shall not be created when validation fails.

---

## FR-IDENTITY-007 — Successful Registration Response

**Priority:** Critical
**Status:** Implemented

When registration succeeds, the system shall return:

```http
HTTP 201 Created
```

The response shall contain:

* A success message.
* The new user's unique identifier.
* The user's email address.
* The user's first name.
* The user's last name.

Example response:

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

The response shall not contain:

* The password.
* The password confirmation.
* The password hash.
* Internal authentication data.
* Administrative-only user information.

---

# 6. Login Requirements

## FR-IDENTITY-008 — User Login

**Priority:** Critical
**Status:** Planned

The system shall allow a registered and active user to authenticate using an email address and password.

The login endpoint shall be:

```text
POST /api/v1/auth/login/
```

The login request shall contain:

| Field      | Required | Type   | Description           |
| ---------- | -------: | ------ | --------------------- |
| `email`    |      Yes | String | Registered user email |
| `password` |      Yes | String | User password         |

Example request:

```json
{
    "email": "admin@atlas.com",
    "password": "SecurePassword123!"
}
```

The system shall:

1. Validate the request data.
2. Find the user using the supplied email address.
3. Verify the supplied password.
4. Verify that the user account is active.
5. Generate JWT authentication tokens.
6. Return the authentication tokens and approved user information.

---

## FR-IDENTITY-009 — Login Success Response

**Priority:** Critical
**Status:** Planned

When authentication succeeds, the system shall return:

```http
HTTP 200 OK
```

The response shall contain:

* An access token.
* A refresh token.
* Basic authenticated-user information.

The exact response contract shall be defined in:

```text
06-api-specification.md
```

The system shall not return:

* The user's password.
* The user's password hash.
* Internal authentication fields.

---

## FR-IDENTITY-010 — Invalid Login Handling

**Priority:** Critical
**Status:** Planned

When the supplied credentials are invalid, the system shall reject the login request.

The system shall:

* Return an authentication failure response.
* Avoid revealing whether the email address exists.
* Avoid revealing whether the password was incorrect.
* Return a consistent error message for invalid credentials.

The system shall not issue access or refresh tokens when authentication fails.

---

## FR-IDENTITY-011 — Inactive User Login

**Priority:** High
**Status:** Planned

The system shall prevent inactive user accounts from receiving authentication tokens.

If a user's account is inactive:

* Login shall be rejected.
* No access token shall be issued.
* No refresh token shall be issued.
* The user shall not be authenticated.

---

# 7. JWT Requirements

## FR-IDENTITY-012 — Access Token Issuance

**Priority:** Critical
**Status:** Planned

After successful authentication, the system shall issue a JWT access token.

The access token shall:

* Represent the authenticated Atlas user.
* Be used to access protected API endpoints.
* Have a limited lifetime.
* Be validated by Django REST Framework and Simple JWT.
* Be sent by clients using the HTTP Authorization header.

Example:

```http
Authorization: Bearer <access_token>
```

The access-token lifetime shall be controlled through Atlas environment configuration.

---

## FR-IDENTITY-013 — Refresh Token Issuance

**Priority:** Critical
**Status:** Planned

After successful authentication, the system shall issue a JWT refresh token.

The refresh token shall:

* Allow the client to request a new access token.
* Have a longer lifetime than the access token.
* Be handled securely by the client application.
* Be accepted only by the approved token-refresh endpoint.

---

## FR-IDENTITY-014 — Token Refresh

**Priority:** Critical
**Status:** Planned

The system shall allow a valid refresh token to generate a new access token.

The token-refresh endpoint shall be:

```text
POST /api/v1/auth/token/refresh/
```

The request shall contain:

```json
{
    "refresh": "<refresh_token>"
}
```

The system shall:

* Validate the refresh token.
* Reject expired refresh tokens.
* Reject invalid refresh tokens.
* Issue a new access token when the refresh token is valid.

---

# 8. Authenticated User Requirements

## FR-IDENTITY-015 — Retrieve Current User

**Priority:** High
**Status:** Planned

The system shall allow an authenticated user to retrieve their profile information.

The endpoint shall be:

```text
GET /api/v1/auth/me/
```

The endpoint shall require a valid JWT access token.

The response shall contain approved profile information, including:

* User ID.
* Email address.
* First name.
* Last name.
* Account status.

The response shall not contain password information.

---

## FR-IDENTITY-016 — Update Current User

**Priority:** High
**Status:** Planned

The system shall allow an authenticated user to update permitted profile information.

The endpoint shall be:

```text
PATCH /api/v1/auth/me/
```

The system shall:

* Require JWT authentication.
* Update only approved profile fields.
* Validate submitted values.
* Prevent unauthorized modification of protected fields.
* Return the updated user information.

Password updates shall use the dedicated password-change endpoint and shall not be handled by the profile-update endpoint.

---

# 9. Logout Requirements

## FR-IDENTITY-017 — User Logout

**Priority:** High
**Status:** Planned

The system shall provide a logout endpoint.

The endpoint shall be:

```text
POST /api/v1/auth/logout/
```

The final logout design shall define whether refresh-token blacklisting is enabled.

If token blacklisting is implemented, the system shall:

* Accept the user's refresh token.
* Validate the refresh token.
* Add the token to the blacklist.
* Prevent the blacklisted token from being used again.

The client application shall remove locally stored authentication data after a successful logout.

---

# 10. Password Management Requirements

## FR-IDENTITY-018 — Change Password

**Priority:** High
**Status:** Planned

The system shall allow an authenticated user to change their password.

The endpoint shall be:

```text
POST /api/v1/auth/password/change/
```

The system shall:

* Require JWT authentication.
* Require the current password.
* Require a new password.
* Require new-password confirmation.
* Verify the current password.
* Verify that the new password and confirmation match.
* Apply Django password validation.
* Hash the new password before storage.
* Never return password information.

---

## FR-IDENTITY-019 — Password Reset Request

**Priority:** High
**Status:** Planned

The system shall allow a user to request a password-reset process.

The endpoint shall be:

```text
POST /api/v1/auth/password/reset/
```

The system shall:

* Accept an email address.
* Process the request securely.
* Avoid revealing whether the submitted email is registered.
* Generate a secure password-reset process.
* Support future email-service integration.

---

## FR-IDENTITY-020 — Password Reset Confirmation

**Priority:** High
**Status:** Planned

The system shall allow a user to confirm a password reset using a valid reset mechanism.

The system shall:

* Validate the reset information.
* Require a new password.
* Require password confirmation.
* Apply Django password validation.
* Hash the new password before storage.
* Reject invalid or expired reset information.

---

# 11. Authorization Requirements

## FR-IDENTITY-021 — Protected API Access

**Priority:** Critical
**Status:** Partially Implemented

Protected Atlas API endpoints shall require valid authentication.

The default Atlas API configuration shall use:

```python
"rest_framework.permissions.IsAuthenticated"
```

Unauthenticated requests to protected endpoints shall be rejected.

Public endpoints shall explicitly declare:

```python
AllowAny
```

Examples of public Identity endpoints:

* User registration.
* User login.
* Token refresh.
* Password-reset request.
* Password-reset confirmation.

---

## FR-IDENTITY-022 — Current User Identification

**Priority:** Critical
**Status:** Planned

For authenticated requests, the system shall make the current user available through:

```python
request.user
```

Other Atlas modules shall use the authenticated user identity when ownership, permissions, audit records, or user-specific data are required.

---

# 12. Account Status Requirements

## FR-IDENTITY-023 — Active User Status

**Priority:** High
**Status:** Planned

The system shall maintain a user account status.

The system shall:

* Allow active accounts to authenticate.
* Prevent inactive accounts from authenticating.
* Prevent inactive accounts from accessing protected Atlas resources.
* Preserve user records when accounts are deactivated unless deletion is explicitly approved.

---

# 13. Integration Requirements

## FR-IDENTITY-024 — Atlas Module Integration

**Priority:** Critical
**Status:** Planned

The Identity module shall provide authenticated-user information to other Atlas modules.

Other modules shall:

* Use the Atlas custom User model.
* Reference the user model through `settings.AUTH_USER_MODEL`.
* Avoid creating separate authentication systems.
* Avoid storing duplicate user credentials.
* Use the authenticated user from `request.user`.

The Identity module shall remain responsible for user credentials and authentication.

---

# 14. API Versioning Requirements

## FR-IDENTITY-025 — Versioned API Endpoints

**Priority:** High
**Status:** Implemented

All public Identity API endpoints shall use the Atlas API version prefix:

```text
/api/v1/
```

Examples:

```text
/api/v1/auth/register/
/api/v1/auth/login/
/api/v1/auth/token/refresh/
/api/v1/auth/me/
```

Breaking API changes shall require a new API version rather than silently changing an existing public API contract.

---

# 15. Functional Requirement Traceability

| Requirement     | Feature                     | Implementation Status |
| --------------- | --------------------------- | --------------------- |
| FR-IDENTITY-001 | Custom User model           | Implemented           |
| FR-IDENTITY-002 | Email identity              | Implemented           |
| FR-IDENTITY-003 | User registration           | Implemented           |
| FR-IDENTITY-004 | Secure password storage     | Implemented           |
| FR-IDENTITY-005 | Registration request data   | Implemented           |
| FR-IDENTITY-006 | Registration validation     | Implemented           |
| FR-IDENTITY-007 | Registration response       | Implemented           |
| FR-IDENTITY-008 | User login                  | Planned               |
| FR-IDENTITY-009 | Login response              | Planned               |
| FR-IDENTITY-010 | Invalid login handling      | Planned               |
| FR-IDENTITY-011 | Inactive-user handling      | Planned               |
| FR-IDENTITY-012 | Access token                | Planned               |
| FR-IDENTITY-013 | Refresh token               | Planned               |
| FR-IDENTITY-014 | Token refresh               | Planned               |
| FR-IDENTITY-015 | Retrieve current user       | Planned               |
| FR-IDENTITY-016 | Update current user         | Planned               |
| FR-IDENTITY-017 | Logout                      | Planned               |
| FR-IDENTITY-018 | Password change             | Planned               |
| FR-IDENTITY-019 | Password-reset request      | Planned               |
| FR-IDENTITY-020 | Password-reset confirmation | Planned               |
| FR-IDENTITY-021 | Protected API access        | Partially Implemented |
| FR-IDENTITY-022 | Current-user identification | Planned               |
| FR-IDENTITY-023 | Account status              | Planned               |
| FR-IDENTITY-024 | Atlas module integration    | Planned               |
| FR-IDENTITY-025 | API versioning              | Implemented           |

---

# 16. Approval

| Role           | Name                   | Status  | Date |
| -------------- | ---------------------- | ------- | ---- |
| Product Owner  | Wilson Kilonzo Mutinda | Pending | —    |
| Lead Developer | Wilson Kilonzo Mutinda | Pending | —    |

---

**Document Version:** `0.1.0`
**Module:** Identity
**Document:** Functional Requirements
**Status:** Draft
**Last Updated:** July 29, 2026
