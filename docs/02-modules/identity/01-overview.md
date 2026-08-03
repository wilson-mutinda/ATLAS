# Identity Module Overview

## 1. Purpose

The Identity module provides the user identity and authentication foundation for Atlas Business Suite.

It is responsible for creating and managing user accounts, identifying authenticated users, and providing the authentication mechanisms required to access protected Atlas resources.

The module establishes the answer to the question:

> Who is the current Atlas user?

Other Atlas modules may use the authenticated user's identity, but they must not manage user credentials or authentication logic independently.

---

## 2. Scope

The Identity module covers the following areas:

* User account creation
* User identity management
* Email-based authentication
* Password management
* JWT-based authentication
* Authenticated user information
* User account status
* Authentication-related API endpoints

The module will provide a consistent authentication foundation for all Atlas business domains.

---

## 3. In Scope

The following capabilities are within the responsibility of the Identity module.

### 3.1 User Registration

The system must allow a new user to create an Atlas account using:

* Email address
* First name
* Last name
* Password
* Password confirmation

The system must validate the submitted information before creating the user.

---

### 3.2 User Authentication

The system will allow a registered user to authenticate using:

* Email address
* Password

A successful login will provide JWT authentication tokens.

---

### 3.3 JWT Token Management

The module will support:

* Access tokens
* Refresh tokens
* Access-token renewal
* Authentication of protected API requests

JWT tokens will be used by the Vue frontend when communicating with protected Atlas APIs.

---

### 3.4 Authenticated User Profile

An authenticated user will be able to:

* Retrieve their profile information
* View their email address
* View their first name
* View their last name
* Update permitted profile information

---

### 3.5 Password Management

The module will support:

* Secure password storage
* Password changes for authenticated users
* Password-reset requests
* Password-reset confirmation

Passwords must never be stored or returned as plain text.

---

### 3.6 User Account Status

The system will maintain user account status through the Django user model.

User accounts may be:

* Active
* Inactive
* Staff accounts
* Superuser accounts

Inactive users must not be allowed to authenticate.

---

## 4. Out of Scope

The following responsibilities are outside the Identity module:

* Organization creation
* Organization membership
* Company profiles
* Business branches
* Inventory management
* Product management
* Sales management
* Customer management
* Supplier management
* Financial management
* Hotel operations
* Module-specific business permissions

These capabilities will be implemented in their respective Atlas modules.

---

## 5. Module Architecture

The Identity module follows the Atlas backend architecture.

```text
Client Application
        │
        ▼
Vue Frontend
        │
        ▼
Identity API
        │
        ▼
API Views
        │
        ▼
Serializers
        │
        ▼
User Model
        │
        ▼
PostgreSQL Database
```

For authenticated requests:

```text
Vue Frontend
        │
        │ Authorization: Bearer <access_token>
        ▼
Django REST Framework
        │
        ▼
JWT Authentication
        │
        ▼
Authenticated User
        │
        ▼
Protected Atlas API
```

---

## 6. Backend Structure

The Identity backend application is located at:

```text
backend/apps/identity/
```

The expected structure is:

```text
apps/identity/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── serializers.py
├── tests.py
├── views.py
├── migrations/
│   └── __init__.py
└── api/
    ├── __init__.py
    ├── urls.py
    └── views.py
```

### Component Responsibilities

| Component        | Responsibility                                          |
| ---------------- | ------------------------------------------------------- |
| `models.py`      | Defines the custom Atlas User model                     |
| `serializers.py` | Validates and transforms API data                       |
| `api/views.py`   | Handles Identity API requests                           |
| `api/urls.py`    | Defines Identity API routes                             |
| `admin.py`       | Registers and configures the User model in Django admin |
| `tests.py`       | Contains automated Identity tests                       |
| `migrations/`    | Stores database migration history                       |

---

## 7. User Identity Design

Atlas uses a custom Django User model.

The user's email address is the primary login identity.

The system does not use a traditional username for authentication.

The main user identity fields are:

| Field          | Purpose                                                       |
| -------------- | ------------------------------------------------------------- |
| `id`           | Unique database identifier                                    |
| `email`        | Unique user identity and login credential                     |
| `first_name`   | User's first name                                             |
| `last_name`    | User's last name                                              |
| `password`     | Securely hashed user password                                 |
| `is_active`    | Indicates whether the user account can authenticate           |
| `is_staff`     | Indicates whether the user can access Django admin            |
| `is_superuser` | Indicates whether the user has full administrative privileges |
| `date_joined`  | Records when the user account was created                     |

The complete database design is documented in:

```text
05-database.md
```

---

## 8. Authentication Design

Atlas uses JSON Web Tokens (JWT) for API authentication.

The authentication flow will operate as follows:

```text
User submits email and password
                │
                ▼
Identity Login API
                │
                ▼
Credentials are validated
                │
                ▼
JWT access token is generated
                │
                ▼
JWT refresh token is generated
                │
                ▼
Tokens are returned to the Vue frontend
                │
                ▼
Frontend uses the access token
                │
                ▼
Protected Atlas APIs identify the user
```

The JWT implementation uses:

```text
djangorestframework-simplejwt
```

---

## 9. API Base Path

All Identity API endpoints use the following base path:

```text
/api/v1/auth/
```

The current and planned endpoints include:

| Method  | Endpoint                        | Status      |
| ------- | ------------------------------- | ----------- |
| `POST`  | `/api/v1/auth/register/`        | Implemented |
| `POST`  | `/api/v1/auth/login/`           | Planned     |
| `POST`  | `/api/v1/auth/token/refresh/`   | Planned     |
| `POST`  | `/api/v1/auth/logout/`          | Planned     |
| `GET`   | `/api/v1/auth/me/`              | Planned     |
| `PATCH` | `/api/v1/auth/me/`              | Planned     |
| `POST`  | `/api/v1/auth/password/change/` | Planned     |
| `POST`  | `/api/v1/auth/password/reset/`  | Planned     |

The complete API contracts are documented in:

```text
06-api-specification.md
```

---

## 10. Module Dependencies

The Identity module depends on:

* Django
* Django REST Framework
* PostgreSQL
* `django-environ`
* `djangorestframework-simplejwt`

The module uses the following Atlas configuration:

* Custom user model
* PostgreSQL database
* JWT authentication
* Environment-based configuration
* Versioned API URLs

---

## 11. Modules That Depend on Identity

The following Atlas modules are expected to use the Identity module:

| Module        | Identity Dependency                     |
| ------------- | --------------------------------------- |
| Organizations | Organization ownership and membership   |
| Dashboard     | Current-user information                |
| Inventory     | Record ownership and audit information  |
| Sales         | Sales-user identification               |
| Finance       | Financial-record ownership and approval |
| Hotel         | Staff and user identification           |

The Identity module must remain independent of business-domain logic.

For example, Identity may provide the authenticated user, but Inventory is responsible for determining whether that user can perform inventory operations.

---

## 12. Design Principles

The Identity module follows these principles:

### 12.1 Email Is the User Identity

Email addresses are used as the primary user identifier.

### 12.2 Passwords Are Never Stored as Plain Text

Passwords are processed using Django's password-hashing system.

### 12.3 Authentication Is Centralized

Authentication logic belongs to the Identity module and must not be duplicated across business modules.

### 12.4 APIs Are Versioned

Identity APIs use the `/api/v1/` version prefix.

### 12.5 Authentication and Authorization Are Separate

Authentication answers:

> Who is the user?

Authorization answers:

> What is the user allowed to do?

The Identity module provides authentication. More detailed business permissions may be implemented by other Atlas modules.

### 12.6 Sensitive Information Is Not Returned

API responses must never return:

* Passwords
* Password hashes
* Secret keys
* JWT signing configuration
* Internal authentication details

---

## 13. Current Implementation State

The following Identity functionality is currently implemented:

* Custom User model
* Email-based user identity
* User registration serializer
* User registration API
* PostgreSQL user storage
* Django admin registration
* JWT authentication configuration
* Postman registration testing

The following functionality remains to be implemented:

* User login
* JWT token issuance
* Token refresh
* Authenticated user profile
* User profile update
* Logout
* Password change
* Password reset
* Role-based access control

---

## 14. Related Documentation

| Document                        | Purpose                                     |
| ------------------------------- | ------------------------------------------- |
| `README.md`                     | Module introduction and documentation index |
| `02-business-requirements.md`   | Business needs                              |
| `03-functional-requirements.md` | Required system behavior                    |
| `04-use-cases.md`               | User workflows                              |
| `05-database.md`                | User database design                        |
| `06-api-specification.md`       | API contracts                               |
| `07-validation-rules.md`        | Validation rules                            |
| `08-permissions.md`             | Authentication and authorization            |
| `09-testing.md`                 | Testing requirements                        |
| `10-implementation-status.md`   | Implementation progress                     |
| `11-changelog.md`               | Change history                              |

---

## 15. Approval

| Role           | Status  | Date |
| -------------- | ------- | ---- |
| Product Owner  | Pending | —    |
| Lead Developer | Pending | —    |

---

**Document:** `01-overview.md`
**Module:** Identity
**Version:** `0.1.0`
**Status:** Draft
**Last Updated:** July 29, 2026
