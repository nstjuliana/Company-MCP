# schema_migrations

**Database:** postgres_production
**Schema:** realtime
**Description:** This table represents a database schema migration tracking system for the realtime module, storing version identifiers and timestamps of when each migration was applied. Each row tracks a specific migration event with a version number (formatted as a timestamp-based identifier like "20211116024918") and the exact datetime when it was inserted into the system. The table serves as an internal system component to maintain the database schema evolution history and ensure migrations are applied in the correct order without duplication.

**Row Count:** 65

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| version | bigint | NO | Records the timestamp identifier for each database schema migration that has been applied, formatted as YYYYMMDDHHMMSS. Tracks the chronological order and timing of structural changes made to the realtime database schema. |
| inserted_at | timestamp without time zone | YES | Records the timestamp when each database schema migration was applied to the realtime system. All sample values show migrations executed within seconds of each other on the same date, indicating a batch migration deployment. |

## Primary Key

`version`

## Indexes

- `schema_migrations_pkey`: CREATE UNIQUE INDEX schema_migrations_pkey ON realtime.schema_migrations USING btree (version)

## Sample Data

| version | inserted_at |
| --- | --- |
| 20211116024918 | Tue Dec 09 2025 21:30:00 GMT-0600 (Central Stan... |
| 20211116045059 | Tue Dec 09 2025 21:30:01 GMT-0600 (Central Stan... |
| 20211116050929 | Tue Dec 09 2025 21:30:02 GMT-0600 (Central Stan... |
| 20211116051442 | Tue Dec 09 2025 21:30:02 GMT-0600 (Central Stan... |
| 20211116212300 | Tue Dec 09 2025 21:30:03 GMT-0600 (Central Stan... |

*Generated at: 2025-12-11T22:51:46.506Z*