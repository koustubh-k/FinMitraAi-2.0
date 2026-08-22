# Authentication & Authorization Architecture

## Overview
FinMitra implements a provider-independent authentication system using JWT access tokens and stateful refresh tokens stored in PostgreSQL.

## Token Lifecycle
- **Access Tokens**: Short-lived (15 minutes). Stateless. Validated via secret key `JWT_SECRET_KEY`.
- **Refresh Tokens**: Long-lived (30 days). Stateful. Stored as SHA256 hashes in the `refresh_tokens` table.
- **Refresh Token Rotation**: Upon using a refresh token to obtain a new access token, the old refresh token is marked as revoked, and a new one is issued.

## Password Hashing
- Algorithm: `Argon2id` (via `passlib`)
- Validated manually to ensure minimum complexity (e.g. 8+ characters).

## Authorization
- Uses `get_current_user` FastAPI dependency.
- Endpoints enforce Resource Ownership checking `resource.user_id == current_user.id`.
- The system returns `403 Forbidden` or `404 Not Found` upon unauthorized access.

## Future Strategy
This system abstracts the core logic to potentially migrate to Clerk or OAuth in future phases, allowing seamless swapping of the `AuthService` dependency.
