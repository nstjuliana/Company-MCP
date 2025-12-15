# degree_requirements

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.degree_requirements" table represents the academic requirements a student must satisfy to complete a specific program, identified by unique records for each requirement. It includes details such as the associated program and course (via the "program_id" and "course_id" columns), type of requirement, required credit hours, the minimum grade needed, and whether the requirement is mandatory, along with timestamps of when the record was created and last updated. The table references undefined relationships with other tables, suggesting it forms part of a broader educational data model encompassing programs and courses structure.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| requirement_id | integer | NO | This column uniquely identifies each entry in the table of degree requirements, serving as a primary key for distinguishing different sets of requirements. |
| program_id | integer | NO | This column represents unique identifiers for various educational programs associated with specific degree requirements. |
| course_id | integer | YES | This column represents unique identifiers for courses that are part of a degree's requirements. Each number corresponds to a specific course needed to fulfill the educational program. |
| requirement_type | character varying | YES | Purpose unclear from available data. The sample values do not provide a clear insight into what this column represents in business terms. |
| credit_hours | integer | YES | This column represents the number of credit hours associated with a specific requirement needed for degree completion. Purpose unclear from available data. |
| minimum_grade | character varying | YES | Purpose unclear from available data. |
| is_required | boolean | YES | Indicates whether a specific course or requirement is essential to fulfill the criteria for completing a degree program. Its default value suggests that most requirements are considered essential unless otherwise specified. |
| created_at | timestamp without time zone | YES | This column records the date and time when a particular entry in the degree requirements table was initially created. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a modification was last made to a record in the degree requirements table. It is automatically set to the current timestamp when the record is inserted or updated. |

## Primary Key

`requirement_id`

## Foreign Keys

- `course_id` → `synthetic.courses.course_id`
- `program_id` → `synthetic.programs.program_id`

## Indexes

- `degree_requirements_pkey`: CREATE UNIQUE INDEX degree_requirements_pkey ON synthetic.degree_requirements USING btree (requirement_id)

## Sample Data

| requirement_id | program_id | course_id | requirement_type | credit_hours | minimum_grade | is_required | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 18 | 3 | Outside way remember just Republican. | 947 | Each. | true | Sat Dec 13 2025 03:17:07 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:07 GMT-0600 (Central Stan... |
| 2 | 44 | 18 | Like rich chance former everything offer. | 921 | Beat. | true | Sat Dec 13 2025 03:17:07 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:07 GMT-0600 (Central Stan... |
| 3 | 12 | 21 | Probably of least yourself. | 17 | Top. | true | Sat Dec 13 2025 03:17:07 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:07 GMT-0600 (Central Stan... |
| 4 | 38 | 10 | Should six audience organization the data sister. | 771 | City. | false | Sat Dec 13 2025 03:17:07 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:07 GMT-0600 (Central Stan... |
| 5 | 5 | 20 | Trip crime some security. | 167 | Fact. | true | Sat Dec 13 2025 03:17:07 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:07 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:56.290Z*