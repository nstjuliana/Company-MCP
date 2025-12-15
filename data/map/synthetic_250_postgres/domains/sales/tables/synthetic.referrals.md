# referrals

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.referrals` table represents a record of medical referrals, tracking information about referrals from one physician to another, including but not limited to the patient involved, the referral dates, reasons, urgency, and status. The `referral_id` serves as the primary key, with potential references to other tables through undefined foreign keys implying connections to patient and physician details. The table's role in the data model is to facilitate the management and historical tracking of referral interactions within a healthcare setting, evident from columns like `referral_date`, `reason`, and `status`.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| referral_id | integer | NO | This column represents the unique identifier assigned to each referral record in the database, ensuring each entry is distinct and can be individually referenced. Purpose unclear from available data. |
| patient_id | integer | NO | This column represents a unique identifier assigned to each patient within the referrals context. Based on the sample values, it serves to link or track patient-specific referral data. |
| referring_physician_id | integer | YES | This column likely represents the unique identifier associated with a physician who has referred a patient for a particular service or consultation. Purpose unclear from available data. |
| referred_to_physician_id | integer | YES | Purpose unclear from available data. |
| referral_date | date | NO | This column records the dates on which referrals occurred, indicating the specific days when referral actions were logged in the system. The dates suggest transactions were captured across various months and years. |
| reason | text | YES | The column records brief descriptive notes or statements related to the context or circumstances surrounding a referral. Purpose unclear from available data. |
| urgency | character varying | YES | Purpose unclear from available data. |
| status | character varying | YES | This column indicates the current state or progress of a referral, with potential stages being 'active', 'inactive', and 'pending'. It suggests the transition of a referral through different phases, likely relating to its completion or approval status. |
| authorization_number | character varying | YES | This column contains a unique identifier associated with each referral, likely used to track or authorize specific actions or processes. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when each referral record was initially created. The timestamp reflects the exact moment a new referral entry is added to the system, defaulting to the current system time upon creation. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a referral record was last modified, with each entry defaulting to the current timestamp upon any updates. Purpose unclear from available data beyond tracking modification times. |

## Primary Key

`referral_id`

## Foreign Keys

- `patient_id` → `synthetic.patients.patient_id`
- `referred_to_physician_id` → `synthetic.physicians.physician_id`
- `referring_physician_id` → `synthetic.physicians.physician_id`

## Indexes

- `referrals_pkey`: CREATE UNIQUE INDEX referrals_pkey ON synthetic.referrals USING btree (referral_id)

## Sample Data

| referral_id | patient_id | referring_physician_id | referred_to_physician_id | referral_date | reason | urgency | status | authorization_number | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 49 | null | null | Wed Jul 02 2025 00:00:00 GMT-0500 (Central Dayl... | Foot national raise there order effort. Picture... | Operation media difficult adult last know away. | inactive | 734996321553397 | Sat Dec 13 2025 03:22:44 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:44 GMT-0600 (Central Stan... |
| 2 | 47 | null | null | Wed Sep 03 2025 00:00:00 GMT-0500 (Central Dayl... | Big word capital worker stay. Beyond continue p... | Task base direction although and certainly. | pending | 842351802642149 | Sat Dec 13 2025 03:22:44 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:44 GMT-0600 (Central Stan... |
| 3 | 48 | null | null | Fri Mar 22 2024 00:00:00 GMT-0500 (Central Dayl... | Father hold discussion through everything exper... | Scientist let so spend test country. | inactive | 988268744337314 | Sat Dec 13 2025 03:22:44 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:44 GMT-0600 (Central Stan... |
| 4 | 30 | null | null | Mon Mar 17 2025 00:00:00 GMT-0500 (Central Dayl... | Participant dinner after nation. | Develop before break. | active | 216348443053447 | Sat Dec 13 2025 03:22:44 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:44 GMT-0600 (Central Stan... |
| 5 | 47 | null | null | Fri Nov 21 2025 00:00:00 GMT-0600 (Central Stan... | Society challenge director. Month mouth best ho... | Make social stand. | inactive | 638720323832270 | Sat Dec 13 2025 03:22:44 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:44 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:56.616Z*