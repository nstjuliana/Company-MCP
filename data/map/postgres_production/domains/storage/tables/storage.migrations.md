# migrations

**Database:** postgres_production
**Schema:** storage
**Description:** The storage.migrations table is a system metadata table that tracks database schema migration operations, storing each migration's unique identifier, descriptive name, content hash for integrity verification, and execution timestamp. Based on the sample data showing a "create-migrations-table" migration, this table serves as an audit log to ensure database schema changes are applied consistently and to prevent duplicate migration executions. The table operates independently without foreign key relationships, functioning as a standalone tracking mechanism for database version control and deployment processes.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | integer | NO | Sequential numeric identifier that tracks the order and execution status of database schema changes. Based on the consecutive values starting from 0, this appears to represent migration scripts that have been applied to update the database structure. |
| name | character varying | NO | Records the descriptive identifier for each database migration operation, indicating the specific change or feature being implemented such as table creation, schema modifications, or security policy additions. |
| hash | character varying | NO | Contains unique cryptographic fingerprints that identify specific database schema changes or migration scripts. Each value represents a distinct version or state of the database structure modifications. |
| executed_at | timestamp without time zone | YES | Records the timestamp when a database migration was successfully executed. Based on the sample values showing identical timestamps, this likely captures when a batch of migrations were run together during a deployment or database update process. |

## Indexes

- `migrations_name_key`: CREATE UNIQUE INDEX migrations_name_key ON storage.migrations USING btree (name)
- `migrations_pkey`: CREATE UNIQUE INDEX migrations_pkey ON storage.migrations USING btree (id)

## Sample Data

| id | name | hash | executed_at |
| --- | --- | --- | --- |
| 0 | create-migrations-table | e18db593bcde2aca2a408c4d1100f6abba2195df | Tue Dec 09 2025 21:29:55 GMT-0600 (Central Stan... |
| 1 | initialmigration | 6ab16121fbaa08bbd11b712d05f358f9b555d777 | Tue Dec 09 2025 21:29:55 GMT-0600 (Central Stan... |
| 2 | storage-schema | 5c7968fd083fcea04050c1b7f6253c9771b99011 | Tue Dec 09 2025 21:29:55 GMT-0600 (Central Stan... |
| 3 | pathtoken-column | 2cb1b0004b817b29d5b0a971af16bafeede4b70d | Tue Dec 09 2025 21:29:55 GMT-0600 (Central Stan... |
| 4 | add-migrations-rls | 427c5b63fe1c5937495d9c635c263ee7a5905058 | Tue Dec 09 2025 21:29:55 GMT-0600 (Central Stan... |

*Generated at: 2025-12-11T22:51:15.514Z*