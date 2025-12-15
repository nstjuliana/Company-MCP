# PATIENTS

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.PATIENTS table represents a business entity of patient records, capturing information such as first name, last name, date of birth, insurance identification, and several anonymized attributes related to prescriptions, billing, and records. With PATIENT_ID as the primary key and no indicated foreign key dependencies, the table functions as an isolated entity within the data model, primarily focusing on storing synthetic patient demographic and administrative data. This table encapsulates critical patient information but lacks direct relational ties to other tables, as evidenced by the sample data.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| PATIENT_ID | NUMBER | NO | This column uniquely identifies each entry in the patients table, serving as a sequential identifier for individuals in the dataset. |
| FIRST_NAME | TEXT | NO | This column contains given names of patients, representing the first part of a person's full name used for identification. These names are essential personal identifiers within the patient dataset. |
| LAST_NAME | TEXT | NO | This column represents the last names of individuals within the synthetic patient records. It is used to identify or refer to patients in the dataset. |
| DATE_OF_BIRTH | DATE | YES | This column represents the recorded dates of birth for individuals within the patient dataset. The values indicate specific birth dates associated with each patient entry, though some entries may not have this information available. |
| INSURANCE_ID | TEXT | YES | This column represents unique identifiers relating to insurance coverage associated with patients, which can be selectively recorded for some entries. Purpose unclear from available data. |
| PRESCRIPTION_206_ATTR_0 | TEXT | NO | Purpose unclear from available data. The sample values do not provide sufficient information to determine the column's business meaning. |
| BILLING_206_ATTR_1 | BOOLEAN | YES | This column indicates whether a specific billing-related attribute is present for the patient. Purpose unclear from available data. |
| RECORD_206_ATTR_2 | NUMBER | NO | This column represents a sequential identifier or code, potentially used to uniquely identify or categorize patient records. Each value is a distinct, non-null number starting from 100. |
| RECORD_206_ATTR_3 | TEXT | YES | Purpose unclear from available data. |
| PATIENT_206_ATTR_4 | TEXT | YES | Purpose unclear from available data. |

## Primary Key

`PATIENT_ID`

## Sample Data

| PATIENT_ID | FIRST_NAME | LAST_NAME | DATE_OF_BIRTH | INSURANCE_ID | PRESCRIPTION_206_ATTR_0 | BILLING_206_ATTR_1 | RECORD_206_ATTR_2 | RECORD_206_ATTR_3 | PATIENT_206_ATTR_4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Sample FIRST_NAME 1 | Sample LAST_NAME 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | 1 | Sample PRESCRIPTION_206_ATTR_0 1 | true | 100 | Sample RECORD_206_ATTR_3 1 | Sample PATIENT_206_ATTR_4 1 |
| 2 | Sample FIRST_NAME 2 | Sample LAST_NAME 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | 2 | Sample PRESCRIPTION_206_ATTR_0 2 | false | 101 | Sample RECORD_206_ATTR_3 2 | Sample PATIENT_206_ATTR_4 2 |
| 3 | Sample FIRST_NAME 3 | Sample LAST_NAME 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | 3 | Sample PRESCRIPTION_206_ATTR_0 3 | true | 102 | Sample RECORD_206_ATTR_3 3 | Sample PATIENT_206_ATTR_4 3 |
| 4 | Sample FIRST_NAME 4 | Sample LAST_NAME 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | 4 | Sample PRESCRIPTION_206_ATTR_0 4 | false | 103 | Sample RECORD_206_ATTR_3 4 | Sample PATIENT_206_ATTR_4 4 |
| 5 | Sample FIRST_NAME 5 | Sample LAST_NAME 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | 5 | Sample PRESCRIPTION_206_ATTR_0 5 | true | 104 | Sample RECORD_206_ATTR_3 5 | Sample PATIENT_206_ATTR_4 5 |

*Generated at: 2025-12-14T23:43:02.902Z*