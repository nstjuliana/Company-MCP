# service_requests

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.service_requests` table represents a collection of service request records, each uniquely identified by the primary key `request_id`. The table captures various attributes of a service request including descriptors like `title`, `description`, `category`, `priority`, and `status`, along with metadata such as `requested_by`, `assigned_to`, `fulfilled_at`, `created_at`, and `updated_at`. As there are no foreign key relationships, this table functions independently within the database, likely serving as a record-keeping structure for service operations and their lifecycle statuses.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| request_id | integer | NO | This column uniquely identifies each service request in a sequential and incremental manner. It serves as a unique identifier to track individual entries within the service requests table. |
| request_number | character varying | YES | This column represents unique identifiers assigned to individual service requests. It is used to distinguish and track each request within the system. |
| title | character varying | NO | This column contains brief, descriptive phrases likely summarizing service requests or issues. Based on the varied and abstract nature of the samples, the exact purpose or context of these summaries is unclear from the available data. |
| description | text | YES | The column holds textual narratives or summaries related to a variety of topics, potentially capturing customer experience or incident details in service requests. Purpose unclear from available data. |
| category | character varying | YES | Purpose unclear from available data. |
| priority | character varying | YES | Purpose unclear from available data. |
| status | character varying | YES | This column indicates the current status of a service request, with possible states such as inactive, active, or pending. These terms reflect the progression or condition of each service request within the system. |
| requested_by | integer | YES | This column represents an identifier for individuals or entities that have made a service request. Purpose unclear from available data. |
| assigned_to | integer | YES | This column likely represents identifiers for employees or agents to whom service requests are assigned. The purpose of these specific values is unclear from the available data. |
| fulfilled_at | timestamp without time zone | YES | This column records the date and time when service requests are completed. It reflects moments in both Central Standard and Central Daylight Time, indicating fulfillment across different times of the year. |
| created_at | timestamp without time zone | YES | This column indicates the date and time when each service request was initially created. The values reflect the initiation times in the Central Standard Time zone. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a service request was most recently updated, allowing for tracking changes over time. Purpose unclear from available data. |

## Primary Key

`request_id`

## Indexes

- `service_requests_pkey`: CREATE UNIQUE INDEX service_requests_pkey ON synthetic.service_requests USING btree (request_id)
- `service_requests_request_number_key`: CREATE UNIQUE INDEX service_requests_request_number_key ON synthetic.service_requests USING btree (request_number)

## Sample Data

| request_id | request_number | title | description | category | priority | status | requested_by | assigned_to | fulfilled_at | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 455799900725668 | Capital economic high decide. | Land money cup recently positive have. Expect d... | That him design bag instead. Foreign later word... | Near last thought. | inactive | 27 | 94 | Wed Feb 26 2025 20:39:36 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:07 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:07 GMT-0600 (Central Stan... |
| 2 | 969087863914183 | Once second tonight experience. | So employee everything leader laugh. | Large collection next think direction. | Sport fly spring. | active | 985 | 691 | Sun Jul 27 2025 00:42:11 GMT-0500 (Central Dayl... | Sat Dec 13 2025 03:16:07 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:07 GMT-0600 (Central Stan... |
| 3 | 317718626678616 | Somebody she hot. | Drop voice central son. Field standard middle f... | Stage whole power expert car. Herself answer mu... | Fight property hear. | pending | 602 | 974 | Mon Dec 30 2024 15:25:22 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:07 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:07 GMT-0600 (Central Stan... |
| 4 | 969001923315240 | Throughout but finish. | Method environment soon left military wish. Pre... | Behavior environment someone. Hour her increase... | Hope school walk. | active | 784 | 689 | Mon Sep 02 2024 20:13:38 GMT-0500 (Central Dayl... | Sat Dec 13 2025 03:16:07 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:07 GMT-0600 (Central Stan... |
| 5 | 612038467264401 | Want send pay relate member. | Throughout quickly still word. Theory political... | Exist represent somebody suggest each share sim... | Probably your stay. | inactive | 591 | 42 | Sat Aug 24 2024 04:21:37 GMT-0500 (Central Dayl... | Sat Dec 13 2025 03:16:07 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:07 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:31.126Z*