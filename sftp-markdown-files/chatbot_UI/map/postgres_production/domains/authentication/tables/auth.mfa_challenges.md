# mfa_challenges

**Database:** postgres_production
**Schema:** auth
**Description:** This table stores metadata about multi-factor authentication (MFA) challenge requests within the authentication system, as indicated by its location in the auth schema and the database comment. The table appears to track individual MFA challenge instances that are generated when users attempt to authenticate, though specific challenge details cannot be determined without column information. As a standalone table with no foreign key relationships, it likely serves as an audit log or temporary storage for MFA challenge sessions within the broader authentication workflow.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | uuid | NO | Purpose unclear from available data, though given the context of an MFA challenges table, this likely serves as the primary identifier for multi-factor authentication challenge instances. |
| factor_id | uuid | NO | References the specific authentication factor (such as SMS, TOTP, or hardware token) that this multi-factor authentication challenge is associated with. Links each challenge attempt to its corresponding configured authentication method for the user. |
| created_at | timestamp with time zone | NO | Records the exact moment when a multi-factor authentication challenge was initiated for a user. This timestamp enables tracking of authentication attempt timing and supports security auditing workflows. |
| verified_at | timestamp with time zone | YES | Records the exact moment when a multi-factor authentication challenge was successfully completed by a user. Remains empty until the challenge is verified, serving as both a completion flag and audit timestamp. |
| ip_address | inet | NO | Stores the network address from which a multi-factor authentication challenge was initiated or attempted. This enables security tracking and potential geographic or network-based access controls during the authentication process. |
| otp_code | text | YES | Purpose unclear from available data. Likely stores a temporary numeric or alphanumeric code used for multi-factor authentication verification. |
| web_authn_session_data | jsonb | YES | Stores session-specific data and state information required for WebAuthn authentication ceremonies during multi-factor authentication challenges. Purpose unclear from available data due to lack of sample values. |

## Primary Key

`id`

## Indexes

- `mfa_challenge_created_at_idx`: CREATE INDEX mfa_challenge_created_at_idx ON auth.mfa_challenges USING btree (created_at DESC)
- `mfa_challenges_pkey`: CREATE UNIQUE INDEX mfa_challenges_pkey ON auth.mfa_challenges USING btree (id)

*Generated at: 2025-12-11T22:50:34.510Z*