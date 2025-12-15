# vector_indexes

**Database:** postgres_production
**Schema:** storage
**Description:** This table appears to be a metadata catalog for vector indexes used in a vector database or search system, storing configuration and operational details about high-dimensional vector indexes for similarity search or machine learning operations. The table is currently empty with no established relationships to other tables, suggesting it may be part of a newly implemented or standalone vector search infrastructure. Without visible column definitions or sample data, the specific attributes and functionality of the vector indexes cannot be determined.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | text | NO | A unique identifier that serves as the primary key for each vector index record in the system. Since no sample values are available, the specific format and usage pattern cannot be determined from the available data. |
| name | text | NO | Purpose unclear from available data, though this appears to be an identifier or label for vector index configurations within the storage system. |
| bucket_id | text | NO | Purpose unclear from available data. Appears to reference a storage container or grouping mechanism within the vector indexing system. |
| data_type | text | NO | Purpose unclear from available data. Appears to specify the format or structure of data stored in vector indexes, but cannot be determined without sample values. |
| dimension | integer | NO | Purpose unclear from available data. This appears to store a numeric value related to vector index configuration, but without sample values or additional context, the specific business meaning cannot be determined. |
| distance_metric | text | NO | The method used to calculate distance or similarity between vectors in the index, such as cosine similarity, Euclidean distance, or Manhattan distance. Purpose unclear from available data due to lack of sample values. |
| metadata_configuration | jsonb | YES | Purpose unclear from available data. Likely stores configuration settings or parameters related to metadata handling for vector search indexes in JSON format. |
| created_at | timestamp with time zone | NO | Records the exact date and time when each vector index was initially created in the system. Automatically populated upon index creation and remains unchanged throughout the index's lifecycle. |
| updated_at | timestamp with time zone | NO | Records the date and time when the vector index configuration or metadata was last modified. Automatically updated to the current timestamp whenever changes are made to the index record. |

## Indexes

- `vector_indexes_name_bucket_id_idx`: CREATE UNIQUE INDEX vector_indexes_name_bucket_id_idx ON storage.vector_indexes USING btree (name, bucket_id)
- `vector_indexes_pkey`: CREATE UNIQUE INDEX vector_indexes_pkey ON storage.vector_indexes USING btree (id)

*Generated at: 2025-12-11T22:51:26.762Z*