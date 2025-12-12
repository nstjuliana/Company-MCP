# saml_relay_states

**Database:** postgres_production
**Schema:** auth
**Description:** This table stores SAML relay state information used during Service Provider initiated authentication flows in a SAML-based single sign-on system. The table appears to temporarily track state data needed to complete SAML authentication requests, with each record identified by a primary key. As an isolated authentication utility table with no foreign key relationships, it serves as a temporary data store for managing SAML protocol state during user login processes.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | uuid | NO | A unique identifier for each SAML relay state record used to maintain session context during SAML authentication flows. Purpose unclear from available data due to lack of sample values. |
| sso_provider_id | uuid | NO | Identifies the specific single sign-on provider configuration used during a SAML authentication flow. Links the relay state to the particular SSO provider that initiated or will handle the authentication request. |
| request_id | text | NO | Purpose unclear from available data. The column appears to store text identifiers related to SAML authentication relay state management, but without sample values, the specific nature of these identifiers cannot be determined. |
| for_email | text | YES | Purpose unclear from available data. Based on the table context and column name, this may store an email address associated with a SAML authentication relay state. |
| redirect_to | text | YES | Purpose unclear from available data. Likely stores a URL or path where users should be redirected after SAML authentication processing completes. |
| created_at | timestamp with time zone | YES | Purpose unclear from available data. Likely tracks when SAML relay state records were initially created in the system. |
| updated_at | timestamp with time zone | YES | Records when each SAML relay state entry was last modified, enabling tracking of changes to authentication session data over time. |
| flow_state_id | uuid | YES | Links a SAML relay state to a specific authentication flow session, enabling the system to track and resume user authentication processes across SAML identity provider interactions. |

## Primary Key

`id`

## Indexes

- `saml_relay_states_created_at_idx`: CREATE INDEX saml_relay_states_created_at_idx ON auth.saml_relay_states USING btree (created_at DESC)
- `saml_relay_states_for_email_idx`: CREATE INDEX saml_relay_states_for_email_idx ON auth.saml_relay_states USING btree (for_email)
- `saml_relay_states_pkey`: CREATE UNIQUE INDEX saml_relay_states_pkey ON auth.saml_relay_states USING btree (id)
- `saml_relay_states_sso_provider_id_idx`: CREATE INDEX saml_relay_states_sso_provider_id_idx ON auth.saml_relay_states USING btree (sso_provider_id)

*Generated at: 2025-12-11T22:50:46.901Z*