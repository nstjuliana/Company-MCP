# objects

**Database:** postgres_production
**Schema:** storage
**Description:** Based on the available information, this appears to be an objects table within a storage schema that likely represents file or blob storage entities in a PostgreSQL production database. The table has 13 columns with an 'id' primary key, suggesting it tracks stored objects with various metadata attributes. However, without visible column details or sample data, the specific purpose and data model role cannot be determined beyond its apparent function as a storage object registry.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | uuid | NO | A unique identifier automatically assigned to each stored object in the system. Serves as the primary reference for tracking and managing individual files or data objects within the storage system. |
| bucket_id | text | YES | Purpose unclear from available data. Likely references a storage container or organizational unit within the storage system, but cannot be confirmed without sample values. |
| name | text | YES | Purpose unclear from available data. Likely contains identifiers or labels for stored objects, but cannot be determined without sample values. |
| owner | uuid | YES | A deprecated identifier that previously tracked the entity responsible for or associated with a stored object. This field has been superseded by owner_id and should no longer be used. |
| created_at | timestamp with time zone | YES | Records the exact moment when a storage object was first added to the system. Automatically populated with the current timestamp when a new object record is created. |
| updated_at | timestamp with time zone | YES | Records the timestamp when the stored object was last modified or updated. Automatically captures the current date and time whenever changes are made to the object's metadata or content. |
| last_accessed_at | timestamp with time zone | YES | Records the most recent date and time when the stored object was accessed or retrieved. Automatically updates to the current timestamp when not explicitly set. |
| metadata | jsonb | YES | Purpose unclear from available data. Likely stores additional file or object properties and attributes in a flexible key-value structure. |
| path_tokens | ARRAY | YES | Purpose unclear from available data. Appears to store segmented components of a file or object path structure. |
| version | text | YES | Purpose unclear from available data. Could represent a version identifier or revision number for stored objects, but cannot be determined without sample values. |
| owner_id | text | YES | Purpose unclear from available data. Likely stores an identifier linking each storage object to its associated owner or user account. |
| user_metadata | jsonb | YES | Purpose unclear from available data. Appears to store flexible metadata attributes defined by users for stored objects. |
| level | integer | YES | Purpose unclear from available data. The integer values may represent a hierarchical depth, priority ranking, or classification tier within the storage object system. |

## Primary Key

`id`

## Indexes

- `bucketid_objname`: CREATE UNIQUE INDEX bucketid_objname ON storage.objects USING btree (bucket_id, name)
- `idx_name_bucket_level_unique`: CREATE UNIQUE INDEX idx_name_bucket_level_unique ON storage.objects USING btree (name COLLATE "C", bucket_id, level)
- `idx_objects_bucket_id_name`: CREATE INDEX idx_objects_bucket_id_name ON storage.objects USING btree (bucket_id, name COLLATE "C")
- `idx_objects_lower_name`: CREATE INDEX idx_objects_lower_name ON storage.objects USING btree ((path_tokens[level]), lower(name) text_pattern_ops, bucket_id, level)
- `name_prefix_search`: CREATE INDEX name_prefix_search ON storage.objects USING btree (name text_pattern_ops)
- `objects_bucket_id_level_idx`: CREATE UNIQUE INDEX objects_bucket_id_level_idx ON storage.objects USING btree (bucket_id, level, name COLLATE "C")
- `objects_pkey`: CREATE UNIQUE INDEX objects_pkey ON storage.objects USING btree (id)

*Generated at: 2025-12-11T22:51:16.852Z*