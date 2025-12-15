# claim_lines

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.claim_lines` table represents individual line items within an insurance claim, capturing details about medical procedures associated with a particular claim. Each entry is uniquely identified by `claim_line_id`, and contains information such as `procedure_code`, `modifier`, `units`, and financial details (`charge_amount` and `allowed_amount`). The table serves as a child to the claims table, as indicated by the `claim_id` foreign key relationship, which it references.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| claim_line_id | integer | NO | This column represents a unique identifier for individual entries within the claim lines table, ensuring each entry has a distinct reference number. |
| claim_id | integer | NO | Each value uniquely identifies a specific claim within the claim lines dataset, serving as a reference to group related claim details. |
| procedure_code | character varying | YES | This column appears to represent coded information, likely related to procedures, for each claim line entry. The exact purpose of the codes is unclear from the available data. |
| modifier | character varying | YES | Purpose unclear from available data. |
| diagnosis_pointer | character varying | YES | Purpose unclear from available data. |
| units | integer | YES | This column likely represents the number of units involved or affected in each claim line within the claims processing system. The default value suggests that if unspecified, the transaction is assumed to involve a minimum single unit. |
| charge_amount | numeric | YES | This column represents the monetary amounts charged for individual claim lines, which can vary significantly in value. Purpose unclear from available data. |
| allowed_amount | numeric | YES | This column likely represents the monetary amount that is permitted or authorized for payment on an individual claim line within the claims data. The values suggest different financial limits applied to various claims. |
| created_at | timestamp without time zone | YES | This column records the date and time when each claim line entry was created, providing a historical reference for when the data was initially logged. It captures timestamps in the Central Standard Time zone. |
| updated_at | timestamp without time zone | YES | This column captures the most recent date and time when a change was made to a claim line entry. It automatically records the current timestamp by default, indicating when entries were last updated. |

## Primary Key

`claim_line_id`

## Foreign Keys

- `claim_id` → `synthetic.medical_claims.claim_id`

## Indexes

- `claim_lines_pkey`: CREATE UNIQUE INDEX claim_lines_pkey ON synthetic.claim_lines USING btree (claim_line_id)

## Sample Data

| claim_line_id | claim_id | procedure_code | modifier | diagnosis_pointer | units | charge_amount | allowed_amount | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 20 | YVTNKZMK | Sense voice answer. | Take bar where name. | 597 | 7231.60 | 124.24 | Sat Dec 13 2025 03:22:37 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:37 GMT-0600 (Central Stan... |
| 2 | 42 | MJQBJLFP | Book one pass raise. | Alone form already. | 369 | 6930.76 | 630.62 | Sat Dec 13 2025 03:22:37 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:37 GMT-0600 (Central Stan... |
| 3 | 8 | TYGOFEPS | Believe writer. | Way seat establish. | 477 | 3075.00 | 4060.11 | Sat Dec 13 2025 03:22:37 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:37 GMT-0600 (Central Stan... |
| 4 | 33 | FRAWXTUF | Sure cover end. | Design world grow. | 946 | 8952.23 | 7038.53 | Sat Dec 13 2025 03:22:37 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:37 GMT-0600 (Central Stan... |
| 5 | 20 | LEAYWTVN | Begin happy reality. | Into daughter agent. | 707 | 1182.98 | 9162.14 | Sat Dec 13 2025 03:22:37 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:22:37 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:37.901Z*