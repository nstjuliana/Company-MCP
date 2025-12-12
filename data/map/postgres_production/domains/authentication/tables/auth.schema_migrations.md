# schema_migrations

**Database:** postgres_production
**Schema:** auth
**Description:** The auth.schema_migrations table is a system table that tracks database schema version changes for the authentication system, storing migration version timestamps as strings. Based on the sample data showing version "20171026211738" (representing a timestamp format), this table maintains a historical record of which database migrations have been applied to keep the auth schema up to date. This table operates independently without foreign key relationships and serves as an internal tracking mechanism for database migration management within the authentication module.

**Row Count:** 71

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| version | character varying | NO | Stores migration identifiers that track database schema changes over time, with most values following a timestamp format indicating when each migration was created. |

## Indexes

- `schema_migrations_pkey`: CREATE UNIQUE INDEX schema_migrations_pkey ON auth.schema_migrations USING btree (version)

## Sample Data

| version |
| --- |
| 20171026211738 |
| 20171026211808 |
| 20171026211834 |
| 20180103212743 |
| 20180108183307 |

*Generated at: 2025-12-11T22:50:47.284Z*