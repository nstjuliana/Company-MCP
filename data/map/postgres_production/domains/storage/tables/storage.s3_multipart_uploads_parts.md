# s3_multipart_uploads_parts

**Database:** postgres_production
**Schema:** storage
**Description:** I cannot provide a semantic description for this table as the column information is missing or not properly displayed, and there is no sample data available. Without knowing the actual column names and their data types, it would be speculative to describe the business entity or purpose of this table beyond what can be inferred from its name suggesting it relates to S3 multipart upload operations.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | uuid | NO | A unique identifier automatically assigned to each part of a multipart file upload in the S3-compatible storage system. This serves as the primary key to distinguish individual chunks or segments that make up a larger file being uploaded in pieces. |
| upload_id | text | NO | Unique identifier that associates individual parts with their parent multipart upload operation in S3 storage. Links uploaded file chunks to enable proper reassembly into the complete file. |
| size | bigint | NO | The byte size of an individual part within a multipart upload to S3 storage. Defaults to zero when no data has been uploaded for the part. |
| part_number | integer | NO | The sequential identifier for individual parts within a multipart upload operation, used to maintain the correct order when reassembling the complete file. This value determines the position of each chunk in the final assembled object. |
| bucket_id | text | NO | Identifies the specific S3 storage bucket that contains the multipart upload parts. This serves as a reference to link upload parts with their designated storage container. |
| key | text | NO | Purpose unclear from available data. Without sample values, the specific meaning of this required text field in the S3 multipart uploads parts table cannot be determined. |
| etag | text | NO | A unique identifier returned by AWS S3 for each part of a multipart upload, used to verify the integrity and successful upload of that specific part. |
| owner_id | text | YES | Purpose unclear from available data, though likely stores an identifier linking multipart upload parts to the entity or user who initiated the upload process. |
| version | text | NO | Purpose unclear from available data. Likely stores a version identifier or revision number for multipart upload parts, but cannot be determined definitively without sample values. |
| created_at | timestamp with time zone | NO | Records the exact moment when each part of a multipart S3 upload was initiated or registered in the system. Automatically captures the timestamp when new upload parts are created to track upload progression and timing. |

## Primary Key

`id`

## Indexes

- `s3_multipart_uploads_parts_pkey`: CREATE UNIQUE INDEX s3_multipart_uploads_parts_pkey ON storage.s3_multipart_uploads_parts USING btree (id)

*Generated at: 2025-12-11T22:51:26.129Z*