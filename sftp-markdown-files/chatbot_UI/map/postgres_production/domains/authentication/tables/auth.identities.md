# identities

**Database:** postgres_production
**Schema:** auth
**Description:** This table stores identity records associated with user authentication, serving as a repository for different authentication methods or identity providers linked to users. Based on the database comment indicating it stores "identities associated to a user," this table likely supports multiple authentication mechanisms (such as email/password, OAuth providers, or social logins) for a single user account. The table appears to be part of an authentication system's data model, though specific relationships and implementation details cannot be determined from the available information.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| provider_id | text | NO | Purpose unclear from available data. This appears to store an external identifier associated with authentication providers, but without sample values the specific format or meaning cannot be determined. |
| user_id | uuid | NO | Purpose unclear from available data. Based on the table context in an authentication system, this likely references a user account that the identity record belongs to. |
| identity_data | jsonb | NO | Purpose unclear from available data. Appears to store structured information related to user authentication identities in a flexible format. |
| provider | text | NO | Purpose unclear from available data. This appears to store text values related to authentication identity sources, but without sample values the specific meaning cannot be determined. |
| last_sign_in_at | timestamp with time zone | YES | Records the most recent date and time when the user successfully authenticated and signed into the system. Used for tracking user activity patterns and implementing security policies based on login recency. |
| created_at | timestamp with time zone | YES | Records the timestamp when an identity record was first established in the authentication system. Purpose unclear from available data due to lack of sample values. |
| updated_at | timestamp with time zone | YES | Records when an identity record was last modified, tracking the most recent update to authentication-related information for audit and data management purposes. |
| email | text | YES | A generated field that extracts and stores the optional email address from the identity data associated with an authentication record. References email information provided during user identity creation or updates. |
| id | uuid | NO | Unique identifier for each identity record within the authentication system. Automatically generated to distinguish between different user authentication methods or providers. |

## Primary Key

`id`

## Indexes

- `identities_email_idx`: CREATE INDEX identities_email_idx ON auth.identities USING btree (email text_pattern_ops)
- `identities_pkey`: CREATE UNIQUE INDEX identities_pkey ON auth.identities USING btree (id)
- `identities_provider_id_provider_unique`: CREATE UNIQUE INDEX identities_provider_id_provider_unique ON auth.identities USING btree (provider_id, provider)
- `identities_user_id_idx`: CREATE INDEX identities_user_id_idx ON auth.identities USING btree (user_id)

*Generated at: 2025-12-11T22:50:26.466Z*