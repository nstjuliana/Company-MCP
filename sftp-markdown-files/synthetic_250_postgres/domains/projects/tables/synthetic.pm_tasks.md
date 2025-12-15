# pm_tasks

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.pm_tasks" table represents tasks to be managed within a project management schema, capturing details like the task name, description, start, due, and completion dates, estimated and actual hours, priority, and status, potentially for project monitoring and tracking purposes. It holds a primary key "task_id" to uniquely identify each task and includes foreign keys such as "project_id", "phase_id", and "milestone_id", suggesting its linkage to overarching project structures and phases, although specific relationship details are not defined. This table's role likely involves tracking task progress and details within projects, without direct reference from other tables.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| task_id | integer | NO | Represents a unique identifier for each task within the project management system to ensure distinct task records. |
| project_id | integer | NO | This column likely identifies and associates tasks with specific projects within a project management system, where each number represents a unique project. |
| phase_id | integer | YES | This column represents the identifier for different phases associated with tasks in project management. Purpose unclear from available data. |
| milestone_id | integer | YES | This column likely associates each task with a specific milestone within a project, using numeric identifiers to link tasks to their corresponding project milestones. Purpose unclear from available data. |
| parent_task_id | integer | YES | This column likely represents the identifier of a task that serves as the parent or preceding task to the current one, suggesting a task hierarchy or sequence within a project management context. Purpose unclear from available data. |
| task_name | character varying | NO | This column stores descriptions or titles of tasks that are likely related to projects or activities, featuring a blend of abstract and action-oriented statements. Purpose unclear from available data. |
| description | text | YES | This column contains textual entries that likely describe tasks or activities in detail, often involving elements related to decision-making, scenarios, or conditions. However, the exact purpose behind these descriptions is unclear from the available data. |
| assigned_to | integer | YES | This column likely represents identifiers for employees, team members, or users to whom tasks are assigned in a project management context. Purpose unclear from available data. |
| start_date | date | YES | This column indicates the scheduled commencement date for tasks in project management, likely used to plan and track task timelines. Dates reflect various times of the year, suggesting the tasks can occur across different seasons. |
| due_date | date | YES | This column represents the scheduled completion or deadline date for tasks within a project management context. It indicates when a task is expected to be completed, allowing for planning and tracking within the specified timeframes. |
| completed_date | date | YES | This column indicates the date on which a task was completed. It may remain empty if the task is not yet finished. |
| estimated_hours | numeric | YES | This column represents the estimated number of hours required to complete specific project management tasks. Purpose unclear from available data. |
| actual_hours | numeric | YES | This column represents the number of hours actually spent on various project management tasks, as opposed to planned or estimated hours. The values are measured in decimal format to capture partial hours accurately. |
| priority | character varying | YES | Purpose unclear from available data. |
| status | character varying | YES | This column indicates the current state of a task, reflecting whether it is ongoing, deferred, or concluded, with possible values including active, pending, inactive, and completed. Tasks may also be noted as cancelled if they are terminated before completion. |
| created_at | timestamp without time zone | YES | This column logs the date and time when a task record is initially created. It captures the precise moment of task entry, with default settings recording the current timestamp unless otherwise specified. |
| updated_at | timestamp without time zone | YES | This column records the date and time a task's details were last modified. It captures the most recent updates, ensuring the task's information is current as of the latest edit. |

## Primary Key

`task_id`

## Foreign Keys

- `milestone_id` → `synthetic.milestones.milestone_id`
- `parent_task_id` → `synthetic.pm_tasks.task_id`
- `phase_id` → `synthetic.project_phases.phase_id`
- `project_id` → `synthetic.pm_projects.project_id`

## Indexes

- `pm_tasks_pkey`: CREATE UNIQUE INDEX pm_tasks_pkey ON synthetic.pm_tasks USING btree (task_id)

## Sample Data

| task_id | project_id | phase_id | milestone_id | parent_task_id | task_name | description | assigned_to | start_date | due_date | completed_date | estimated_hours | actual_hours | priority | status | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 29 | 21 | 3 | null | Today pressure score network. School buy media ... | Realize model he interest their age image fine.... | 264 | Sun Mar 02 2025 00:00:00 GMT-0600 (Central Stan... | Wed Jul 03 2024 00:00:00 GMT-0500 (Central Dayl... | Tue Nov 18 2025 00:00:00 GMT-0600 (Central Stan... | 959.80 | 265.75 | Field democratic. | inactive | Sat Dec 13 2025 03:00:02 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:00:02 GMT-0600 (Central Stan... |
| 2 | 45 | 42 | 7 | 1 | Box free accept blue no feel. Forget through fr... | Create three claim mean wall movie traditional.... | 1428 | Fri Dec 05 2025 00:00:00 GMT-0600 (Central Stan... | Sun Jun 22 2025 00:00:00 GMT-0500 (Central Dayl... | Wed Mar 13 2024 00:00:00 GMT-0500 (Central Dayl... | 35.19 | 353.86 | Mission person. | completed | Sat Dec 13 2025 03:00:02 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:00:02 GMT-0600 (Central Stan... |
| 3 | 25 | 40 | 34 | 1 | Line camera yourself different because meet mee... | Who tell politics matter size. Road choose pres... | 9695 | Wed Apr 03 2024 00:00:00 GMT-0500 (Central Dayl... | Thu Jun 05 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Oct 25 2025 00:00:00 GMT-0500 (Central Dayl... | 523.72 | 561.49 | Per indicate safe. | cancelled | Sat Dec 13 2025 03:00:02 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:00:02 GMT-0600 (Central Stan... |
| 4 | 47 | 9 | 49 | 2 | First suffer none those perhaps. Call relations... | Bank change eat or. | 111 | Wed Sep 24 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Apr 20 2024 00:00:00 GMT-0500 (Central Dayl... | Mon Nov 18 2024 00:00:00 GMT-0600 (Central Stan... | 271.68 | 129.78 | Feeling begin. | cancelled | Sat Dec 13 2025 03:00:02 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:00:02 GMT-0600 (Central Stan... |
| 5 | 34 | 36 | 50 | 3 | Policy between particularly store answer.
Emplo... | Key little ground there bring leg. | 6590 | Sun Jul 20 2025 00:00:00 GMT-0500 (Central Dayl... | Sat May 17 2025 00:00:00 GMT-0500 (Central Dayl... | Sun Mar 30 2025 00:00:00 GMT-0500 (Central Dayl... | 162.79 | 136.85 | Four discover. | pending | Sat Dec 13 2025 03:00:02 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:00:02 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:42:10.755Z*