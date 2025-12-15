# mfa_amr_claims

**Database:** postgres_production
**Schema:** auth
**Description:** This table stores Authentication Method Reference (AMR) claims for multi-factor authentication, tracking the specific authentication methods used during user login sessions. Based on the database comment, it appears to be part of an authentication system that needs to maintain records of how users verified their identity for security and compliance purposes. The table currently contains no data and has no foreign key relationships, suggesting it may be a logging or audit table that operates independently within the auth schema.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| session_id | uuid | NO | Uniquely identifies the authentication session for which multi-factor authentication method claims are being tracked. Links MFA verification records to specific user login sessions. |
| created_at | timestamp with time zone | NO | Records the exact date and time when a multi-factor authentication method claim was first established in the system. This timestamp enables tracking of when each authentication factor was initially registered or verified for audit and security purposes. |
| updated_at | timestamp with time zone | NO | Records the timestamp when each multi-factor authentication method claim record was last modified. Tracks the most recent update to authentication method verification data for auditing and synchronization purposes. |
| authentication_method | text | NO | Stores the specific method used to authenticate a user during multi-factor authentication, such as SMS, email, authenticator app, or biometric verification. Purpose unclear from available data due to lack of sample values. |
| id | uuid | NO | Purpose unclear from available data as no sample values or descriptive comments are provided for this identifier column in the multi-factor authentication claims table. |

## Primary Key

`id`

## Indexes

- `amr_id_pk`: CREATE UNIQUE INDEX amr_id_pk ON auth.mfa_amr_claims USING btree (id)
- `mfa_amr_claims_session_id_authentication_method_pkey`: CREATE UNIQUE INDEX mfa_amr_claims_session_id_authentication_method_pkey ON auth.mfa_amr_claims USING btree (session_id, authentication_method)

*Generated at: 2025-12-11T22:50:24.623Z*