# vital_signs

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The synthetic.vital_signs table depicts patient vital sign measurements with each row representing a set of recorded vitals for a patient, denoted by a unique vital_id. This table is pivotal for capturing vital statistics such as temperature, blood pressure, heart rate, and more, likely linked to patient entities via patient_id and encounter_id, though specific relationships are unclear. It plays a critical role in storing clinical measurements necessary for patient monitoring and assessment, maintaining records enhanced by timestamped entries for creation and updates.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| vital_id | integer | NO | This column represents a unique identifier for each record in the vital signs table, ensuring that each entry is distinguishable from others. The sequential integer values suggest it serves as a primary key for organizing data entries. |
| patient_id | integer | NO | This column represents a unique identifier for patients. Each value corresponds to a specific individual within the database, ensuring that vital sign records are associated with the correct patient. |
| encounter_id | integer | YES | This column likely identifies a specific interaction or visit between a patient and healthcare provider within the record of vital signs. Purpose unclear from available data. |
| recorded_at | timestamp without time zone | NO | This column records the date and time when vital signs data is captured. It ensures accurate tracking of when each measurement is taken, though the specific significance of the timestamp to the business process is unclear from the available data. |
| temperature_f | numeric | YES | The column appears to represent some form of measurement typically captured in Fahrenheit, but the sample values indicate it may be stored in an unconventional scale or context. Purpose unclear from available data. |
| blood_pressure_systolic | integer | YES | Purpose unclear from available data as sample values greatly exceed typical human systolic blood pressure ranges. |
| blood_pressure_diastolic | integer | YES | This column represents recorded measurements of diastolic blood pressure, but the values seem unusually high, suggesting the data might not represent typical physiological ranges. Purpose unclear from available data. |
| heart_rate | integer | YES | This column might represent a numerical identifier or event count related to vital signs rather than a traditional heart rate, given the atypically high values observed. Purpose unclear from available data. |
| respiratory_rate | integer | YES | Purpose unclear from available data. |
| oxygen_saturation | numeric | YES | This column records some measure related to oxygen saturation levels; however, the unusually high sample values suggest they may not represent standard physiological percentages. Purpose unclear from available data. |
| weight_kg | numeric | YES | This column represents the weight of individuals measured in kilograms. The values appear to range widely, suggesting inclusion of data from a diverse population or varied entities. |
| height_cm | numeric | YES | This column appears to represent unusually large numerical values that could indicate a data entry or scaling error, as these figures do not correspond to typical human heights when measured in centimeters. Purpose unclear from available data. |
| bmi | numeric | YES | The column represents a measured value related to an individual's biometrics or health data, with unusually high values suggesting these are not standard Body Mass Index measurements. Purpose unclear from available data. |
| recorded_by | integer | YES | This column likely references unique identifiers for individuals who have recorded the vital signs, such as healthcare professionals or data entry personnel. The purpose of these identifiers is unclear from the available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a vital sign entry was created, capturing the moment of data entry or generation. It reflects the initial logging time rather than any subsequent updates. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a record in the vital signs table was last updated. Its purpose is unclear from the available data. |

## Primary Key

`vital_id`

## Foreign Keys

- `encounter_id` → `synthetic.encounters.encounter_id`
- `patient_id` → `synthetic.patients.patient_id`

## Indexes

- `vital_signs_pkey`: CREATE UNIQUE INDEX vital_signs_pkey ON synthetic.vital_signs USING btree (vital_id)

## Sample Data

| vital_id | patient_id | encounter_id | recorded_at | temperature_f | blood_pressure_systolic | blood_pressure_diastolic | heart_rate | respiratory_rate | oxygen_saturation | weight_kg | height_cm | bmi | recorded_by | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 42 | null | Mon Oct 07 2024 01:57:25 GMT-0500 (Central Dayl... | 358.67 | 408 | 283 | 195 | 992 | 122.16 | 848.03 | 454.7 | 662.77 | 658 | Sat Dec 13 2025 03:22:23 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:23 GMT-0600 (Central Stan... |
| 2 | 41 | null | Thu Jun 20 2024 19:10:09 GMT-0500 (Central Dayl... | 597.15 | 22 | 52 | 806 | 342 | 243.57 | 125.92 | 564.6 | 68.61 | 784 | Sat Dec 13 2025 03:22:23 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:23 GMT-0600 (Central Stan... |
| 3 | 36 | null | Wed Jul 30 2025 17:45:03 GMT-0500 (Central Dayl... | 207.16 | 222 | 833 | 891 | 239 | 328.56 | 147.55 | 900.5 | 2.84 | 880 | Sat Dec 13 2025 03:22:23 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:23 GMT-0600 (Central Stan... |
| 4 | 10 | null | Sun Nov 16 2025 13:07:36 GMT-0600 (Central Stan... | 987.53 | 554 | 257 | 818 | 179 | 109.93 | 866.45 | 131.8 | 358.24 | 808 | Sat Dec 13 2025 03:22:23 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:23 GMT-0600 (Central Stan... |
| 5 | 16 | null | Sat Dec 16 2023 18:05:38 GMT-0600 (Central Stan... | 588.85 | 17 | 179 | 272 | 54 | 126.76 | 420.96 | 113.7 | 63.56 | 460 | Sat Dec 13 2025 03:22:23 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:23 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:32.724Z*