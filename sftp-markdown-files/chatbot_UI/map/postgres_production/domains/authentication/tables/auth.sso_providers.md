# sso_providers

**Database:** postgres_production
**Schema:** auth
**Description:** This table represents Single Sign-On (SSO) identity providers configured for authentication purposes, as indicated by its location in the auth schema and the database comment. The table serves as a registry for non-SAML SSO providers, complementing the separate saml_providers table mentioned in the comment for SAML-specific configurations. With no foreign key relationships and an empty dataset, this appears to be a standalone configuration table that likely stores provider-specific settings and credentials for external authentication services.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | uuid | NO | Purpose unclear from available data. Appears to be a primary key for single sign-on provider configurations. |
| resource_id | text | YES | A user-defined identifier that uniquely distinguishes each single sign-on provider within the system, designed to be case-insensitive and suitable for use in automated infrastructure management tools. |
| created_at | timestamp with time zone | YES | Records when each single sign-on provider configuration was first added to the system. Purpose unclear from available data due to lack of sample values. |
| updated_at | timestamp with time zone | YES | Records when each SSO provider configuration was last modified, enabling tracking of configuration changes and maintenance history. |
| disabled | boolean | YES | Indicates whether the single sign-on provider configuration is deactivated and unavailable for user authentication. Purpose unclear from available data due to lack of sample values. |

## Primary Key

`id`

## Indexes

- `sso_providers_pkey`: CREATE UNIQUE INDEX sso_providers_pkey ON auth.sso_providers USING btree (id)
- `sso_providers_resource_id_idx`: CREATE UNIQUE INDEX sso_providers_resource_id_idx ON auth.sso_providers USING btree (lower(resource_id))
- `sso_providers_resource_id_pattern_idx`: CREATE INDEX sso_providers_resource_id_pattern_idx ON auth.sso_providers USING btree (resource_id text_pattern_ops)

*Generated at: 2025-12-11T22:50:55.528Z*