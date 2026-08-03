# Identity Module — Database Design

## 1. Document Information

| Item            | Details          |
| --------------- | ---------------- |
| Module          | Identity         |
| Document        | Database Design  |
| Document File   | `05-database.md` |
| Database        | PostgreSQL       |
| ORM             | Django ORM       |
| Current Version | `0.1.0`          |
| Status          | Active           |
| Last Updated    | July 30, 2026    |

---

## 2. Purpose

This document defines the database design for the Atlas Identity module.

The Identity module is responsible for storing and managing user identity information required for authentication and access to Atlas Business Suite.

The current database design includes a custom Django User model that uses an email address as the primary login identity.

This document describes:

* The database technology used by Atlas.
* The Identity module's database responsibilities.
* The User model.
* User model fields.
* Database constraints.
* Authentication-related database behavior.
* Model relationships.
* Data-integrity rules.
* Migration history.
* Planned database changes.

---

## 3. Database Technology

Atlas Business Suite uses PostgreSQL as its primary relational database.

| Technology        | Purpose                                                      |
| ----------------- | ------------------------------------------------------------ |
| PostgreSQL        | Persistent storage for Atlas application data                |
| Django ORM        | Database abstraction, model management, and query operations |
| Django Migrations | Version-controlled database schema changes                   |
| Psycopg           | PostgreSQL database adapter for Python                       |

The Atlas development database is configured through environment variables.

Database credentials must not be stored directly in the source code.

The database configuration is loaded from the backend `.env` file.

---

## 4. Database Scope

The Identity module owns user identity and authentication-related data.

The Identity module currently manages:

* User accounts.
* User email addresses.
* User first names.
* User last names.
* User passwords.
* User account status.
* User permissions.
* User account creation timestamps.
* User login timestamps.

The Identity module does not own:

* Organization information.
* Organization membership.
* Company information.
* Business branches.
* Inventory data.
* Sales data.
* Financial data.
* Hotel data.

These records will be managed by their respective Atlas modules.

---

## 5. User Model

### 5.1 Model Name

```text
User
```

### 5.2 Django Model Path

```text
backend/apps/identity/models.py
```

### 5.3 Database Table

The database table is generated and managed by Django.

The expected table name is:

```text
identity_user
```

### 5.4 Model Purpose

The User model represents an individual who can access Atlas Business Suite.

Each User record stores the information required to identify and authenticate an Atlas user.

Atlas uses a custom User model instead of Django's default User model.

The custom model allows Atlas to use email as the primary authentication identity and provides flexibility for future user-management requirements.

---

## 6. User Field Definitions

| Field          | Data Type     | Required | Unique | Purpose                                                                 |
| -------------- | ------------- | -------- | ------ | ----------------------------------------------------------------------- |
| `id`           | Big Integer   | Yes      | Yes    | Unique identifier for each user                                         |
| `email`        | Email         | Yes      | Yes    | Primary user identity and login identifier                              |
| `first_name`   | String        | Yes      | No     | User's first name                                                       |
| `last_name`    | String        | Yes      | No     | User's last name                                                        |
| `password`     | Hashed String | Yes      | No     | Securely stores the user's password hash                                |
| `is_active`    | Boolean       | Yes      | No     | Determines whether the account can access Atlas                         |
| `is_staff`     | Boolean       | Yes      | No     | Determines whether the user can access the Django administration system |
| `is_superuser` | Boolean       | Yes      | No     | Indicates whether the user has all system permissions                   |
| `last_login`   | Date and Time | No       | No     | Stores the user's most recent successful login time                     |
| `date_joined`  | Date and Time | Yes      | No     | Stores the date and time when the user account was created              |

---

## 7. Field Descriptions

### 7.1 `id`

The `id` field is the primary key for the User model.

It uniquely identifies each user record.

The value is generated automatically by Django and PostgreSQL.

The `id` field is used when other Atlas models need to create relationships with a user.

Example:

```text
User ID: 1
```

---

### 7.2 `email`

The `email` field stores the user's primary email address.

Atlas uses email as the user's authentication identity.

The email address must be unique.

Two Atlas users cannot have the same email address.

Example:

```text
admin@atlas.com
```

The email field is used during:

* User registration.
* User login.
* User identification.
* Account recovery.
* Future account notifications.

---

### 7.3 `first_name`

The `first_name` field stores the user's first name.

Example:

```text
Wilson
```

The first name may be displayed in the Atlas dashboard, user profile, reports, notifications, and other user-facing interfaces.

---

### 7.4 `last_name`

The `last_name` field stores the user's last name.

Example:

```text
Mutinda
```

The last name may be combined with the first name to display the user's full name.

---

### 7.5 `password`

The `password` field stores a secure password hash.

Atlas must never store a user's plain-text password.

Passwords are processed using Django's password-management system before being stored in PostgreSQL.

The original password cannot be retrieved from the database.

During login, Django compares the submitted password with the stored password hash.

---

### 7.6 `is_active`

The `is_active` field determines whether a user account is active.

| Value   | Meaning                                                |
| ------- | ------------------------------------------------------ |
| `True`  | The user account is active and may authenticate        |
| `False` | The user account is disabled and must not authenticate |

This field allows an account to be disabled without permanently deleting the user's data.

---

### 7.7 `is_staff`

The `is_staff` field determines whether a user can access the Django administration interface.

| Value   | Meaning                                                               |
| ------- | --------------------------------------------------------------------- |
| `True`  | The user may access the Django administration interface if authorized |
| `False` | The user cannot access the Django administration interface            |

---

### 7.8 `is_superuser`

The `is_superuser` field identifies users with full Django permission access.

Superuser access is intended for authorized system administrators.

| Value   | Meaning                                |
| ------- | -------------------------------------- |
| `True`  | The user has all Django permissions    |
| `False` | The user has only assigned permissions |

---

### 7.9 `last_login`

The `last_login` field stores the date and time of the user's most recent successful login.

The field may be empty when a user has not logged in.

---

### 7.10 `date_joined`

The `date_joined` field stores the date and time when the user account was created.

This field supports:

* User-account auditing.
* User-account reporting.
* Account-history analysis.
* Future administrative features.

---

## 8. Database Constraints

The User model must enforce the following database and application rules.

| Rule ID           | Constraint                                                      |
| ----------------- | --------------------------------------------------------------- |
| `DB-IDENTITY-001` | Every User record must have a unique primary key                |
| `DB-IDENTITY-002` | Every User record must have an email address                    |
| `DB-IDENTITY-003` | Every user email address must be unique                         |
| `DB-IDENTITY-004` | User passwords must not be stored as plain text                 |
| `DB-IDENTITY-005` | A user account must have an active-status value                 |
| `DB-IDENTITY-006` | A user account must have a creation timestamp                   |
| `DB-IDENTITY-007` | User identity records must be managed through Django migrations |

---

## 9. Authentication Database Design

Atlas uses email as the primary user identity.

The User model is configured as the project's authentication model.

The Atlas Django configuration contains:

```python
AUTH_USER_MODEL = "identity.User"
```

The authentication username field is:

```text
email
```

The email address is used to identify a user during authentication.

Passwords are managed using Django's built-in password-hashing system.

The database does not store:

```text
Plain-text passwords
```

The database stores:

```text
Secure password hashes
```

---

## 10. Model Relationships

The User model currently has no custom business-domain relationships.

Future Atlas modules are expected to reference the User model.

Planned relationships may include:

```text
User
 ├── Organization Membership
 ├── Organization Role
 ├── Audit Log
 ├── Inventory Activity
 ├── Sales Transaction
 ├── Financial Transaction
 └── Hotel Activity
```

These relationships will be documented and implemented by their respective modules.

Future modules must reference the configured Atlas user model rather than importing the User model directly.

Django relationships should use:

```python
settings.AUTH_USER_MODEL
```

This prevents future problems caused by hard-coded user-model references.

---

## 11. Database Integrity Rules

The following rules protect Identity data integrity.

### Rule 1: Email Uniqueness

Each Atlas user must have a unique email address.

A registration request using an existing email address must be rejected.

---

### Rule 2: Password Security

Passwords must be processed through Django's password-hashing system.

Plain-text passwords must not be stored in PostgreSQL.

Plain-text passwords must not be returned by the API.

---

### Rule 3: User Identification

Each user must have a unique primary key.

Other Atlas modules must use the User model's primary key when creating user relationships.

---

### Rule 4: Migration Control

Database schema changes must be created and applied through Django migrations.

Manual changes to the PostgreSQL schema should be avoided unless they are reviewed and documented.

---

### Rule 5: User Model Stability

The custom User model is a foundational Atlas model.

Changes to authentication fields must be carefully reviewed because other Atlas modules will depend on the User model.

---

## 12. Migration History

The initial Identity migration was created after the custom User model was implemented.

| Migration         | Description                   | Status  |
| ----------------- | ----------------------------- | ------- |
| `0001_initial.py` | Creates the custom User model | Applied |

The migration was successfully applied to the Atlas PostgreSQL database.

The Identity User table is available for application use.

---

## 13. Current Database Status

| Item                             | Status   |
| -------------------------------- | -------- |
| PostgreSQL configured            | Complete |
| Atlas database created           | Complete |
| Atlas database user created      | Complete |
| Django connected to PostgreSQL   | Complete |
| Custom User model created        | Complete |
| User migration created           | Complete |
| User migration applied           | Complete |
| User records stored successfully | Complete |
| User registration tested         | Complete |

---

## 14. Future Database Changes

The following database features are planned but have not yet been implemented.

| Feature                       | Status  |
| ----------------------------- | ------- |
| User profile fields           | Planned |
| User profile image            | Planned |
| Password-reset records        | Planned |
| Refresh-token blacklist       | Planned |
| User login history            | Future  |
| User session records          | Future  |
| User account activity records | Future  |
| Organization membership       | Planned |
| User roles                    | Planned |
| User permissions              | Planned |
| Audit-log relationships       | Planned |

Each future database change must be documented before implementation.

---

## 15. Database Change Procedure

Every Atlas database change must follow this process:

```text
Business Requirement
        ↓
Database Design Documentation
        ↓
Model Design
        ↓
Django Model Implementation
        ↓
Create Migration
        ↓
Review Migration
        ↓
Apply Migration
        ↓
Automated Tests
        ↓
Postman Verification
        ↓
Documentation Update
        ↓
Git Commit
```

Database changes must not be implemented without documenting their purpose and expected behavior.

---

## 16. Database Design Status

**Current Status:** Active

**Current Database:** PostgreSQL

**Current Model:**

```text
User
```

**Completed Database Work:**

```text
Custom User model
Email-based authentication identity
PostgreSQL configuration
Initial Identity migration
User record creation
```

**Next Planned Database Work:**

```text
Review database requirements for the Login feature.
```

---

## 17. Approval

| Role           | Name                   | Status  | Date |
| -------------- | ---------------------- | ------- | ---- |
| Product Owner  | Wilson Kilonzo Mutinda | Pending | —    |
| Lead Developer | Wilson Kilonzo Mutinda | Pending | —    |

---

**Document Version:** `0.1.0`

**Module:** Identity

**Document:** Database Design

**Status:** Draft

**Last Updated:** July 30, 2026
