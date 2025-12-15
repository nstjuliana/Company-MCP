# programs

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "programs" table in the "synthetic_250_postgres" database models academic programs, capturing details such as the program identifier, code, name, associated department, degree type, credit hour requirements, a descriptive overview, and status indicators like active status. The primary key "program_id" uniquely identifies each program, while the "department_id" suggests a potential relationship with a departments table, although this relationship is not defined in the foreign key constraints. It serves as a foundational entity for managing academic offerings within an educational institution, potentially linking to departments and influencing curriculum planning systems.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| program_id | integer | NO | This column represents a unique identifier for each entry in the programs table. It is used to distinctly distinguish each program within the dataset. |
| program_code | character varying | YES | This column likely represents a unique identifier or code associated with each program offered. The specific purpose or categorization of these codes is unclear from the available data. |
| program_name | character varying | NO | This column represents the titles or names of various programs, which appear to relate to educational or professional initiatives, projects, or events. The names suggest themes involving strategic actions, scientific advancements, societal issues, and organizational endeavors. |
| department_id | integer | YES | This column likely represents identifiers for various departments associated with programs. The purpose of these identifiers is unclear from the available data. |
| degree_type | character varying | YES | Purpose unclear from available data. |
| credit_hours_required | integer | YES | This column represents the number of credit hours a program requires for completion. Purpose unclear from available data. |
| description | text | YES | This column contains brief narrative snippets or summaries related to various topics such as current affairs, personal experiences, and socioeconomic observations. The purpose of these descriptions remains unclear from the available data. |
| is_active | boolean | YES | Indicates whether a program is currently operational or inactive. By default, programs are considered operational unless specified otherwise. |
| created_at | timestamp without time zone | YES | This column records the date and time when a program entry was created, defaulting to the current timestamp if not specified. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column captures the date and time when a program record was last modified. It is set to the current timestamp by default, indicating the most recent update to the database entry. |

## Primary Key

`program_id`

## Foreign Keys

- `department_id` → `synthetic.academic_departments.department_id`

## Indexes

- `programs_pkey`: CREATE UNIQUE INDEX programs_pkey ON synthetic.programs USING btree (program_id)
- `programs_program_code_key`: CREATE UNIQUE INDEX programs_program_code_key ON synthetic.programs USING btree (program_code)

## Sample Data

| program_id | program_code | program_name | department_id | degree_type | credit_hours_required | description | is_active | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | OKIZDTZA | Indicate far trade care board. Something party ... | 37 | Within allow exist necessary into read. | 272 | Heart state job current cost. Including signifi... | true | Sat Dec 13 2025 03:16:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:45 GMT-0600 (Central Stan... |
| 2 | TIXOPOAB | Company property until go final. Choose answer ... | 50 | Herself night similar someone seek vote. | 586 | Let she send would with. Fine future peace caus... | false | Sat Dec 13 2025 03:16:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:45 GMT-0600 (Central Stan... |
| 3 | QODLSFHM | Result look science leg small modern. Successfu... | 40 | A cultural plant financial benefit only trip. | 655 | Me whole summer best. | true | Sat Dec 13 2025 03:16:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:45 GMT-0600 (Central Stan... |
| 4 | TCMWWKFG | Report century rule as have probably. Provide r... | 32 | Best man be tax population art magazine. | 911 | Occur money idea economy main Mrs senior. Claim... | false | Sat Dec 13 2025 03:16:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:45 GMT-0600 (Central Stan... |
| 5 | IYIFWMAR | Policy science cell stop bit for. Question deep... | 42 | Parent member century enough month decision. | 980 | View boy dog modern particularly weight. Phone ... | false | Sat Dec 13 2025 03:16:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:45 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:30.297Z*