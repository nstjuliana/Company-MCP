# medical_history

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.medical_history` table represents the medical history records of patients, capturing details such as medical conditions, corresponding ICD-10 codes, and the status of the condition. It primarily links to a `patient_id`, implying a relationship to a patients' table for individual patient information. While it doesn't explicitly reference other tables, it serves a critical role in the data model by documenting the timeline and details of medical conditions pertinent to patient care.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| history_id | integer | NO | This column assigns a unique identifier to each record in the medical history table, ensuring each history entry can be distinctly referenced. The sequence of numbers suggests an ordered list typically used for record tracking. |
| patient_id | integer | NO | This column identifies each patient with a unique numerical identifier within the medical history dataset. It is a necessary reference point for associating medical records with individual patients. |
| condition | character varying | NO | Purpose unclear from available data. The sample values appear unrelated to health conditions or medical history. |
| icd10_code | character varying | YES | Purpose unclear from available data. |
| onset_date | date | YES | Represents the date when a medical condition or event began for a patient. This data is used to track the timeline and development of medical conditions over time. |
| resolution_date | date | YES | This column likely records the date when a particular medical issue was resolved for a patient. It can remain empty if the resolution date is not yet determined. |
| status | character varying | YES | This column indicates the current state of an individual's medical record, which can be either 'active', 'inactive', or 'pending'. It serves to track whether medical histories are currently being maintained and updated, are no longer in use, or are awaiting further updates or verification. |
| notes | text | YES | This column contains narrative descriptions or commentary related to individuals' social or personal histories, activities, or other general observations, potentially relevant to their medical context. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time an entry in the medical history table was created. The purpose is to track when a medical record was first logged. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a medical record entry was last updated. Purpose unclear from available data. |

## Primary Key

`history_id`

## Foreign Keys

- `patient_id` → `synthetic.patients.patient_id`

## Indexes

- `medical_history_pkey`: CREATE UNIQUE INDEX medical_history_pkey ON synthetic.medical_history USING btree (history_id)

## Sample Data

| history_id | patient_id | condition | icd10_code | onset_date | resolution_date | status | notes | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 11 | Development chair tonight skin. | YIPNCLQD | Wed Feb 05 2025 00:00:00 GMT-0600 (Central Stan... | Thu Oct 09 2025 00:00:00 GMT-0500 (Central Dayl... | active | We money risk culture social history. Foot choo... | Sat Dec 13 2025 03:22:47 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:47 GMT-0600 (Central Stan... |
| 2 | 32 | Dog young computer easy. Word training plant. S... | QPXPUWVQ | Sat Oct 19 2024 00:00:00 GMT-0500 (Central Dayl... | Wed Apr 10 2024 00:00:00 GMT-0500 (Central Dayl... | inactive | This feel several identify along particularly f... | Sat Dec 13 2025 03:22:47 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:47 GMT-0600 (Central Stan... |
| 3 | 42 | Big benefit skill he stay father. Financial mee... | FWSUILNB | Tue Sep 16 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 30 2023 00:00:00 GMT-0600 (Central Stan... | inactive | Agent involve order special color better. Learn... | Sat Dec 13 2025 03:22:47 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:47 GMT-0600 (Central Stan... |
| 4 | 37 | Cost military case who. Pull natural growth lay. | KUIUPZUU | Thu Mar 20 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Mar 08 2025 00:00:00 GMT-0600 (Central Stan... | active | Fire black factor inside. Eye natural camera. D... | Sat Dec 13 2025 03:22:47 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:47 GMT-0600 (Central Stan... |
| 5 | 34 | Surface practice up fear scene guy.
Term high c... | MYWPECQE | Mon Oct 07 2024 00:00:00 GMT-0500 (Central Dayl... | Fri Dec 13 2024 00:00:00 GMT-0600 (Central Stan... | active | Need water how dog fine green station down. You... | Sat Dec 13 2025 03:22:47 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:47 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:38.360Z*