# Identity Module — Changelog

## [0.4.0] - 2026-08-04

### Added

* Implemented `POST /api/v1/auth/token/refresh/`.
* Added JWT access-token refresh functionality.
* Added automated tests for valid and invalid refresh tokens.

### Verified

* A valid refresh token returns a new access token.
* An invalid refresh token returns `401 Unauthorized`.
* All 8 Identity tests pass successfully.
---
## [0.3.0] - 2026-08-04

### Added

- Implemented `GET /api/v1/auth/me/`.
- Added authenticated user profile retrieval.
- Added automated tests for authenticated profile access.
- Added automated tests for unauthenticated profile access.

### Verified

- Authenticated requests return the current user's profile.
- Requests without a valid access token return `401 Unauthorized`.
- All Identity tests pass successfully.
---

## [0.2.0] - 2026-08-04

### Added

* Implemented the user Login API.
* Added email and password authentication.
* Added JWT access-token generation.
* Added JWT refresh-token generation.
* Added Login API automated tests.

### Verified

* Successful login returns user information and JWT tokens.
* Invalid credentials are rejected.
* Missing password is rejected.
* All four Login tests pass.
---

## Version 0.1.0 — August 3, 2026

### Added

* Identity module documentation structure.
* Module overview and scope.
* Business requirements.
* Functional requirements.
* Identity use cases.
* User database design.
* API specifications.
* Validation rules.
* Authentication and permission rules.
* Testing requirements.
* Implementation status tracking.

### Implemented

* Custom Django User model.
* Email-based user authentication.
* PostgreSQL user storage.
* Django admin integration.
* User registration serializer.
* User registration API.
* Password hashing.
* JWT authentication configuration.
* Health API.
* Postman testing for user registration.

### Next

* Implement the user Login API.
* Generate JWT access and refresh tokens.
* Test login using Postman.
* Add automated Django tests.

---

**Current Version:** `0.1.0`
**Module Status:** In Progress
**Last Updated:** August 3, 2026
