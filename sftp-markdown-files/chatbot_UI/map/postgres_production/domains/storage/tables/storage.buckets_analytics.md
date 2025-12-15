# buckets_analytics

**Database:** postgres_production
**Schema:** storage
**Description:** Based on the limited information available, this table appears to represent analytics or metrics data related to storage buckets within a cloud storage system. The table has 7 columns with 'id' serving as the primary key, suggesting it tracks analytical measurements or usage statistics for storage containers. Without column details or sample data, the specific metrics being tracked cannot be determined, but the table likely serves a monitoring or reporting function within the storage subsystem of the application.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| name | text | NO | Purpose unclear from available data. Likely contains identifying labels or titles for storage bucket analytics records. |
| type | USER-DEFINED | NO | Categorizes analytics buckets by their designated purpose or functionality within the storage system. Defaults to 'ANALYTICS' indicating this table specifically tracks analytical data storage containers. |
| format | text | NO | Specifies the data storage format used for analytics buckets, with Iceberg as the standard format. Purpose unclear from available data due to lack of sample values to confirm other supported formats. |
| created_at | timestamp with time zone | NO | Records the exact date and time when each bucket analytics record was initially created in the system. This timestamp is automatically set when the record is first inserted and cannot be null. |
| updated_at | timestamp with time zone | NO | Records the timestamp when analytics data for a storage bucket was last modified or refreshed. Automatically updates to the current time whenever changes occur to the bucket's analytics information. |
| id | uuid | NO | Unique identifier that automatically distinguishes each analytics record for storage buckets within the system. Serves as the primary key for tracking and referencing individual bucket analytics entries. |
| deleted_at | timestamp with time zone | YES | Records the exact moment when a storage bucket's analytics data was marked for deletion, enabling soft delete functionality and audit trails. When null, indicates the analytics record is currently active and has not been deleted. |

## Primary Key

`id`

## Indexes

- `buckets_analytics_pkey`: CREATE UNIQUE INDEX buckets_analytics_pkey ON storage.buckets_analytics USING btree (id)
- `buckets_analytics_unique_name_idx`: CREATE UNIQUE INDEX buckets_analytics_unique_name_idx ON storage.buckets_analytics USING btree (name) WHERE (deleted_at IS NULL)

*Generated at: 2025-12-11T22:51:15.210Z*