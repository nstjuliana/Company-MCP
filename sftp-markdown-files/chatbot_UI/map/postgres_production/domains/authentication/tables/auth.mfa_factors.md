# mfa_factors

**Database:** postgres_production
**Schema:** auth
**Description:** This table stores multi-factor authentication (MFA) factors within the authentication schema, representing the various authentication methods or devices that users can employ for additional security verification. Based on the table name and database comment indicating it stores "metadata about factors," this table likely maintains configuration and status information for MFA options such as SMS, authenticator apps, or hardware tokens. The table appears to function as a standalone reference for MFA factor definitions, as evidenced by the absence of foreign key relationships, suggesting it may be referenced by other authentication-related tables in the system.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | uuid | NO | Uniquely identifies each multi-factor authentication method configured for user accounts. Serves as the primary reference for tracking and managing individual MFA devices or factors within the authentication system. |
| user_id | uuid | NO | References the unique identifier of the user account that owns the multi-factor authentication factors configured in this table. Establishes the relationship between MFA settings and individual user accounts in the authentication system. |
| friendly_name | text | YES | Purpose unclear from available data. Appears to store an optional user-defined label or display name associated with multi-factor authentication factors. |
| factor_type | USER-DEFINED | NO | Purpose unclear from available data. This appears to store the specific method or technology used for multi-factor authentication within the system's security framework. |
| status | USER-DEFINED | NO | Purpose unclear from available data. Likely indicates the current state or condition of a multi-factor authentication factor, but specific status values cannot be determined without sample data. |
| created_at | timestamp with time zone | NO | Records the exact moment when a multi-factor authentication method was first established for a user account. This timestamp is automatically set when the authentication factor is initially configured and cannot be null. |
| updated_at | timestamp with time zone | NO | Records when the multi-factor authentication factor configuration was last modified. Automatically maintained to track changes to MFA settings for auditing and synchronization purposes. |
| secret | text | YES | The cryptographic key or seed value used to generate time-based or counter-based one-time passwords for multi-factor authentication. This confidential data enables the validation of authentication codes produced by authenticator applications or hardware tokens. |
| phone | text | YES | Purpose unclear from available data. This nullable field appears to be intended for storing phone number information related to multi-factor authentication factors. |
| last_challenged_at | timestamp with time zone | YES | Records the most recent date and time when the multi-factor authentication method was used to verify a user's identity during a login or security challenge. Enables tracking of MFA usage patterns and identifying inactive authentication factors. |
| web_authn_credential | jsonb | YES | Purpose unclear from available data. Appears to store WebAuthn authentication credential information in JSON format for multi-factor authentication. |
| web_authn_aaguid | uuid | YES | Purpose unclear from available data. This appears to be related to WebAuthn authentication factors but the specific business meaning cannot be determined without sample values or additional context. |
| last_webauthn_challenge_data | jsonb | YES | Stores the most recent challenge information used in WebAuthn authentication flows, containing the cryptographic data needed to verify user identity through security keys or biometric devices. This data is temporarily held during the authentication process to validate user responses against the original challenge. |

## Primary Key

`id`

## Indexes

- `factor_id_created_at_idx`: CREATE INDEX factor_id_created_at_idx ON auth.mfa_factors USING btree (user_id, created_at)
- `mfa_factors_last_challenged_at_key`: CREATE UNIQUE INDEX mfa_factors_last_challenged_at_key ON auth.mfa_factors USING btree (last_challenged_at)
- `mfa_factors_pkey`: CREATE UNIQUE INDEX mfa_factors_pkey ON auth.mfa_factors USING btree (id)
- `mfa_factors_user_friendly_name_unique`: CREATE UNIQUE INDEX mfa_factors_user_friendly_name_unique ON auth.mfa_factors USING btree (friendly_name, user_id) WHERE (TRIM(BOTH FROM friendly_name) <> ''::text)
- `mfa_factors_user_id_idx`: CREATE INDEX mfa_factors_user_id_idx ON auth.mfa_factors USING btree (user_id)
- `unique_phone_factor_per_user`: CREATE UNIQUE INDEX unique_phone_factor_per_user ON auth.mfa_factors USING btree (user_id, phone)

*Generated at: 2025-12-11T22:50:37.850Z*