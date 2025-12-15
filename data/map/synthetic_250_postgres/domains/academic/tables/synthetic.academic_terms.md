# academic_terms

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.academic_terms" table represents periods or sessions within an academic institution, identified by a unique "term_id" and characterized by a "term_code" and "term_name." It includes date ranges for both the term and its registration period, and indicates whether the term is current, with timestamped entries for creation and last update. As it has no foreign key relationships, this table likely serves as a standalone entity within the database to encapsulate academic scheduling information.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| term_id | integer | NO | This column represents a unique identifier for academic terms within an educational institution's system. The sequential values suggest an automatic incrementing sequence to ensure each term is distinctly identifiable. |
| term_code | character varying | YES | Purpose unclear from available data. The values appear to be randomly generated strings and do not provide insight into their meaning or usage. |
| term_name | character varying | NO | Purpose unclear from available data. The sample values do not provide discernible information connecting them to a specific academic term. |
| start_date | date | YES | This column records the start dates for academic terms, likely representing when each term begins during different years. The values indicate specific weekdays and account for variations in daylight saving time within the Central time zone. |
| end_date | date | YES | This column represents the final date by which an academic term concludes within the institution's calendar. The dates indicate variations in end dates presumably due to differing start times or specific term durations. |
| registration_start | date | YES | This column represents the start date for when students can begin registering for academic terms. The dates vary, indicating they align with specific term schedules throughout the academic year. |
| registration_end | date | YES | This column represents the date by which registration for an academic term must be completed. If not specified, this deadline may not be applicable or determined for every term. |
| is_current | boolean | YES | Indicates whether an academic term is currently active. The default setting suggests that terms are generally not considered active unless specified otherwise. |
| created_at | timestamp without time zone | YES | Records the date and time when a new academic term entry is created. The timestamp defaults to the current moment when the entry is added. |
| updated_at | timestamp without time zone | YES | This column represents the timestamp indicating when the academic term record was last updated. It defaults to the current timestamp but may remain null if not explicitly set. |

## Primary Key

`term_id`

## Indexes

- `academic_terms_pkey`: CREATE UNIQUE INDEX academic_terms_pkey ON synthetic.academic_terms USING btree (term_id)
- `academic_terms_term_code_key`: CREATE UNIQUE INDEX academic_terms_term_code_key ON synthetic.academic_terms USING btree (term_code)

## Sample Data

| term_id | term_code | term_name | start_date | end_date | registration_start | registration_end | is_current | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | RVTEJPBR | Employee shake cell idea card certainly notice.... | Tue Feb 20 2024 00:00:00 GMT-0600 (Central Stan... | Fri Jul 05 2024 00:00:00 GMT-0500 (Central Dayl... | Thu Feb 13 2025 00:00:00 GMT-0600 (Central Stan... | Thu Jul 10 2025 00:00:00 GMT-0500 (Central Dayl... | true | Sat Dec 13 2025 03:16:54 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:54 GMT-0600 (Central Stan... |
| 2 | FQFCGBTF | Shoulder allow anything beyond wear attention. ... | Mon Apr 21 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Mar 02 2024 00:00:00 GMT-0600 (Central Stan... | Sat Jul 06 2024 00:00:00 GMT-0500 (Central Dayl... | Wed Oct 30 2024 00:00:00 GMT-0500 (Central Dayl... | true | Sat Dec 13 2025 03:16:54 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:54 GMT-0600 (Central Stan... |
| 3 | HTRWZOYI | Fact time instead worry decade. Author type fas... | Wed Sep 11 2024 00:00:00 GMT-0500 (Central Dayl... | Fri Nov 01 2024 00:00:00 GMT-0500 (Central Dayl... | Fri Dec 20 2024 00:00:00 GMT-0600 (Central Stan... | Wed Apr 16 2025 00:00:00 GMT-0500 (Central Dayl... | false | Sat Dec 13 2025 03:16:54 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:54 GMT-0600 (Central Stan... |
| 4 | UKSYQLNP | Debate laugh low everyone. Week itself type lay. | Wed Aug 21 2024 00:00:00 GMT-0500 (Central Dayl... | Fri Mar 01 2024 00:00:00 GMT-0600 (Central Stan... | Wed Sep 24 2025 00:00:00 GMT-0500 (Central Dayl... | Wed May 21 2025 00:00:00 GMT-0500 (Central Dayl... | true | Sat Dec 13 2025 03:16:54 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:54 GMT-0600 (Central Stan... |
| 5 | ZAGEOHZO | Brother occur learn it song program these. Sing... | Thu Oct 30 2025 00:00:00 GMT-0500 (Central Dayl... | Fri Feb 21 2025 00:00:00 GMT-0600 (Central Stan... | Mon Dec 08 2025 00:00:00 GMT-0600 (Central Stan... | Tue Oct 15 2024 00:00:00 GMT-0500 (Central Dayl... | true | Sat Dec 13 2025 03:16:54 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:16:54 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:50.206Z*