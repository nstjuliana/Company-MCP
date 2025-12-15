# refresh_tokens

**Database:** postgres_production
**Schema:** auth
**Description:** The `auth.refresh_tokens` table stores refresh tokens used in the JWT authentication system to obtain new access tokens when they expire. This table serves as a secure repository for managing token refresh capabilities within the authentication workflow. Based on the table name and database comment, it plays a critical role in maintaining user sessions by enabling seamless token renewal without requiring users to re-authenticate.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| instance_id | uuid | YES | Purpose unclear from available data. This appears to be an optional identifier that may link refresh tokens to a specific application or service instance. |
| id | bigint | NO | A unique identifier that automatically increments for each refresh token record in the authentication system. Serves as the primary key to distinguish individual refresh token entries. |
| token | character varying | YES | A unique string value used to securely refresh user authentication sessions without requiring re-login. Purpose unclear from available data due to lack of sample values. |
| user_id | character varying | YES | Identifies which user account owns each refresh token for authentication purposes. Links refresh tokens to specific users to enable secure session management and token validation. |
| revoked | boolean | YES | Indicates whether the refresh token has been invalidated and can no longer be used for authentication purposes. When true, the token is no longer valid for generating new access tokens. |
| created_at | timestamp with time zone | YES | Records the exact date and time when a refresh token was initially generated for user authentication purposes. Used to track token age and enable token expiration policies. |
| updated_at | timestamp with time zone | YES | Records when a refresh token record was last modified or updated in the system. Purpose unclear from available data due to lack of sample values. |
| parent | character varying | YES | Purpose unclear from available data. The column appears to be designed to store some form of identifier or reference value related to refresh token relationships, but without sample values or additional context, the specific business meaning cannot be determined. |
| session_id | uuid | YES | Links a refresh token to a specific user authentication session, allowing the system to track and manage token validity within the context of that session. Can be null when the refresh token is not associated with any particular session. |

## Primary Key

`id`

## Indexes

- `refresh_tokens_instance_id_idx`: CREATE INDEX refresh_tokens_instance_id_idx ON auth.refresh_tokens USING btree (instance_id)
- `refresh_tokens_instance_id_user_id_idx`: CREATE INDEX refresh_tokens_instance_id_user_id_idx ON auth.refresh_tokens USING btree (instance_id, user_id)
- `refresh_tokens_parent_idx`: CREATE INDEX refresh_tokens_parent_idx ON auth.refresh_tokens USING btree (parent)
- `refresh_tokens_pkey`: CREATE UNIQUE INDEX refresh_tokens_pkey ON auth.refresh_tokens USING btree (id)
- `refresh_tokens_session_id_revoked_idx`: CREATE INDEX refresh_tokens_session_id_revoked_idx ON auth.refresh_tokens USING btree (session_id, revoked)
- `refresh_tokens_token_unique`: CREATE UNIQUE INDEX refresh_tokens_token_unique ON auth.refresh_tokens USING btree (token)
- `refresh_tokens_updated_at_idx`: CREATE INDEX refresh_tokens_updated_at_idx ON auth.refresh_tokens USING btree (updated_at DESC)

*Generated at: 2025-12-11T22:50:48.278Z*