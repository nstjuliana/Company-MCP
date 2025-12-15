# patient_consents

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.patient_consents" table represents the consents given by patients within a healthcare context, capturing details such as consent type, dates, granting authority, and current status. Each record is uniquely identified by "consent_id" and associates with patients via the "patient_id" column, although no direct foreign key is specified. The table's role in the data model is to track and manage the consents provided by patients concerning their healthcare decisions or interactions.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| consent_id | integer | NO | This column represents a unique identifier for each patient consent record. It ensures that each consent entry is distinct and sequentially ordered within the dataset. |
| patient_id | integer | NO | This column likely represents a unique identifier assigned to each patient in the consent records. It ensures each patient's consent information is tracked individually and facilitates linking consents to specific patients. |
| consent_type | character varying | NO | Purpose unclear from available data. |
| consent_date | date | NO | This column represents the specific date on which patients provided their consent, presumably for participation in a study or receiving treatment, as seen in the list of example dates. The dates align with various seasons, suggesting that consent is gathered through the year. |
| expiration_date | date | YES | This column represents the date until which a patient's consent is valid. Purpose is unclear from available data beyond indicating expiration. |
| granted_by | character varying | YES | Purpose unclear from available data. |
| status | character varying | YES | This column indicates the current state of a patient's consent process, which can be 'active', 'inactive', or 'pending'. These states likely denote whether consent has been given, revoked, or is under consideration, respectively. |
| document_url | character varying | YES | This column contains URLs linking to digital documents related to patient consents. These URLs direct to various websites, indicating external locations where consent documentation is stored or managed. |
| created_at | timestamp without time zone | YES | This field records the date and time when a specific patient consent was created. The timestamp reflects when the entry was initially recorded in the system. |
| updated_at | timestamp without time zone | YES | Indicates the most recent date and time when the consent information of a patient was updated. Each timestamp reflects the moment changes were saved, helping track updates over time. |

## Primary Key

`consent_id`

## Foreign Keys

- `patient_id` → `synthetic.patients.patient_id`

## Indexes

- `patient_consents_pkey`: CREATE UNIQUE INDEX patient_consents_pkey ON synthetic.patient_consents USING btree (consent_id)

## Sample Data

| consent_id | patient_id | consent_type | consent_date | expiration_date | granted_by | status | document_url | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 33 | Hold open range just take drug prevent he. Seni... | Wed Oct 23 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Apr 06 2024 00:00:00 GMT-0500 (Central Dayl... | Hair attorney job identify herself stuff southe... | inactive | https://www.murphy.biz/ | Sat Dec 13 2025 03:23:01 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:23:01 GMT-0600 (Central Stan... |
| 2 | 27 | Pretty term by talk pull party record. Heavy wh... | Mon Jun 03 2024 00:00:00 GMT-0500 (Central Dayl... | Thu Sep 12 2024 00:00:00 GMT-0500 (Central Dayl... | Human follow into nation while own specific. St... | pending | https://www.steele-strickland.net/ | Sat Dec 13 2025 03:23:01 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:23:01 GMT-0600 (Central Stan... |
| 3 | 9 | Listen kid information street. Matter similar g... | Sat Mar 09 2024 00:00:00 GMT-0600 (Central Stan... | Tue Feb 25 2025 00:00:00 GMT-0600 (Central Stan... | Always six law speech fill be instead. Charge e... | pending | https://www.campbell.com/ | Sat Dec 13 2025 03:23:01 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:23:01 GMT-0600 (Central Stan... |
| 4 | 25 | Total magazine tax top write certain. More nice... | Fri Dec 13 2024 00:00:00 GMT-0600 (Central Stan... | Thu Sep 25 2025 00:00:00 GMT-0500 (Central Dayl... | Game card probably foot better. | inactive | https://howard.com/ | Sat Dec 13 2025 03:23:01 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:23:01 GMT-0600 (Central Stan... |
| 5 | 12 | Pick letter who cold task all. Now decide newsp... | Mon May 12 2025 00:00:00 GMT-0500 (Central Dayl... | Wed Jan 03 2024 00:00:00 GMT-0600 (Central Stan... | Expect from member guy number task sister. Whos... | inactive | http://brown-foley.info/ | Sat Dec 13 2025 03:23:01 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:23:01 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:47.586Z*