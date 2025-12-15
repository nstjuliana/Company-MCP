# performance_goals

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.performance_goals" table represents performance goals for employees, indicated by columns such as "employee_id," "goal_title," and "description," with key performance metrics like "target_date," "completion_percentage," and "status." The primary key "goal_id" uniquely identifies each goal, and relationships with other tables are not well-defined. This table is fundamental for tracking employee performance objectives, aligning with organizational targets, and monitoring progress towards goal completion.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| goal_id | integer | NO | This column represents unique identifiers assigned to individual performance goals, ensuring each goal can be distinctly tracked and referenced within the system. |
| employee_id | integer | NO | This column represents the unique identifier for employees within the organization. It is used to associate individual employees with their respective performance goals. |
| goal_title | character varying | NO | This column represents titles or brief descriptions of objectives or goals related to various thematic areas such as market opportunities, social interactions, and organizational dynamics. Purpose unclear from available data. |
| description | text | YES | This column captures narrative or abstract descriptions of performance goals, likely summarizing objectives, plans, or considerations. Purpose unclear from available data. |
| category | character varying | YES | This column appears to categorize broad themes or topics related to performance goals, as illustrated by the diverse, abstract descriptions. The purpose of these categorizations is unclear from the available data. |
| target_date | date | YES | This column represents the deadline by which specific performance goals are expected to be achieved within an organization. The values indicate target dates for various goals extending from early 2024 to late 2025. |
| completion_percentage | integer | YES | This column represents the percentage of completion toward a specific goal, with values indicating varying levels of progress ranging from no progress (0%) to near completion (up to 98%). Its purpose within the business context is unclear from the available data. |
| status | character varying | YES | This column indicates the current status of a performance goal, showing whether it is "pending," "inactive," or "active." These statuses reflect the progress or implementation stage of each goal within the associated business process. |
| weight | numeric | YES | This column likely represents weighted values attributed to specific performance goals within a business context. The purpose of these weights is unclear from the available data. |
| created_at | timestamp without time zone | YES | This column likely records the date and time when a performance goal entry was created or logged. It is used to track the creation timestamp of each entry within the performance goals table. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a performance goal was last updated, reflecting either an edit or a verification action. Purpose unclear from available data. |

## Primary Key

`goal_id`

## Foreign Keys

- `employee_id` → `synthetic.employees.employee_id`

## Indexes

- `performance_goals_pkey`: CREATE UNIQUE INDEX performance_goals_pkey ON synthetic.performance_goals USING btree (goal_id)

## Sample Data

| goal_id | employee_id | goal_title | description | category | target_date | completion_percentage | status | weight | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 28 | Opportunity late market. | Local a case effect. With project author term m... | Change available cut during. | Sun Nov 09 2025 00:00:00 GMT-0600 (Central Stan... | 62 | pending | 442.04 | Sat Dec 13 2025 03:20:04 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:20:04 GMT-0600 (Central Stan... |
| 2 | 18 | Democratic close make low. | World continue just hope share leave fund offic... | Too recognize final boy begin show forget. | Thu May 30 2024 00:00:00 GMT-0500 (Central Dayl... | 27 | pending | 113.82 | Sat Dec 13 2025 03:20:04 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:20:04 GMT-0600 (Central Stan... |
| 3 | 28 | Animal building attorney. | Main her year none lay TV. | According anyone cell why less fill name. | Sun Oct 13 2024 00:00:00 GMT-0500 (Central Dayl... | 14 | inactive | 678.22 | Sat Dec 13 2025 03:20:04 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:20:04 GMT-0600 (Central Stan... |
| 4 | 38 | History girl real. | Teach almost image good recognize. | Current open history evening interview cost less. | Sat May 03 2025 00:00:00 GMT-0500 (Central Dayl... | 62 | pending | 667.13 | Sat Dec 13 2025 03:20:04 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:20:04 GMT-0600 (Central Stan... |
| 5 | 3 | Fly anyone he. | Conference glass claim. Leg purpose interview d... | Send themselves walk factor determine remember. | Tue Feb 25 2025 00:00:00 GMT-0600 (Central Stan... | 28 | inactive | 984.45 | Sat Dec 13 2025 03:20:04 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:20:04 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:22.084Z*