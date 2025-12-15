# oauth_consents

**Database:** postgres_production
**Schema:** auth
**Description:** This table represents OAuth consent records within an authentication system, likely storing user permissions and authorizations granted to third-party applications or services. The table appears to be part of a broader authentication schema but currently has no established relationships with other tables in the database. Given its location in the auth schema and naming convention, it likely serves as a tracking mechanism for OAuth flow consent decisions, though the specific consent attributes cannot be determined without column information.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | uuid | NO | Unique identifier for each OAuth consent record that tracks user authorization decisions for third-party applications. Purpose unclear from available data due to lack of sample values. |
| user_id | uuid | NO | References the unique identifier of the user who has granted or denied consent for OAuth authorization. Links each consent record to a specific user account in the authentication system. |
| client_id | uuid | NO | Purpose unclear from available data. Appears to reference an external entity within an OAuth consent management system. |
| scopes | text | NO | Purpose unclear from available data. Likely contains authorization permissions or access levels granted through OAuth authentication flows, but cannot be confirmed without sample values. |
| granted_at | timestamp with time zone | NO | Records the exact moment when a user provided consent for an OAuth application to access their account or data. This timestamp establishes when the authorization was officially granted in the system. |
| revoked_at | timestamp with time zone | YES | Records the date and time when a user's OAuth consent was revoked or withdrawn. When null, indicates the consent is still active and has not been revoked. |

## Primary Key

`id`

## Indexes

- `oauth_consents_active_client_idx`: CREATE INDEX oauth_consents_active_client_idx ON auth.oauth_consents USING btree (client_id) WHERE (revoked_at IS NULL)
- `oauth_consents_active_user_client_idx`: CREATE INDEX oauth_consents_active_user_client_idx ON auth.oauth_consents USING btree (user_id, client_id) WHERE (revoked_at IS NULL)
- `oauth_consents_pkey`: CREATE UNIQUE INDEX oauth_consents_pkey ON auth.oauth_consents USING btree (id)
- `oauth_consents_user_client_unique`: CREATE UNIQUE INDEX oauth_consents_user_client_unique ON auth.oauth_consents USING btree (user_id, client_id)
- `oauth_consents_user_order_idx`: CREATE INDEX oauth_consents_user_order_idx ON auth.oauth_consents USING btree (user_id, granted_at DESC)

*Generated at: 2025-12-11T22:50:34.940Z*