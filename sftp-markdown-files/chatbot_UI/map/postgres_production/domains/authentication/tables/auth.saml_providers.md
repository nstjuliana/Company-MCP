# saml_providers

**Database:** postgres_production
**Schema:** auth
**Description:** This table represents SAML (Security Assertion Markup Language) identity providers configured for authentication in the system. Based on the database comment, it manages connections to external SAML Identity Providers that enable single sign-on functionality for user authentication. The table currently has no foreign key relationships and serves as a standalone configuration store for SAML provider settings within the auth schema.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | uuid | NO | A unique identifier that distinguishes each SAML (Security Assertion Markup Language) identity provider configuration within the authentication system. This enables the system to manage multiple SAML providers for single sign-on integration. |
| sso_provider_id | uuid | NO | Purpose unclear from available data. Appears to reference an external single sign-on provider entity within the SAML authentication configuration. |
| entity_id | text | NO | Purpose unclear from available data. This appears to be a required text identifier within the SAML authentication provider configuration, but without sample values, the specific business meaning cannot be determined. |
| metadata_xml | text | NO | Contains the SAML identity provider's metadata configuration in XML format, which defines authentication endpoints, certificates, and other provider-specific settings required for SAML single sign-on integration. |
| metadata_url | text | YES | Stores the URL endpoint where SAML identity provider metadata can be retrieved, containing configuration details needed for authentication integration. Purpose unclear from available data due to lack of sample values. |
| attribute_mapping | jsonb | YES | Purpose unclear from available data. Likely stores configuration that maps SAML assertion attributes to internal user profile fields, but cannot be confirmed without sample values. |
| created_at | timestamp with time zone | YES | Records when each SAML identity provider configuration was first added to the system for audit and tracking purposes. |
| updated_at | timestamp with time zone | YES | Records when a SAML authentication provider configuration was last modified or updated. Purpose unclear from available data due to lack of sample values. |
| name_id_format | text | YES | Purpose unclear from available data. Likely stores a format specification for SAML name identifiers, but cannot determine specific usage without sample values. |

## Primary Key

`id`

## Indexes

- `saml_providers_entity_id_key`: CREATE UNIQUE INDEX saml_providers_entity_id_key ON auth.saml_providers USING btree (entity_id)
- `saml_providers_pkey`: CREATE UNIQUE INDEX saml_providers_pkey ON auth.saml_providers USING btree (id)
- `saml_providers_sso_provider_id_idx`: CREATE INDEX saml_providers_sso_provider_id_idx ON auth.saml_providers USING btree (sso_provider_id)

*Generated at: 2025-12-11T22:50:47.979Z*