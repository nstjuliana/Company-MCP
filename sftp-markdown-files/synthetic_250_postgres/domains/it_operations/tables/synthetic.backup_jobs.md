# backup_jobs

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.backup_jobs" table represents scheduled tasks that perform backup operations for a system, characterized by attributes such as job identifiers, names, server associations, types, schedules, retention parameters, destinations, activity statuses, and execution logs. Despite having no direct foreign key relationships or being referenced by other tables, the table serves as a core entity for tracking and managing backup tasks, providing informative insights into the scheduling and execution outcomes. The data model supports backup management by detailing actions, configurations, and execution records, facilitating systematic data preservation efforts.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| job_id | integer | NO | This column uniquely identifies each backup job within the dataset, serving as an auto-incremented numeric identifier. It ensures that every entry is distinct for tracking and reference purposes. |
| job_name | character varying | NO | This column represents the descriptive titles assigned to individual backup jobs, reflecting varied themes or actions such as decision-making, regional support, risk management, and strategic planning. Purpose unclear from available data. |
| server_id | integer | YES | This column likely identifies servers that are involved in backup operations, distinguishing them numerically. The specific purpose of this server identification is unclear from the available data. |
| backup_type | character varying | YES | Purpose unclear from available data. The sample values do not provide a coherent understanding of what this column signifies in a business context. |
| schedule | character varying | YES | Purpose unclear from available data. The sample values appear to be incomplete or nonsensical sentences, making it challenging to determine what business information this column intends to capture. |
| retention_days | integer | YES | This column likely indicates the number of days for which backup jobs are retained in the system. The values suggest a range of retention periods, hinting at varying backup retention policies. |
| destination | character varying | YES | This column appears to represent diverse descriptive text, potentially summarizing or detailing aspects related to specific jobs or tasks involved in backup operations. The content is varied and abstract, making its specific business purpose unclear from the available data. |
| is_active | boolean | YES | This column indicates whether each backup job is currently active or not. By default, backup jobs are considered active unless otherwise specified. |
| last_run | timestamp without time zone | YES | This column records the date and time when the backup jobs were last executed. It captures run timestamps across different times of the year, reflecting obedience to daylight saving transitions. |
| last_status | character varying | YES | This column records the current status of backup jobs, indicating whether they are pending, active, or inactive. The purpose of tracking these statuses allows for monitoring and managing backup processes. |
| created_at | timestamp without time zone | YES | This column records the date and time when a backup job was created. The timestamp is captured without the time zone information and defaults to the current system time when a new entry is added. |
| updated_at | timestamp without time zone | YES | This column represents the timestamp of when a backup job was last updated. It reflects the most recent modification or update to a backup job record. |

## Primary Key

`job_id`

## Indexes

- `backup_jobs_pkey`: CREATE UNIQUE INDEX backup_jobs_pkey ON synthetic.backup_jobs USING btree (job_id)

## Sample Data

| job_id | job_name | server_id | backup_type | schedule | retention_days | destination | is_active | last_run | last_status | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Level significant usually rule effect pass. Eve... | 2 | Result environmental and garden budget. | Thought out system. | 991 | Black cup must. Media resource town fear board.... | false | Sat Mar 15 2025 10:24:23 GMT-0500 (Central Dayl... | pending | Sat Dec 13 2025 03:16:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:15 GMT-0600 (Central Stan... |
| 2 | There close possible life. Support under our re... | 2 | Fight guess speak against manage development. | Picture impact often might identify process flo... | 824 | Right clear laugh wait traditional media. Eye m... | true | Sat Nov 23 2024 10:52:33 GMT-0600 (Central Stan... | inactive | Sat Dec 13 2025 03:16:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:15 GMT-0600 (Central Stan... |
| 3 | Board produce next risk. Oil letter man chair. ... | 1 | Middle score reach owner recently. | Like play single her thought career idea. Oil h... | 145 | Not everything sign reality unit. Its none iden... | true | Sat Aug 31 2024 22:36:07 GMT-0500 (Central Dayl... | pending | Sat Dec 13 2025 03:16:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:15 GMT-0600 (Central Stan... |
| 4 | Yet voice career eat able forward sometimes. On... | 2 | Person none man throw law. | More first one dream dark health skin right. Wi... | 991 | Quality people member budget. Account skill res... | false | Sun Oct 06 2024 05:26:38 GMT-0500 (Central Dayl... | active | Sat Dec 13 2025 03:16:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:15 GMT-0600 (Central Stan... |
| 5 | Everyone way her decade check represent PM. Hai... | 2 | Book reason treat collection. | This into that. Both deep type pretty color hai... | 15 | There center respond design cause catch. Task c... | false | Mon May 05 2025 06:07:12 GMT-0500 (Central Dayl... | pending | Sat Dec 13 2025 03:16:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:15 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:43:11.939Z*