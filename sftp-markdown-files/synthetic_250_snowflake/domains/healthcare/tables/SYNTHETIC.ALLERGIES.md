# ALLERGIES

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.ALLERGIES table represents allergy records within the synthetic_250_snowflake database, capturing details such as allergy names, descriptions, and relevant medical attributes for patient care. Each entry is uniquely identified by the primary key, ALLERGIE_ID, and contains various attributes including appointment and prescription information, suggesting its role in tracking allergy-related healthcare interactions. This table operates independently with no direct foreign key connections to other tables, signifying its role as a standalone record-keeping entity within the data model.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| ALLERGIE_ID | NUMBER | NO | This column uniquely identifies individual allergy records within the dataset, ensuring each allergy entry is distinct and can be referenced separately. |
| NAME | TEXT | NO | This column enumerates various types of allergies identified in a synthetic dataset. Each entry represents a unique allergy with a sequential numeric designation. |
| DESCRIPTION | TEXT | YES | This column provides textual descriptions of different allergies identified within the table, offering detailed information or labels for each allergy entry. Each description follows a sequential naming pattern, indicating distinct allergy descriptions. |
| RECORD_217_ATTR_0 | NUMBER | NO | This column appears to represent a sequential identifier or code unique to each allergy record in the dataset. The purpose behind assigning these specific numerical values to the records is unclear from the available data. |
| BILLING_217_ATTR_1 | NUMBER | NO | Purpose unclear from available data. |
| APPOINTMENT_217_ATTR_2 | TEXT | NO | Purpose unclear from available data. |
| PATIENT_217_ATTR_3 | BOOLEAN | YES | Purpose unclear from available data. |
| RECORD_217_ATTR_4 | TEXT | YES | Purpose unclear from available data. |
| PRESCRIPTION_217_ATTR_5 | DATE | YES | This column likely represents a scheduled date associated with specific prescriptions, possibly indicating when a prescription was prescribed, dispensed, or needs to be refilled. The purpose is unclear beyond representing a date related to prescriptions. |
| VERSION | NUMBER | NO | This column represents the sequential versioning or iteration identifier for entries in the allergies table. It starts at 1 by default and increments with each new version, ensuring precise tracking of updates or changes. |

## Primary Key

`ALLERGIE_ID`

## Sample Data

| ALLERGIE_ID | NAME | DESCRIPTION | RECORD_217_ATTR_0 | BILLING_217_ATTR_1 | APPOINTMENT_217_ATTR_2 | PATIENT_217_ATTR_3 | RECORD_217_ATTR_4 | PRESCRIPTION_217_ATTR_5 | VERSION |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ALLERGIES 1 | Description for ALLERGIES 1 | 100 | 100 | Sample APPOINTMENT_217_ATTR_2 1 | true | Sample RECORD_217_ATTR_4 1 | Thu Dec 11 2025 18:00:00 GMT-0600 (Central Stan... | 100 |
| 2 | ALLERGIES 2 | Description for ALLERGIES 2 | 101 | 101 | Sample APPOINTMENT_217_ATTR_2 2 | false | Sample RECORD_217_ATTR_4 2 | Fri Dec 12 2025 18:00:00 GMT-0600 (Central Stan... | 101 |
| 3 | ALLERGIES 3 | Description for ALLERGIES 3 | 102 | 102 | Sample APPOINTMENT_217_ATTR_2 3 | true | Sample RECORD_217_ATTR_4 3 | Sat Dec 13 2025 18:00:00 GMT-0600 (Central Stan... | 102 |
| 4 | ALLERGIES 4 | Description for ALLERGIES 4 | 103 | 103 | Sample APPOINTMENT_217_ATTR_2 4 | false | Sample RECORD_217_ATTR_4 4 | Sun Dec 14 2025 18:00:00 GMT-0600 (Central Stan... | 103 |
| 5 | ALLERGIES 5 | Description for ALLERGIES 5 | 104 | 104 | Sample APPOINTMENT_217_ATTR_2 5 | true | Sample RECORD_217_ATTR_4 5 | Mon Dec 15 2025 18:00:00 GMT-0600 (Central Stan... | 104 |

*Generated at: 2025-12-14T23:43:02.834Z*