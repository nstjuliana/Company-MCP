# app_server_map

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.app_server_map` table likely represents the association between applications and servers, detailing which application is hosted on which server within certain environments. Through the primary key `map_id`, it relates application identifiers (`app_id`) and server identifiers (`server_id`) alongside metadata such as `environment`, `created_at`, and `updated_at` timestamps, though it is unclear which specific table provides source references due to undefined foreign keys. Despite containing no data currently, it serves as a mapping table crucial for understanding the deployment of applications across various servers in different environments.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| map_id | integer | NO | This column assigns a unique identifier to each entry in the relational mapping between applications and servers, ensuring that each mapping can be distinctly referenced. The values are auto-incremented, indicating a sequential assignment for new mappings within the dataset. |
| app_id | integer | NO | This column represents a unique identifier for different applications mapped to servers. It ensures distinct tracking and management of applications within the server environment. |
| server_id | integer | NO | This column likely represents a unique identifier for servers within a specified application server mapping context. The repeating values suggest a limited set of servers mapped to entries in the table. |
| environment | character varying | YES | Purpose unclear from available data. The column appears to contain random sentences or phrases not indicative of a specific business context. |
| created_at | timestamp without time zone | YES | This column records the date and time when an entry in the application server map was created. It defaults to the present time when the record is inserted, but its specific purpose is unclear from the available data. |
| updated_at | timestamp without time zone | YES | The column records the date and time when each entry in the table was last modified, defaulting to the current timestamp if no other value is provided. Purpose unclear from available data. |

## Primary Key

`map_id`

## Foreign Keys

- `app_id` → `synthetic.applications.app_id`

## Indexes

- `app_server_map_pkey`: CREATE UNIQUE INDEX app_server_map_pkey ON synthetic.app_server_map USING btree (map_id)

## Sample Data

| map_id | app_id | server_id | environment | created_at | updated_at |
| --- | --- | --- | --- | --- | --- |
| 1 | 42 | 2 | Such night check station message window. | Sat Dec 13 2025 03:15:50 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:15:50 GMT-0600 (Central Stan... |
| 2 | 44 | 2 | Remain son center media shake. | Sat Dec 13 2025 03:15:50 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:15:50 GMT-0600 (Central Stan... |
| 3 | 2 | 1 | Away phone coach term. | Sat Dec 13 2025 03:15:50 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:15:50 GMT-0600 (Central Stan... |
| 4 | 17 | 1 | Special tend hour serve five white. | Sat Dec 13 2025 03:15:50 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:15:50 GMT-0600 (Central Stan... |
| 5 | 38 | 2 | Minute something reach program. | Sat Dec 13 2025 03:15:50 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:15:50 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:43:10.600Z*