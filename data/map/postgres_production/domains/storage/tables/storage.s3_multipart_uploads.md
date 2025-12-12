# s3_multipart_uploads

**Database:** postgres_production
**Schema:** storage
**Description:** This table appears to track S3 multipart upload operations within a storage system, managing the metadata and state of large file uploads that are split into multiple parts for efficient transfer. Based on its location in the storage schema and naming convention, it likely serves as a temporary tracking mechanism for in-progress multipart uploads to Amazon S3 or S3-compatible storage services. The table currently has no relationships to other tables and contains no data, suggesting it may be used for transient operational data that is cleaned up upon upload completion or failure.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | text | NO | Purpose unclear from available data. Appears to be a unique identifier for multipart upload operations in S3 storage. |
| in_progress_size | bigint | NO | Tracks the cumulative size in bytes of data that has been uploaded but not yet completed for a multipart upload operation. Represents the total amount of storage space currently occupied by incomplete upload parts. |
| upload_signature | text | NO | Purpose unclear from available data. Appears to store a signature or hash value used to validate or authenticate multipart upload operations to S3 storage. |
| bucket_id | text | NO | Purpose unclear from available data. Appears to reference a storage bucket identifier within the S3 multipart upload process. |
| key | text | NO | The unique identifier or path that specifies the location and name of the file being uploaded through the S3 multipart upload process. Purpose unclear from available data due to lack of sample values. |
| version | text | NO | Purpose unclear from available data. Without sample values or additional context, the specific meaning of this version identifier in the context of S3 multipart uploads cannot be determined. |
| owner_id | text | YES | Purpose unclear from available data, though the column name suggests it may store an identifier for the entity that owns or initiated the multipart upload operation. |
| created_at | timestamp with time zone | NO | Records the exact date and time when a multipart upload operation was initiated in the S3 storage system. This timestamp is automatically set when the upload process begins and cannot be null. |
| user_metadata | jsonb | YES | Purpose unclear from available data. Likely stores custom metadata attributes associated with multipart upload operations, but cannot determine specific content or structure without sample values. |

## Primary Key

`id`

## Indexes

- `idx_multipart_uploads_list`: CREATE INDEX idx_multipart_uploads_list ON storage.s3_multipart_uploads USING btree (bucket_id, key, created_at)
- `s3_multipart_uploads_pkey`: CREATE UNIQUE INDEX s3_multipart_uploads_pkey ON storage.s3_multipart_uploads USING btree (id)

*Generated at: 2025-12-11T22:51:27.164Z*