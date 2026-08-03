---
document: Development Setup Guide
project: Atlas Business Suite
document_id: ATLAS-DEVOPS-001
version: 1.0.0
status: Approved
author: Wilson Mutinda
created: 2026-07-28
last_updated: 2026-07-28
---

# Development Setup Guide

> "A consistent development environment ensures every engineer builds Atlas the same way."

---

# Table of Contents

1. Purpose
2. Development Environment
3. Required Software
4. Project Structure
5. Backend Setup
6. Frontend Setup
7. Database Setup
8. Environment Variables
9. Running Atlas
10. Coding Standards
11. Troubleshooting
12. Revision History

---

# 1. Purpose

This document defines the official development environment for Atlas Business Suite.

Every developer working on Atlas should follow this guide to ensure a consistent, reliable, and reproducible development setup.

---

# 2. Development Environment

Operating System

- Ubuntu 24.04 LTS (Recommended)

Programming Languages

- Python 3.12+
- TypeScript 5+

Frameworks

- Django
- Django REST Framework
- Vue 3
- Vite

Database

- PostgreSQL

Version Control

- Git

Code Editor

- Visual Studio Code

---

# 3. Required Software

The following software must be installed before working on Atlas.

- Python
- pip
- Node.js
- npm
- PostgreSQL
- Git
- Visual Studio Code

Recommended VS Code Extensions

- Python
- Pylance
- Vue Official
- ESLint
- Prettier
- GitLens
- Markdown All in One
- Markdown Preview Enhanced
- Error Lens

---

# 4. Project Structure

ATLAS/

backend/

frontend/

docs/

infrastructure/

scripts/

README.md

LICENSE

CHANGELOG.md

---

# 5. Backend Setup

The backend is built using Django and Django REST Framework.

Future setup steps include:

- Create Python virtual environment
- Install project dependencies
- Configure Django
- Configure Django REST Framework
- Configure JWT Authentication
- Configure CORS
- Configure logging

---

# 6. Frontend Setup

The frontend is built using Vue 3 and TypeScript.

Future setup steps include:

- Initialize Vue project
- Configure TypeScript
- Install Pinia
- Configure Vue Router
- Install Axios
- Configure Tailwind CSS

---

# 7. Database Setup

Atlas uses PostgreSQL.

Database responsibilities include:

- Data persistence
- Relationships
- Transactions
- Constraints
- Indexes

Development databases should be isolated from production databases.

---

# 8. Environment Variables

Sensitive configuration shall never be committed to Git.

Environment variables include:

- SECRET_KEY
- DEBUG
- DATABASE_URL
- ALLOWED_HOSTS
- CORS_ALLOWED_ORIGINS
- JWT_SECRET
- EMAIL_CONFIGURATION

These values will be stored in a `.env` file.

---

# 9. Running Atlas

Backend

- Activate virtual environment
- Start Django development server

Frontend

- Install dependencies
- Start Vite development server

Both services should be running during development.

---

# 10. Coding Standards

Atlas follows these engineering standards.

Backend

- SOLID Principles
- DRY
- Clean Architecture
- Services contain business logic
- Thin Views
- Reusable Models

Frontend

- Reusable Components
- Composition API
- Strong Typing
- Modular Structure

General

- Meaningful commit messages
- Clear naming conventions
- Documentation-first mindset
- Feature-based development

---

# 11. Troubleshooting

Common issues include:

- Python virtual environment not activated
- PostgreSQL service not running
- Missing environment variables
- Incorrect Node.js version
- Port conflicts

Developers should verify software versions before troubleshooting application code.

---

# 12. Revision History

| Version | Date | Author | Summary |
|----------|------------|----------------|--------------------------------|
| 1.0.0 | 2026-07-28 | Wilson Mutinda | Initial Development Setup Guide created. |