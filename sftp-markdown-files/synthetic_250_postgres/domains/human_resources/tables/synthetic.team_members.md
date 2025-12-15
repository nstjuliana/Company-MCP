# team_members

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.team_members` table represents individuals associated with specific teams, capturing their roles and leadership status within the team. Each entry is uniquely identified by the `team_member_id` and includes details such as `team_id`, `user_id`, `role`, whether the member is a leader (`is_leader`), and timestamps for creation and updates (`created_at`, `updated_at`). While the table's primary relationship with other tables is undefined, it plays a crucial role in managing team composition and member roles in the data structure.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| team_member_id | integer | NO | This column uniquely identifies each team member within the synthetic.team_members table, using sequential integer values. |
| team_id | integer | NO | This column likely represents a unique identifier for teams within the system, as indicated by the diverse sample values. Each integer is assigned to a team member to designate their association with a specific team. |
| user_id | integer | NO | A unique identifier assigned to each member of a team, ensuring the distinct identification of individuals within the team data. Purpose unclear from available data. |
| role | character varying | YES | Purpose unclear from available data. The sample values suggest descriptive text possibly related to roles or activities. |
| is_leader | boolean | YES | This column indicates whether a team member holds a leadership position within the team. The values suggest that the majority of team members are not leaders. |
| created_at | timestamp without time zone | YES | This column records the date and time when a team member's information was first added to the database. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a team member's information was last modified, helping track the most recent updates. Purpose unclear from available data. |

## Primary Key

`team_member_id`

## Foreign Keys

- `team_id` → `synthetic.sales_teams.team_id`

## Indexes

- `team_members_pkey`: CREATE UNIQUE INDEX team_members_pkey ON synthetic.team_members USING btree (team_member_id)

## Sample Data

| team_member_id | team_id | user_id | role | is_leader | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 17 | 9929 | Plant hundred science. Order thousand into natu... | true | Sat Dec 13 2025 02:59:10 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:10 GMT-0600 (Central Stan... |
| 2 | 17 | 2039 | Student per top third institution. Chance marri... | false | Sat Dec 13 2025 02:59:10 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:10 GMT-0600 (Central Stan... |
| 3 | 36 | 6441 | Wonder man scientist sure hand Democrat. Heart ... | true | Sat Dec 13 2025 02:59:10 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:10 GMT-0600 (Central Stan... |
| 4 | 5 | 3096 | Anyone sport force deep everyone believe. Every... | false | Sat Dec 13 2025 02:59:10 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:10 GMT-0600 (Central Stan... |
| 5 | 32 | 7451 | Fact anyone think. Number major set spring arti... | false | Sat Dec 13 2025 02:59:10 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:10 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:04.513Z*