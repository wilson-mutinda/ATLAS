# Identity Module — Database Design

## Database

| Item        | Value           |
| ----------- | --------------- |
| Database    | PostgreSQL      |
| ORM         | Django ORM      |
| Application | Django          |
| Model       | `identity.User` |
| Table       | `identity_user` |

---

## User Model

| Field          | Type          | Required | Unique |
| -------------- | ------------- | -------- | ------ |
| `id`           | Big Integer   | Yes      | Yes    |
| `email`        | Email         | Yes      | Yes    |
| `first_name`   | String        | Yes      | No     |
| `last_name`    | String        | Yes      | No     |
| `password`     | Hashed String | Yes      | No     |
| `is_active`    | Boolean       | Yes      | No     |
| `is_staff`     | Boolean       | Yes      | No     |
| `is_superuser` | Boolean       | Yes      | No     |
| `last_login`   | DateTime      | No       | No     |
| `date_joined`  | DateTime      | Yes      | No     |

---

## Authentication

Atlas uses:

```python
AUTH_USER_MODEL = "identity.User"
```

The authentication identity is:

```text
email
```

Passwords are stored using Django's password-hashing system.

Plain-text passwords are never stored.

---

## Relationships

The Identity User model currently has no custom business-domain relationships.

Other Atlas modules should reference the configured user model using:

```python
settings.AUTH_USER_MODEL
```

---

## Migration

Initial migration:

```text
0001_initial.py
```

Status:

```text
Applied
```

---

## Database Status

```text
PostgreSQL:        Connected
User model:        Implemented
Migration:         Applied
User storage:      Working
```

---

## Future Changes

Potential future additions:

* Organization membership
* Roles
* Permissions
* Login history
* Account activity
* Session management
