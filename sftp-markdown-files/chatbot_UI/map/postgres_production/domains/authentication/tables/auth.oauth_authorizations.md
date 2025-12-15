# oauth_authorizations

**Database:** postgres_production
**Schema:** auth
**Description:** Based on the table name `auth.oauth_authorizations`, this table appears to store OAuth authorization records within an authentication system, likely tracking authorization grants or tokens issued during OAuth flows. However, without visible column information or sample data, I cannot determine the specific structure, relationships, or detailed functionality of this authorization entity. The table currently contains no data and has no established foreign key relationships with other tables in the database.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | uuid | NO | Unique identifier for each OAuth authorization record that tracks when users grant permission to third-party applications to access their account. Serves as the primary key for linking authorization events to specific users and applications. |
| authorization_id | text | NO | Purpose unclear from available data. Without sample values or additional context, the specific business meaning of this identifier within the OAuth authorization process cannot be determined. |
| client_id | uuid | NO | Purpose unclear from available data. This appears to reference an external application or service in an OAuth authorization context, but without sample values or additional schema information, the specific business meaning cannot be determined. |
| user_id | uuid | YES | References the unique identifier of the user who granted authorization in the OAuth flow. Can be null when authorization exists without an associated user account. |
| redirect_uri | text | NO | Purpose unclear from available data. Based on the table context, this likely stores the URL where users should be redirected after OAuth authorization completes. |
| scope | text | NO | Purpose unclear from available data. Likely defines the permissions or access levels granted through an OAuth authorization, but cannot be confirmed without sample values. |
| state | text | YES | Purpose unclear from available data. This appears to be an optional text field within the OAuth authorization process, but without sample values or additional context, the specific business meaning cannot be determined. |
| resource | text | YES | Purpose unclear from available data. This appears to store textual identifiers or references related to OAuth authorization processes, but the specific business meaning cannot be determined without sample values. |
| code_challenge | text | YES | A cryptographically secure random string used in the PKCE (Proof Key for Code Exchange) OAuth 2.0 flow to prevent authorization code interception attacks. Purpose unclear from available data due to lack of sample values. |
| code_challenge_method | USER-DEFINED | YES | Purpose unclear from available data. Likely relates to OAuth authorization flow security mechanisms, but cannot determine specific meaning without sample values or additional context. |
| response_type | USER-DEFINED | NO | Specifies the type of response requested in an OAuth authorization flow, with "code" being the default indicating an authorization code grant type. This determines how the OAuth provider should respond after user authorization. |
| status | USER-DEFINED | NO | Tracks the current state of an OAuth authorization request, with requests initially set to pending status. Indicates whether the authorization process is awaiting approval, has been granted, denied, or is in another defined state. |
| authorization_code | text | YES | A temporary code generated during the OAuth authorization flow that can be exchanged for an access token. Purpose unclear from available data due to lack of sample values. |
| created_at | timestamp with time zone | NO | Records the exact moment when an OAuth authorization was first established in the system. This timestamp serves as an audit trail for tracking when users granted permission to third-party applications. |
| expires_at | timestamp with time zone | NO | Records when an OAuth authorization token or code will become invalid and can no longer be used for authentication. Set to expire 3 minutes after creation by default to ensure short-lived authorization windows for security purposes. |
| approved_at | timestamp with time zone | YES | Records the exact date and time when an OAuth authorization request was approved by the user. Remains null for pending or denied authorization requests. |
| nonce | text | YES | A unique random value used to prevent replay attacks and ensure the security of OAuth authorization requests. This cryptographic token helps verify that authorization responses correspond to requests initiated by the same client. |

## Primary Key

`id`

## Indexes

- `oauth_auth_pending_exp_idx`: CREATE INDEX oauth_auth_pending_exp_idx ON auth.oauth_authorizations USING btree (expires_at) WHERE (status = 'pending'::auth.oauth_authorization_status)
- `oauth_authorizations_authorization_code_key`: CREATE UNIQUE INDEX oauth_authorizations_authorization_code_key ON auth.oauth_authorizations USING btree (authorization_code)
- `oauth_authorizations_authorization_id_key`: CREATE UNIQUE INDEX oauth_authorizations_authorization_id_key ON auth.oauth_authorizations USING btree (authorization_id)
- `oauth_authorizations_pkey`: CREATE UNIQUE INDEX oauth_authorizations_pkey ON auth.oauth_authorizations USING btree (id)

*Generated at: 2025-12-11T22:50:39.315Z*