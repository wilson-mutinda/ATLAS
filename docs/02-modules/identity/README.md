# Identity Module

## 1. Module Information

| Item                  | Details                     |
| --------------------- | --------------------------- |
| Module Name           | Identity                    |
| Module Code           | `IDENTITY`                  |
| Module Path           | `backend/apps/identity/`    |
| Documentation Path    | `docs/02-modules/identity/` |
| Current Version       | `0.1.0`                     |
| Module Status         | In Progress                 |
| Backend Framework     | Django 6                    |
| API Framework         | Django REST Framework       |
| Authentication Method | JSON Web Tokens (JWT)       |
| Database              | PostgreSQL                  |

---

## 2. Purpose

The Identity module manages user identity, authentication, and access to Atlas Business Suite.

It provides the foundation through which users are registered, authenticated, identified, and granted access to protected Atlas resources.

All Atlas modules that require knowledge of the current user will depend on the Identity module.

The Identity module is responsible for establishing **who the user is**. Business domains such as Inventory, Sales, Finance, and Hotel will use the authenticated user information but will not manage user credentials directly.

---

## 3. Module Objectives

The Identity module must:

* Create and manage Atlas user accounts.
* Use email addresses as the primary user identity.
* Securely store user passwords using Django's password-hashing system.
* Authenticate users using email and password.
* Issue JWT access and refresh tokens.
* Allow authenticated users to retrieve their profile information.
* Allow users to update permitted profile information.
* Support secure password changes.
* Support password-reset workflows.
* Provide a foundation for future role-based access control.

---

## 4. Current Implementation

The following features have already been implemented:

| Feature                                  | Status   |
| ---------------------------------------- | -------- |
| Custom Django User model                 | Complete |
| Email-based authentication               | Complete |
| User registration serializer             | Complete |
| User registration API                    | Complete |
| Password hashing                         | Complete |
| PostgreSQL user storage                  | Complete |
| Django admin integration                 | Complete |
| JWT package configuration                | Complete |
| Default API authentication configuration | Complete |
| Registration testing in Postman          | Complete |

The following features have not yet been implemented:

| Feature                             | Status  |
| ----------------------------------- | ------- |
| User login                          | Planned |
| JWT token issuance                  | Planned |
| JWT token refresh endpoint          | Planned |
| Authenticated user profile endpoint | Planned |
| User profile update                 | Planned |
| User logout                         | Planned |
| Password change                     | Planned |
| Password reset                      | Planned |
| Role-based access control           | Future  |

---

## 5. Implemented API

### User Registration

| Property                | Value                    |
| ----------------------- | ------------------------ |
| HTTP Method             | `POST`                   |
| Endpoint                | `/api/v1/auth/register/` |
| Authentication Required | No                       |
| Current Status          | Complete                 |
| Expected Success Status | `201 Created`            |

The registration endpoint creates a new Atlas user and stores the user in PostgreSQL.

The user's password is processed through Django's password-hashing system and is not stored as plain text.

### Example Request

```json
{
    "email": "admin@atlas.com",
    "first_name": "Wilson",
    "last_name": "Mutinda",
    "password": "SecurePassword123!",
    "password_confirm": "SecurePassword123!"
}
```

### Example Success Response

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

## 6. Planned API Endpoints

| Method  | Endpoint                        | Description                               | Status   |
| ------- | ------------------------------- | ----------------------------------------- | -------- |
| `POST`  | `/api/v1/auth/register/`        | Create a new user account                 | Complete |
| `POST`  | `/api/v1/auth/login/`           | Authenticate a user                       | Planned  |
| `POST`  | `/api/v1/auth/token/refresh/`   | Generate a new access token               | Planned  |
| `POST`  | `/api/v1/auth/logout/`          | End the current user session              | Planned  |
| `GET`   | `/api/v1/auth/me/`              | Retrieve the authenticated user's profile | Planned  |
| `PATCH` | `/api/v1/auth/me/`              | Update the authenticated user's profile   | Planned  |
| `POST`  | `/api/v1/auth/password/change/` | Change the current user's password        | Planned  |
| `POST`  | `/api/v1/auth/password/reset/`  | Request a password-reset process          | Planned  |

---

## 7. Module Boundaries

### Responsibilities

The Identity module owns:

* User accounts
* User email addresses
* User names
* User credentials
* Password management
* Authentication
* JWT token generation
* JWT token validation
* Authenticated user identity
* User account status

### Responsibilities Outside This Module

The Identity module does not own:

* Organization information
* Company information
* Organization membership
* Business branches
* Inventory records
* Product records
* Sales records
* Financial records
* Hotel operations
* Business-specific permissions

These responsibilities belong to their respective Atlas modules.

---

## 8. Module Dependencies

The Identity module depends on:

* Django
* Django REST Framework
* PostgreSQL
* `djangorestframework-simplejwt`

The Identity module is expected to be used by:

* Organizations
* Dashboard
* Inventory
* Sales
* Finance
* Hotel
* Future Atlas modules

---

## 9. Documentation Structure

| File                            | Description                                          |
| ------------------------------- | ---------------------------------------------------- |
| `README.md`                     | Identity module introduction and documentation index |
| `01-overview.md`                | Module scope, architecture, and responsibilities     |
| `02-business-requirements.md`   | Business requirements addressed by Identity          |
| `03-functional-requirements.md` | Required system behavior                             |
| `04-use-cases.md`               | User interactions and workflows                      |
| `05-database.md`                | User model and database design                       |
| `06-api-specification.md`       | API contracts and endpoint definitions               |
| `07-validation-rules.md`        | Input validation and business rules                  |
| `08-permissions.md`             | Authentication and authorization rules               |
| `09-testing.md`                 | Automated and Postman test specifications            |
| `10-implementation-status.md`   | Current implementation progress                      |
| `11-changelog.md`               | Documentation and implementation history             |

---

## 10. Development Workflow

Every Identity feature must follow the Atlas engineering workflow:

```text
Requirement
    ↓
Documentation
    ↓
Database Design
    ↓
Django Model
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

No new Identity feature should be implemented before its requirements and API behavior have been documented.

---

## 11. Current Development Position

The following work has been completed:

1. The custom User model was created.
2. The User model was configured as the Atlas authentication model.
3. The Identity database migration was created.
4. The migration was applied successfully to PostgreSQL.
5. The registration serializer was implemented.
6. The registration API was implemented.
7. The registration endpoint was connected to the Atlas API URL structure.
8. User registration was successfully tested using Postman.

The next feature to document and implement is:

```text
User Login
```

The Login feature must be documented in the Identity module documentation before implementation begins.

---

## 12. Module Status

**Current Status:** In Progress

**Completed Feature:**

```text
User Registration
```

**Next Feature:**

```text
User Login
```

**Module Completion Condition:**

The Identity module will be considered complete when all approved Identity requirements have been implemented, tested, documented, integrated into the Vue frontend, and committed to Git.

---

## 13. Related Project Documentation

* [Atlas Product Charter](../../00-foundation/)
* [Atlas Architecture Documentation](../../01-architecture/)
* [Core Module Documentation](../core/)
* [Atlas API Documentation](../../03-api/)
* [Atlas Database Documentation](../../04-database/)
* [Atlas UI/UX Documentation](../../05-ui-ux/)
* [Atlas DevOps Documentation](../../06-devops/)

---

## 14. Approval

| Role           | Name                   | Status  | Date |
| -------------- | ---------------------- | ------- | ---- |
| Product Owner  | Wilson Kilonzo Mutinda | Pending | —    |
| Lead Developer | Wilson Kilonzo Mutinda | Pending | —    |

---

**Document Version:** `0.1.0`
**Module:** Identity
**Status:** Draft
**Last Updated:** July 29, 2026
