# territory_assignments

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.territory_assignments` table represents the allocation of specific territories to users or accounts, where each assignment is uniquely identified by `assignment_id`. It does not establish clear foreign key relationships with other tables in the schema but involves associations with territories, users, and accounts via `territory_id`, `user_id`, and `account_id` columns. This table primarily tracks assignment types and timestamps for creation and updates, suggesting its role in managing and auditing territory allocation activities within the business model.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| assignment_id | integer | NO | This column represents a unique identifier for each territory assignment. It ensures that every territory assignment can be individually distinguished within the system. |
| territory_id | integer | NO | This column represents unique identifiers for territories, which are used to assign them within a specific context or function as part of the database table. Purpose unclear from available data. |
| user_id | integer | YES | This column represents a unique identifier for users associated with territory assignments. Purpose unclear from available data beyond indicating user involvement. |
| account_id | integer | YES | This column likely represents identifiers for different accounts associated with territory assignments. Each value corresponds to a unique account, but the specific nature of these accounts is not clear from the available data. |
| assignment_type | character varying | YES | Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a territory assignment entry is created, reflecting the local time setting. The information helps track the initiation of each assigned territory task or record. |
| updated_at | timestamp without time zone | YES | This column records the date and time when each territory assignment was last modified. It is automatically populated with the current timestamp upon updating an entry. |

## Primary Key

`assignment_id`

## Foreign Keys

- `account_id` → `synthetic.accounts.account_id`
- `territory_id` → `synthetic.territories.territory_id`

## Indexes

- `territory_assignments_pkey`: CREATE UNIQUE INDEX territory_assignments_pkey ON synthetic.territory_assignments USING btree (assignment_id)

## Sample Data

| assignment_id | territory_id | user_id | account_id | assignment_type | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 7 | 6859 | 31 | one | Sat Dec 13 2025 02:59:04 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:04 GMT-0600 (Central Stan... |
| 2 | 3 | 4570 | 28 | join | Sat Dec 13 2025 02:59:04 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:04 GMT-0600 (Central Stan... |
| 3 | 36 | 6919 | 5 | ago | Sat Dec 13 2025 02:59:04 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:04 GMT-0600 (Central Stan... |
| 4 | 5 | 1430 | 17 | try | Sat Dec 13 2025 02:59:04 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:04 GMT-0600 (Central Stan... |
| 5 | 43 | 5860 | 31 | generation | Sat Dec 13 2025 02:59:04 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:04 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:26.641Z*