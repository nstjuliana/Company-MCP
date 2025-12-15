# flow_state

**Database:** postgres_production
**Schema:** auth
**Description:** This table stores metadata and state information for PKCE (Proof Key for Code Exchange) authentication flows, which are used to securely handle OAuth authorization processes. The table serves as a temporary data store to track the progress and parameters of ongoing authentication sessions. Based on the database comment and table name, it likely manages the state transitions and security tokens during user login processes, though specific implementation details cannot be determined without column information.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | uuid | NO | Purpose unclear from available data as no sample values or database comments are provided to indicate the specific business meaning of this identifier within the authentication flow state context. |
| user_id | uuid | YES | Purpose unclear from available data. Likely references a user account associated with an authentication flow state, but cannot be confirmed without sample values or additional context. |
| auth_code | text | NO | Purpose unclear from available data. Without sample values or database comments, the specific role of this required text field in the authentication flow cannot be determined. |
| code_challenge_method | USER-DEFINED | NO | Purpose unclear from available data. This appears to be related to authentication flow processing but the specific business meaning cannot be determined without sample values or additional context. |
| code_challenge | text | NO | A cryptographically secure random string used in the OAuth 2.0 PKCE (Proof Key for Code Exchange) flow to verify that the authorization request and token exchange are made by the same client. This value is hashed and compared against the code_verifier to prevent authorization code interception attacks. |
| provider_type | text | NO | Purpose unclear from available data. Likely identifies the type of authentication or identity provider used in an authentication flow process. |
| provider_access_token | text | YES | Purpose unclear from available data. Likely stores access credentials for external authentication providers, but cannot be confirmed without sample values. |
| provider_refresh_token | text | YES | Stores the refresh token obtained from an external authentication provider during OAuth flows, used to obtain new access tokens when the original ones expire. Purpose is to maintain long-term authentication sessions without requiring users to re-authenticate. |
| created_at | timestamp with time zone | YES | Records when an authentication flow state record was initially created in the system. Purpose unclear from available data due to lack of sample values. |
| updated_at | timestamp with time zone | YES | Records the most recent modification time for authentication flow state records, enabling tracking of when user authentication sessions or workflows were last changed. |
| authentication_method | text | NO | Purpose unclear from available data. The column appears to store the specific method or mechanism used during an authentication flow process, but without sample values, the exact authentication methods supported cannot be determined. |
| auth_code_issued_at | timestamp with time zone | YES | Records the exact moment when an authorization code was generated during the OAuth authentication flow. Used to track timing and potentially enforce expiration policies for issued codes. |

## Primary Key

`id`

## Indexes

- `flow_state_created_at_idx`: CREATE INDEX flow_state_created_at_idx ON auth.flow_state USING btree (created_at DESC)
- `flow_state_pkey`: CREATE UNIQUE INDEX flow_state_pkey ON auth.flow_state USING btree (id)
- `idx_auth_code`: CREATE INDEX idx_auth_code ON auth.flow_state USING btree (auth_code)
- `idx_user_id_auth_method`: CREATE INDEX idx_user_id_auth_method ON auth.flow_state USING btree (user_id, authentication_method)

*Generated at: 2025-12-11T22:50:26.780Z*