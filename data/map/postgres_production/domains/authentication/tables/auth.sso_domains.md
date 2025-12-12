# sso_domains

**Database:** postgres_production
**Schema:** auth
**Description:** The auth.sso_domains table represents email domain configurations for Single Sign-On (SSO) authentication, mapping specific email domains to their corresponding SSO Identity Providers. This table serves as a lookup mechanism to determine which SSO provider should handle authentication requests based on a user's email domain. The table appears to be a standalone configuration entity with no direct foreign key relationships, functioning as a reference table within the authentication system.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | uuid | NO | A unique identifier that distinguishes each single sign-on domain configuration within the authentication system. Purpose unclear from available data due to lack of sample values. |
| sso_provider_id | uuid | NO | Links each SSO domain configuration to its corresponding single sign-on provider service. This establishes which authentication provider handles login requests for domains in this table. |
| domain | text | NO | Purpose unclear from available data, though this appears to store domain-related information for single sign-on authentication configuration. |
| created_at | timestamp with time zone | YES | Records the timestamp when a single sign-on domain configuration was first added to the system. Purpose unclear from available data due to lack of sample values. |
| updated_at | timestamp with time zone | YES | Records when an SSO domain configuration was last modified. Purpose unclear from available data due to lack of sample values. |

## Primary Key

`id`

## Indexes

- `sso_domains_domain_idx`: CREATE UNIQUE INDEX sso_domains_domain_idx ON auth.sso_domains USING btree (lower(domain))
- `sso_domains_pkey`: CREATE UNIQUE INDEX sso_domains_pkey ON auth.sso_domains USING btree (id)
- `sso_domains_sso_provider_id_idx`: CREATE INDEX sso_domains_sso_provider_id_idx ON auth.sso_domains USING btree (sso_provider_id)

*Generated at: 2025-12-11T22:50:55.068Z*