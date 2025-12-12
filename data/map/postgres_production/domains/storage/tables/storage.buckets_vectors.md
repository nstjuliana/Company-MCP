# buckets_vectors

**Database:** postgres_production
**Schema:** storage
**Description:** Based on the limited information provided, this table appears to be related to vector storage functionality within a storage system, likely for storing embeddings or vector representations associated with storage buckets. However, without column definitions or sample data, the specific business entity and relationships cannot be determined. The table currently contains no data and lacks defined relationships to other tables in the system.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | text | NO | Purpose unclear from available data. Appears to be a unique identifier for records in the buckets vectors table. |
| type | USER-DEFINED | NO | Specifies the category or classification of storage bucket within the vector storage system. Uses an enumerated value with "VECTOR" as the standard designation for buckets containing vector data. |
| created_at | timestamp with time zone | NO | Records the exact moment when a vector storage bucket was first created in the system. This timestamp cannot be null and automatically captures the current time when a new bucket is established. |
| updated_at | timestamp with time zone | NO | Records the timestamp when the bucket vector record was last modified, automatically set to the current time whenever changes occur. |

## Indexes

- `buckets_vectors_pkey`: CREATE UNIQUE INDEX buckets_vectors_pkey ON storage.buckets_vectors USING btree (id)

*Generated at: 2025-12-11T22:51:13.470Z*