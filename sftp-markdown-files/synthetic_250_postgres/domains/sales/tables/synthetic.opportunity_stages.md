# opportunity_stages

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.opportunity_stages` table represents the various stages through which a business opportunity progresses, with attributes detailing the stage name, probabilistic metrics like the likelihood of conversion (probability), and order of stages (sort_order). The boolean columns `is_closed` and `is_won` indicate whether the stage has concluded and if it resulted in a successful outcome, respectively. This standalone table plays a critical role in documenting and tracking opportunity progressions but does not establish direct relationships with other tables within the database schema.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| stage_id | integer | NO | This column represents the sequential identification number for different stages within an opportunity management process, ensuring each stage is uniquely recognized and ordered. The numbers likely correspond to progressive stages or steps an opportunity passes through. |
| stage_name | character varying | NO | The column specifies different stages or phases related to a process or project, indicated through descriptive phrases. Its purpose and specific context remain unclear from the available data. |
| probability | integer | YES | Purpose unclear from available data. |
| sort_order | integer | YES | This column appears to represent the sequence or priority of opportunity stages, likely indicating their order or rank in a process. The purpose beyond ordering is unclear from available data. |
| is_closed | boolean | YES | Indicates whether an opportunity stage has reached completion. A value of true suggests the stage is closed, whereas false implies it is still open or active. |
| is_won | boolean | YES | This column indicates whether an opportunity has been successfully closed as a "won" deal, with "true" representing a win and "false" a non-win status. |
| created_at | timestamp without time zone | YES | This column records the date and time when an opportunity stage was created, reflecting the initial entry point of a stage within the opportunity lifecycle. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a stage in an opportunity was last modified, reflecting updates to the opportunity's progression through different stages. Purpose unclear from available data. |

## Primary Key

`stage_id`

## Indexes

- `opportunity_stages_pkey`: CREATE UNIQUE INDEX opportunity_stages_pkey ON synthetic.opportunity_stages USING btree (stage_id)

## Sample Data

| stage_id | stage_name | probability | sort_order | is_closed | is_won | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Herself level dinner throw detail move. Detail ... | 7984 | 4770 | true | true | Sat Dec 13 2025 02:58:35 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:35 GMT-0600 (Central Stan... |
| 2 | Watch describe commercial himself. Environment ... | 1452 | 9885 | false | true | Sat Dec 13 2025 02:58:35 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:35 GMT-0600 (Central Stan... |
| 3 | Say risk news today couple full seem. Cold fear... | 8103 | 7086 | false | true | Sat Dec 13 2025 02:58:35 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:35 GMT-0600 (Central Stan... |
| 4 | Which blood student animal it everything reveal... | 1724 | 4591 | false | false | Sat Dec 13 2025 02:58:35 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:35 GMT-0600 (Central Stan... |
| 5 | Nearly first reach know west draw. Relationship... | 8321 | 5388 | false | false | Sat Dec 13 2025 02:58:35 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:35 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:55.777Z*