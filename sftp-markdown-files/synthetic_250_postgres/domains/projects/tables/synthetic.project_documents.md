# project_documents

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.project_documents` table represents project-related documents within an undefined business entity, capturing details such as document names, types, versions, and file paths. The table is linked to projects via the `project_id` foreign key, suggesting it serves as a repository for documents associated with specific projects, with information on who uploaded them and when. Its role in the data model appears to be maintaining a record of various document attributes related to projects, which can be identified by the primary key `document_id`.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| document_id | integer | NO | This column uniquely identifies each document associated with a project. It ensures that each document can be distinctly referenced within the project documentation system. |
| project_id | integer | NO | This column likely represents a unique identifier associated with a specific project within a dataset of project documents. Its purpose is to link documents to their respective projects, as indicated by distinct numeric values. |
| document_name | character varying | NO | This column likely contains summaries or titles of various documents related to project activities or reports, reflecting a broad range of topics and subjects. Purpose unclear from available data. |
| document_type | character varying | YES | The column appears to contain short, narrative-like entries that may represent abstract descriptions or categorizations related to projects, as indicated by varied sample phrases encompassing actions, entities, and general scenarios. The intended purpose or context of these entries is unclear from the available data. |
| file_path | character varying | YES | Purpose unclear from available data. The sample values appear to be fragmented text excerpts, making it difficult to determine the specific nature of the information stored. |
| version | character varying | YES | Purpose unclear from available data. |
| uploaded_by | integer | YES | This column identifies the user who uploaded a document, represented by their unique identifier. Purpose unclear from available data. |
| upload_date | timestamp without time zone | YES | This column indicates the date and time when a document related to a project was uploaded. It reflects the submissions occurring across various months and years, primarily during Central daylight and standard time. |
| description | text | YES | This column contains textual summaries or abstracts related to various subjects, possibly detailing project-related narratives or concepts. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a project document was created, reflecting the moment of entry or generation in the system. The exact purpose of capturing this timestamp is unclear from the available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a document within a project was last modified. It helps in tracking the most recent updates to project-related documents. |

## Primary Key

`document_id`

## Foreign Keys

- `project_id` → `synthetic.pm_projects.project_id`

## Indexes

- `project_documents_pkey`: CREATE UNIQUE INDEX project_documents_pkey ON synthetic.project_documents USING btree (document_id)

## Sample Data

| document_id | project_id | document_name | document_type | file_path | version | uploaded_by | upload_date | description | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 22 | 77 | Provide decide range hotel industry. Perform pr... | Fly care somebody image. Person hotel east. | Base leave to our action may. Wind ready whom a... | Center away its ago. | 47 | Wed Sep 17 2025 07:57:11 GMT-0500 (Central Dayl... | Try themselves particularly country. Scientist ... | Sat Dec 13 2025 03:13:09 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:13:09 GMT-0600 (Central Stan... |
| 21 | 74 | Tonight inside moment social catch push. None r... | Animal mouth candidate tend success ever. | Run score cause common these. Might specific Mr... | Hotel common energy. | 321 | Sat Feb 15 2025 08:32:07 GMT-0600 (Central Stan... | Them writer occur among. Resource hundred thoug... | Sat Dec 13 2025 03:13:09 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:13:09 GMT-0600 (Central Stan... |
| 23 | 87 | Score if against especially talk. Mean citizen ... | Avoid cost my. | High trial indicate structure consider allow. A... | Speech may science. | 885 | Tue May 28 2024 07:36:39 GMT-0500 (Central Dayl... | Face among speech too staff across. There thank... | Sat Dec 13 2025 03:13:09 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:13:09 GMT-0600 (Central Stan... |
| 24 | 65 | Talk worker around across also onto success. Ar... | Computer example cause great put hand. | Win company report teacher. Near current catch ... | Film door station. | 760 | Sun Nov 09 2025 10:31:25 GMT-0600 (Central Stan... | Political owner road scene learn and. Action ev... | Sat Dec 13 2025 03:13:09 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:13:09 GMT-0600 (Central Stan... |
| 25 | 60 | Me speech he. Daughter simple matter avoid. Wha... | Less travel respond official black. | Series interest right cost boy relate talk. Emp... | Society include. | 17 | Wed Aug 06 2025 19:47:05 GMT-0500 (Central Dayl... | Network instead stuff next single federal. Indu... | Sat Dec 13 2025 03:13:09 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:13:09 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:42:10.935Z*