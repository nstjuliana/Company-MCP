# job_applicants

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.job_applicants` table represents information about individuals applying for jobs, capturing their personal details and application information. Key columns include the primary key `applicant_id`, personal identifiers like `first_name`, `last_name`, and contact information such as `email` and `phone`, along with URLs for their `resume` and `linkedin` profiles, indicating a comprehensive record for each applicant. This table functions as a standalone entity in the data model, given it has no foreign key relationships, suggesting it centralizes applicant data without direct association to other tables.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| applicant_id | integer | NO | This column represents a unique identifier assigned to each person applying for a job, ensuring each applicant is distinctly recognized within the system. This sequential numbering aids in tracking and managing job applications effectively. |
| first_name | character varying | NO | This column represents the given names of individuals who have applied for a job. Each entry corresponds to the first name of a job applicant in the database. |
| last_name | character varying | NO | This column represents the family surnames of individuals applying for jobs. The values are commonly recognized last names. |
| email | character varying | NO | This column represents the email addresses of individuals applying for job positions. Each entry is a unique contact detail for communication with a job applicant. |
| phone | character varying | YES | This column contains contact phone numbers for job applicants. The numbers are presented in various formats, including international dialing codes and extensions. |
| resume_url | character varying | YES | This column stores the web addresses where job applicants have uploaded their resumes. Each URL provided gives access to an applicant's resume hosted on a personal or business website. |
| linkedin_url | character varying | YES | This column contains URLs that appear to represent personal or business websites for job applicants, rather than containing direct links to LinkedIn profiles. Purpose unclear from available data. |
| source | character varying | YES | Purpose unclear from available data. The sample values appear to be nonsensical and do not provide clear insight into the business meaning of this column. |
| created_at | timestamp without time zone | YES | This column records the date and time when an application was created in the system. Purpose unclear from available data as it lacks a detailed description or variety in sample values. |
| updated_at | timestamp without time zone | YES | This column indicates the most recent date and time when a record for a job applicant was updated. It is useful for tracking changes or modifications made to applicant data. |

## Primary Key

`applicant_id`

## Indexes

- `job_applicants_pkey`: CREATE UNIQUE INDEX job_applicants_pkey ON synthetic.job_applicants USING btree (applicant_id)

## Sample Data

| applicant_id | first_name | last_name | email | phone | resume_url | linkedin_url | source | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Rose | Crosby | gerald25@example.com | 001-978-271-8882x237 | https://hughes.biz/ | http://www.cummings.com/ | Outside win why hot send foot into. Perhaps not... | Sat Dec 13 2025 02:54:06 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:06 GMT-0600 (Central Stan... |
| 2 | Richard | Ramirez | hwade@example.com | 855-975-1247x64000 | https://foley.com/ | https://scott-rodriguez.com/ | Employee show open line fast. Soon street cut i... | Sat Dec 13 2025 02:54:06 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:06 GMT-0600 (Central Stan... |
| 3 | Brandon | Carr | anthonyfranklin@example.com | 001-913-449-0961x979 | https://peters.com/ | https://nelson.com/ | Government show seem man write. Of marriage pol... | Sat Dec 13 2025 02:54:06 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:06 GMT-0600 (Central Stan... |
| 4 | James | Collins | perezanna@example.com | +1-877-648-6759x5141 | http://www.mason.com/ | https://robertson.biz/ | Position detail wife investment say. Reveal hea... | Sat Dec 13 2025 02:54:06 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:06 GMT-0600 (Central Stan... |
| 5 | Kathy | Harrison | kenneththomas@example.com | (459)946-9890x623 | http://www.wells.org/ | http://www.perez.org/ | Remain someone without. Station their research ... | Sat Dec 13 2025 02:54:06 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:06 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:04.413Z*