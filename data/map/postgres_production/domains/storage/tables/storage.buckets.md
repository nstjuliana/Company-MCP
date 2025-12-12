# buckets

**Database:** postgres_production
**Schema:** storage
**Description:** This table appears to represent storage buckets in a file or object storage system, likely serving as a configuration or metadata registry for organizing stored files. Based on the table name "storage.buckets" and its placement in a dedicated storage schema, it functions as a foundational component for a file storage service within the application. Without column details or sample data available, the specific attributes and relationships of these storage buckets cannot be determined.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | text | NO | Purpose unclear from available data. Serves as the primary identifier for storage bucket records. |
| name | text | NO | Purpose unclear from available data. This appears to be a required identifier field within a storage bucket management system. |
| owner | uuid | YES | Identifies the user or entity that owns this storage bucket, though this field has been superseded by a newer owner_id column. Purpose unclear from available data due to deprecation status and lack of sample values. |
| created_at | timestamp with time zone | YES | Records the exact date and time when each storage bucket was initially created in the system, automatically set to the current timestamp upon bucket creation. |
| updated_at | timestamp with time zone | YES | Records when each storage bucket configuration was last modified, automatically updating to the current timestamp whenever bucket properties or settings are changed. |
| public | boolean | YES | Indicates whether the storage bucket allows unrestricted public access to its contents. When set to true, files in the bucket can be accessed without authentication. |
| avif_autodetection | boolean | YES | Indicates whether automatic detection of AVIF image format is enabled for the storage bucket. Controls if the system should automatically identify and process AVIF files when they are uploaded to this bucket. |
| file_size_limit | bigint | YES | Defines the maximum allowed size in bytes for files that can be stored in this bucket. When set to null, no size restrictions are applied to uploaded files. |
| allowed_mime_types | ARRAY | YES | Purpose unclear from available data. This appears to store restrictions on file types that can be uploaded to a storage bucket, but without sample values the specific implementation cannot be determined. |
| owner_id | text | YES | Purpose unclear from available data. Likely references the identifier of the entity that owns or has control over the storage bucket. |
| type | USER-DEFINED | NO | Specifies the classification or tier of the storage bucket, with a standard configuration as the default option. This likely determines storage characteristics such as performance level, redundancy, or access patterns. |

## Primary Key

`id`

## Indexes

- `bname`: CREATE UNIQUE INDEX bname ON storage.buckets USING btree (name)
- `buckets_pkey`: CREATE UNIQUE INDEX buckets_pkey ON storage.buckets USING btree (id)

*Generated at: 2025-12-11T22:51:17.241Z*