# sessions

**Database:** postgres_production
**Schema:** auth
**Description:** This table represents user authentication sessions in the system, storing session data associated with authenticated users as indicated by the database comment. The table serves as a core component of the authentication system, maintaining session state and user login information. Based on the auth schema namespace and the table name, it plays a central role in managing user session lifecycle and authentication state persistence.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | uuid | NO | Serves as the primary unique identifier for each user authentication session within the system. Enables tracking and management of individual login instances across the application. |
| user_id | uuid | NO | References the unique identifier of the authenticated user who owns this session. Links each session record to a specific user account in the system. |
| created_at | timestamp with time zone | YES | Records the date and time when a user authentication session was initially established in the system. |
| updated_at | timestamp with time zone | YES | Records when each user session was last modified or accessed. Purpose unclear from available data without sample values to confirm specific update triggers. |
| factor_id | uuid | YES | Purpose unclear from available data. Appears to reference an authentication factor or method associated with the session, but without sample values or additional context, the specific business meaning cannot be determined. |
| aal | USER-DEFINED | YES | Purpose unclear from available data. The column appears to be related to authentication sessions but without sample values or additional context, the specific meaning cannot be determined. |
| not_after | timestamp with time zone | YES | Specifies the expiration timestamp after which the user session becomes invalid and should no longer be accepted for authentication. When null, the session may not have a defined expiration time or uses alternative expiration mechanisms. |
| refreshed_at | timestamp without time zone | YES | Records the timestamp when a user session's authentication token was last refreshed or renewed. Purpose unclear from available data due to lack of sample values. |
| user_agent | text | YES | Stores the browser and device information string that identifies the client application used to establish the authentication session. This information is typically used for security monitoring and session management purposes. |
| ip | inet | YES | Stores the network address from which a user established their authentication session. Used for security tracking and access monitoring purposes. |
| tag | text | YES | Purpose unclear from available data. Without sample values, this appears to be an optional text field that may be used for labeling or categorizing user authentication sessions. |
| oauth_client_id | uuid | YES | Identifies the OAuth client application that was used to authenticate and establish this user session. Links the session to a specific third-party application or service that initiated the OAuth flow. |
| refresh_token_hmac_key | text | YES | Stores the cryptographic key used to digitally sign refresh tokens associated with a user's authentication session, enabling verification of token authenticity and integrity. This key ensures that refresh tokens cannot be forged or tampered with during the token refresh process. |
| refresh_token_counter | bigint | YES | Tracks the sequential identifier of the most recently generated refresh token for a user's authentication session. Used to invalidate previous refresh tokens and ensure only the latest token remains valid for session renewal. |
| scopes | text | YES | Purpose unclear from available data. Likely stores permission or access level definitions for user authentication sessions, but cannot be confirmed without sample values. |

## Primary Key

`id`

## Indexes

- `sessions_not_after_idx`: CREATE INDEX sessions_not_after_idx ON auth.sessions USING btree (not_after DESC)
- `sessions_oauth_client_id_idx`: CREATE INDEX sessions_oauth_client_id_idx ON auth.sessions USING btree (oauth_client_id)
- `sessions_pkey`: CREATE UNIQUE INDEX sessions_pkey ON auth.sessions USING btree (id)
- `sessions_user_id_idx`: CREATE INDEX sessions_user_id_idx ON auth.sessions USING btree (user_id)
- `user_id_created_at_idx`: CREATE INDEX user_id_created_at_idx ON auth.sessions USING btree (user_id, created_at)

*Generated at: 2025-12-11T22:50:56.883Z*