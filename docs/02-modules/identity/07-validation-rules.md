# Identity Module — Validation Rules

## Registration

The registration API requires:

* Valid email address
* Unique email address
* First name
* Last name
* Password
* Password confirmation
* Matching passwords
* Password passing Django validation

---

## Login

Login requires:

```text
email
password
```

Invalid credentials return:

```http
401 Unauthorized
```

---

## Profile

The authenticated user may update permitted profile fields.

The email field must remain subject to the configured uniqueness rules.

---

## Password Change

Requires:

```text
current_password
new_password
new_password_confirm
```

Rules:

* Current password must be correct.
* New passwords must match.
* New password must satisfy Django password validation.
* Plain-text passwords must never be stored.

---

## Password Reset

The reset request accepts:

```text
email
```

The API uses a generic response so that it does not reveal whether an account exists.

The confirmation request requires:

```text
uid
token
new_password
new_password_confirm
```

Rules:

* User must exist.
* Reset token must be valid.
* Reset token must not be expired.
* New passwords must match.
* New password must satisfy Django validation.

---

## Validation Status

```text
Registration:       Complete
Login:              Complete
Profile:            Complete
Password Change:    Complete
Password Reset:     Complete
```
