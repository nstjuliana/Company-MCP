# prefixes

**Database:** postgres_production
**Schema:** storage
**Description:** This table appears to represent storage bucket prefixes or directory-like structures within a storage system, organized by bucket identifier, hierarchical level, and name. The composite primary key of (bucket_id, level, name) suggests it maintains a hierarchical organization of storage prefixes within buckets, where each prefix can exist at different levels of a directory tree structure. The table currently contains no data and has no foreign key relationships, indicating it may be part of a standalone storage management system or awaiting population with prefix metadata.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| bucket_id | text | NO | Purpose unclear from available data. Appears to reference an identifier for storage containers, but without sample values the specific meaning cannot be determined. |
| name | text | NO | Purpose unclear from available data. This appears to be an identifier or label field within a storage prefix configuration system, but without sample values or additional context, the specific business meaning cannot be determined. |
| level | integer | NO | Purpose unclear from available data. The integer values likely represent some form of hierarchical depth or priority ranking within the prefix storage system. |
| created_at | timestamp with time zone | YES | Records the moment when a storage prefix configuration was first established in the system. Automatically captures the current timestamp when each prefix entry is initially created. |
| updated_at | timestamp with time zone | YES | Records the date and time when a storage prefix record was last modified, automatically updating to the current timestamp whenever changes are made to the row. |

## Primary Key

`bucket_id, level, name`

## Indexes

- `idx_prefixes_lower_name`: CREATE INDEX idx_prefixes_lower_name ON storage.prefixes USING btree (bucket_id, level, ((string_to_array(name, '/'::text))[level]), lower(name) text_pattern_ops)
- `prefixes_pkey`: CREATE UNIQUE INDEX prefixes_pkey ON storage.prefixes USING btree (bucket_id, level, name)

*Generated at: 2025-12-11T22:51:24.738Z*