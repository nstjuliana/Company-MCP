# change_tickets

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.change_tickets` table represents a collection of change requests or tickets within an organizational context, tracking details necessary for managing and executing changes. Each record captures comprehensive information about a change, including its type, risk assessment, status, and relevant timelines, along with identifiers for users involved in the request and execution process. As it stands without relationships to other tables, the table likely functions independently, fulfilling the need to log and manage change events as a self-contained entity within the broader data schema.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| change_id | integer | NO | This column represents a unique identifier for each change ticket and ensures that each entry is distinct within the change management system. |
| change_number | character varying | YES | This column represents unique identifiers for individual change tickets, allowing them to be distinctly tracked and referenced. Purpose unclear from available data. |
| title | character varying | NO | This column represents brief, descriptive summaries or titles for change tickets, capturing key themes or concepts related to the content of each ticket. Purpose unclear from available data. |
| description | text | YES | This column contains verbose narratives or summaries related to change tickets, which could describe scenarios, tasks, or issues requiring change, with a wide range of themes from personal observations to broader organizational contexts. Purpose unclear from available data. |
| change_type | character varying | YES | Purpose unclear from available data. The values appear to be fragmented and do not clearly represent any specific business term or context. |
| risk_level | character varying | YES | Purpose unclear from available data. |
| status | character varying | YES | The column represents the current state of change tickets, indicating whether they are active, inactive, or pending further action. This status helps track the progress and handling stage of each ticket within a process. |
| requested_by | integer | YES | This column represents identifiers for individuals responsible for initiating change ticket requests. The purpose of these identifiers remains unclear from the available data, as they are only numeric codes without further context. |
| assigned_to | integer | YES | This column likely identifies the person or team responsible for handling a change ticket by referencing their unique numeric identifier. Purpose unclear from available data. |
| planned_start | timestamp without time zone | YES | This column specifies the intended start date and time for change-related activities or tasks. Purpose unclear from available data as no additional context or business processes are provided. |
| planned_end | timestamp without time zone | YES | This column indicates the scheduled completion date and time for a change ticket in a project or organizational change process. The purpose is to track when changes are expected to be finalized. |
| actual_start | timestamp without time zone | YES | This column stores the date and time when a change ticket actually began, noted in Central Time zones, reflecting either daylight saving or standard time. It is used to capture the real start time of a change event, which may differ from scheduled times. |
| actual_end | timestamp without time zone | YES | Represents the date and time when a change ticket was actually completed. This information can vary as it reflects different time zones but consistently marks the conclusion of the designated task or process. |
| approved_by | integer | YES | This column represents the unique identification numbers of individuals who have approved change tickets. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column captures the date and time when a change ticket is created, defaulting to the current timestamp unless specified otherwise. It is used to track the creation time of change tickets without considering the time zone. |
| updated_at | timestamp without time zone | YES | This column indicates the date and time when an entry in the change tickets table was last updated. It reflects modifications to the ticket and defaults to the current timestamp when new records are created, but can be updated with the time of any subsequent changes. |

## Primary Key

`change_id`

## Indexes

- `change_tickets_change_number_key`: CREATE UNIQUE INDEX change_tickets_change_number_key ON synthetic.change_tickets USING btree (change_number)
- `change_tickets_pkey`: CREATE UNIQUE INDEX change_tickets_pkey ON synthetic.change_tickets USING btree (change_id)

## Sample Data

| change_id | change_number | title | description | change_type | risk_level | status | requested_by | assigned_to | planned_start | planned_end | actual_start | actual_end | approved_by | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 771148816058019 | Provide television government majority. | Husband scene high whatever. Enjoy safe before.... | See management pick morning. | Dream left. | pending | 378 | 485 | Sat Dec 21 2024 06:20:32 GMT-0600 (Central Stan... | Fri Oct 11 2024 14:13:16 GMT-0500 (Central Dayl... | Sat Jun 28 2025 12:56:30 GMT-0500 (Central Dayl... | Sat Apr 20 2024 12:57:15 GMT-0500 (Central Dayl... | 567 | Sat Dec 13 2025 03:16:03 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:03 GMT-0600 (Central Stan... |
| 2 | 849704241698142 | Knowledge him. | Keep action investment back. Detail growth line... | Ahead management add. | On enough country. | pending | 353 | 436 | Sun Jul 07 2024 19:47:40 GMT-0500 (Central Dayl... | Sat Sep 07 2024 00:29:39 GMT-0500 (Central Dayl... | Sun Nov 10 2024 21:49:25 GMT-0600 (Central Stan... | Mon Feb 26 2024 09:17:25 GMT-0600 (Central Stan... | 764 | Sat Dec 13 2025 03:16:03 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:03 GMT-0600 (Central Stan... |
| 3 | 677066721922834 | Ten else action play somebody. | Citizen weight seat performance movement cultur... | Generation once environment. | Traditional notice. | pending | 339 | 361 | Sat Feb 17 2024 14:10:33 GMT-0600 (Central Stan... | Wed Apr 16 2025 16:25:50 GMT-0500 (Central Dayl... | Fri Apr 12 2024 01:27:48 GMT-0500 (Central Dayl... | Tue Jun 17 2025 04:02:25 GMT-0500 (Central Dayl... | 720 | Sat Dec 13 2025 03:16:03 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:03 GMT-0600 (Central Stan... |
| 4 | 208361088025701 | Themselves collection another president. | Artist top until people those performance fish.... | Must however them cover task approach. | Choose could. | inactive | 278 | 314 | Thu Sep 11 2025 04:22:23 GMT-0500 (Central Dayl... | Sun Sep 01 2024 01:51:03 GMT-0500 (Central Dayl... | Wed Jul 23 2025 11:53:14 GMT-0500 (Central Dayl... | Mon Dec 08 2025 15:03:33 GMT-0600 (Central Stan... | 258 | Sat Dec 13 2025 03:16:03 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:03 GMT-0600 (Central Stan... |
| 5 | 069409787387183 | Throughout senior word. | Hope music middle yeah whose drive. | Ability move recent weight market although. | Feel fear manage. | active | 124 | 739 | Mon Mar 03 2025 10:30:47 GMT-0600 (Central Stan... | Fri Jan 19 2024 14:47:00 GMT-0600 (Central Stan... | Sun Aug 10 2025 22:54:10 GMT-0500 (Central Dayl... | Tue Jul 30 2024 10:05:27 GMT-0500 (Central Dayl... | 198 | Sat Dec 13 2025 03:16:03 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:03 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:43:11.437Z*