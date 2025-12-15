# medical_claims

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.medical_claims` table represents medical claims within a healthcare billing system, specifically tracking financial transactions tied to patient healthcare services. Each claim, identified by a unique `claim_id`, is associated with a patient and an insurance provider, including details such as service date, submission date, charges, and payment status, reflecting the claim lifecycle from submission to resolution. While it hints at relationships with entities like `patient_id` and `insurance_id`, further links to their respective tables are needed to fully integrate this table into the broader healthcare records system.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| claim_id | integer | NO | This column uniquely identifies each medical claim within the dataset. The values are sequential integers, suggesting they serve as identifiers rather than carrying inherent business meaning. |
| claim_number | character varying | YES | This column likely represents unique identifiers assigned to individual medical claims, facilitating tracking and reference in healthcare billing processes. Purpose unclear from available data if additional business logic or significance applies to these identifiers. |
| patient_id | integer | NO | This column uniquely identifies each patient within the medical claims records, differentiating individuals with distinct numerical identifiers. Purpose unclear from available data. |
| encounter_id | integer | YES | Purpose unclear from available data. |
| insurance_id | integer | YES | This column appears to represent unique identifiers assigned to different insurance policies or providers associated with medical claims. Purpose unclear from available data beyond associating claims with multiple policies or providers as indicated by numerical identifiers. |
| service_date | date | NO | This column represents the date on which a medical service was provided to a patient. The dates are recorded in Central Time, indicating when services occurred within this time zone. |
| submitted_date | date | YES | This column records the date when a medical claim was submitted, reflecting when the claim information was officially entered into the system. Purpose unclear from available data. |
| total_charges | numeric | YES | This column represents the monetary amount associated with individual medical claims. These values indicate the charges incurred during healthcare services, with varying amounts reflecting different levels of service or treatment complexity. |
| allowed_amount | numeric | YES | This column represents the monetary amount that is authorized for payment in a medical claim. The allowed amounts indicate the financial limit approved for coverage in each instance. |
| paid_amount | numeric | YES | This column likely represents the amounts paid in a series of financial transactions, possibly related to medical insurance claims. The values reflect monetary compensation or reimbursement amounts, but further context is needed to understand the specific nature of these payments. |
| patient_responsibility | numeric | YES | This column likely represents the monetary amount that a patient is required to pay out-of-pocket for a medical service or claim. Purpose unclear from available data. |
| status | character varying | YES | This column indicates the current state of a medical claim, categorizing it as either pending, active, or inactive. It helps track the processing status within the claim management workflow. |
| created_at | timestamp without time zone | YES | This column records the date and time a medical claim entry was created in the system. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a record in the medical claims table was last updated. Purpose unclear from available data as it lacks context or specific changes linked to the timestamps shown. |

## Primary Key

`claim_id`

## Foreign Keys

- `encounter_id` → `synthetic.encounters.encounter_id`
- `insurance_id` → `synthetic.insurance_policies.insurance_id`
- `patient_id` → `synthetic.patients.patient_id`

## Indexes

- `medical_claims_claim_number_key`: CREATE UNIQUE INDEX medical_claims_claim_number_key ON synthetic.medical_claims USING btree (claim_number)
- `medical_claims_pkey`: CREATE UNIQUE INDEX medical_claims_pkey ON synthetic.medical_claims USING btree (claim_id)

## Sample Data

| claim_id | claim_number | patient_id | encounter_id | insurance_id | service_date | submitted_date | total_charges | allowed_amount | paid_amount | patient_responsibility | status | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 087775190032260 | 29 | null | 30 | Sat Nov 23 2024 00:00:00 GMT-0600 (Central Stan... | Mon Jul 08 2024 00:00:00 GMT-0500 (Central Dayl... | 680.11 | 3451.70 | 8780.82 | 780.26 | pending | Sat Dec 13 2025 03:22:34 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:34 GMT-0600 (Central Stan... |
| 2 | 784326748464310 | 38 | null | 12 | Thu Jul 31 2025 00:00:00 GMT-0500 (Central Dayl... | Thu Dec 04 2025 00:00:00 GMT-0600 (Central Stan... | 767.78 | 1299.04 | 5033.61 | 868.21 | active | Sat Dec 13 2025 03:22:34 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:34 GMT-0600 (Central Stan... |
| 3 | 233854376730585 | 34 | null | 10 | Wed Jan 08 2025 00:00:00 GMT-0600 (Central Stan... | Tue Feb 06 2024 00:00:00 GMT-0600 (Central Stan... | 304.12 | 1628.05 | 9348.03 | 225.47 | pending | Sat Dec 13 2025 03:22:34 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:34 GMT-0600 (Central Stan... |
| 4 | 645996822431212 | 19 | null | 6 | Wed Aug 28 2024 00:00:00 GMT-0500 (Central Dayl... | Thu Nov 27 2025 00:00:00 GMT-0600 (Central Stan... | 250.61 | 6354.22 | 5512.91 | 125.17 | inactive | Sat Dec 13 2025 03:22:34 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:34 GMT-0600 (Central Stan... |
| 5 | 889839230781412 | 40 | null | 35 | Thu Oct 16 2025 00:00:00 GMT-0500 (Central Dayl... | Wed Jun 25 2025 00:00:00 GMT-0500 (Central Dayl... | 93.43 | 6413.46 | 5922.17 | 580.65 | active | Sat Dec 13 2025 03:22:34 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:34 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:43.472Z*