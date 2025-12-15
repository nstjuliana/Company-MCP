# instances

**Database:** postgres_production
**Schema:** auth
**Description:** The `auth.instances` table appears to represent individual authentication instances or tenant environments within a multi-site authentication system, as indicated by the database comment "Auth: Manages users across multiple sites." This table serves as a foundational entity in the authentication schema, likely storing configuration or metadata for different site instances where users can be managed. With no foreign key relationships currently established and no sample data available, the specific role and data structure cannot be determined beyond its apparent function as an instance registry within the multi-tenant authentication framework.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | uuid | NO | Uniquely identifies each authentication instance within the system. Purpose unclear from available data beyond serving as the primary identifier for instance records. |
| uuid | uuid | YES | Purpose unclear from available data. This appears to be an optional identifier field within an authentication instances table, but without sample values or additional context, the specific business meaning cannot be determined. |
| raw_base_config | text | YES | Purpose unclear from available data. Appears to store configuration information in its original, unprocessed format for authentication instances. |
| created_at | timestamp with time zone | YES | Records the date and time when an authentication instance was first created in the system. Purpose unclear from available data due to lack of sample values. |
| updated_at | timestamp with time zone | YES | Records when an authentication instance was last modified. Purpose unclear from available data due to lack of sample values. |

## Primary Key

`id`

## Indexes

- `instances_pkey`: CREATE UNIQUE INDEX instances_pkey ON auth.instances USING btree (id)

*Generated at: 2025-12-11T22:50:24.782Z*