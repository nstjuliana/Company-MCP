# task_assignments

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.task_assignments" table represents the allocation of tasks to users, with details on each assignment including the assigned task, user, role specifics, and allocation percentage. The table stores data on when assignments were created and last updated, uniquely identifying each entry with an "assignment_id" primary key. Due to the lack of defined foreign key relationships, its integration with other tables cannot be discerned, though it likely participates in task management workflows.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| assignment_id | integer | NO | This column represents a unique identifier assigned to each task within the task assignments table, ensuring that each task can be distinctly referenced within the dataset. The identifier is sequentially generated, as evidenced by the sample values. |
| task_id | integer | NO | This column represents unique identifiers assigned to individual tasks within an assignment system. It ensures that each task can be distinctly referenced in the database. |
| user_id | integer | NO | This column likely represents a unique identifier assigned to each user assigned a task, ensuring they can be distinctly identified within the task assignments system. Purpose unclear from available data. |
| role | character varying | YES | Purpose unclear from available data. The sample values suggest descriptive phrases or sentences related to tasks, roles, or activities, but the exact business meaning is not evident. |
| allocation_percentage | integer | YES | This column likely represents the percentage of a task's resources or time that is allocated to a specific entity or individual. A default value of 100 suggests that full allocation is the norm unless specified otherwise. |
| created_at | timestamp without time zone | YES | This column records the date and time when a task assignment was initially created. It uses a default value to automatically capture the current timestamp upon record insertion. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a task assignment was last modified. The timestamp defaults to the current time, indicating updates are logged automatically upon modification. |

## Primary Key

`assignment_id`

## Foreign Keys

- `task_id` → `synthetic.pm_tasks.task_id`

## Indexes

- `task_assignments_pkey`: CREATE UNIQUE INDEX task_assignments_pkey ON synthetic.task_assignments USING btree (assignment_id)

## Sample Data

| assignment_id | task_id | user_id | role | allocation_percentage | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 24 | 2654 | Choice amount it middle artist consumer her. Pe... | 61 | Sat Dec 13 2025 03:00:08 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:00:08 GMT-0600 (Central Stan... |
| 2 | 15 | 9135 | Budget where lead fish despite down research. | 63 | Sat Dec 13 2025 03:00:08 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:00:08 GMT-0600 (Central Stan... |
| 3 | 18 | 989 | Impact manager trip lawyer executive peace. | 21 | Sat Dec 13 2025 03:00:08 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:00:08 GMT-0600 (Central Stan... |
| 4 | 39 | 1008 | Lot compare become enough for defense seem kid. | 56 | Sat Dec 13 2025 03:00:08 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:00:08 GMT-0600 (Central Stan... |
| 5 | 47 | 1399 | Contain happen least hard worry majority. Like ... | 55 | Sat Dec 13 2025 03:00:08 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:00:08 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:43:42.169Z*