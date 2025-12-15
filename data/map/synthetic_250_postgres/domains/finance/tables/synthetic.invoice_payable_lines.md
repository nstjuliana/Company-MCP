# invoice_payable_lines

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.invoice_payable_lines` table represents individual line items associated with invoices, detailing the payable amounts for goods or services acquired. Each line, uniquely identified by `line_id`, is linked to an invoice through `invoice_id`, capturing details such as quantity, unit price, and total amount, thereby playing a critical role in the financial accounting of payable operations. The table records transactional and descriptive details, like `description` and `cost_center`, aiding in financial tracking and reporting, although its foreign key relationships to other tables remain undefined.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| line_id | integer | NO | This column assigns a unique identifier to each record in the invoice payable lines table, ensuring each entry can be distinctively referenced. |
| invoice_id | integer | NO | This column uniquely identifies invoices within the payable lines, indicating references to specific transactions or billing instances. Purpose unclear from available data. |
| account_id | integer | YES | This column likely represents identifiers for financial accounts associated with payable line items on invoices. The purpose of these identifiers in relation to specific financial processes is unclear from the available data. |
| description | character varying | YES | This column contains textual notes or remarks related to invoice payable lines, capturing various abstract, narrative details that may pertain to business transactions or contextual information. Purpose unclear from available data. |
| quantity | numeric | YES | This column likely represents the amount or volume of a particular payable item involved in a transaction or order. Provision of non-integer values suggests these items can be quantified in fractional units, such as weights or dimensions. |
| unit_price | numeric | YES | This column represents the price per unit in a set of payable invoices. It records the monetary value associated with each unit, reflecting varying amounts typical of financial transaction data. |
| amount | numeric | NO | This column represents monetary amounts related to invoice transactions that need to be paid. It reflects the payable amounts within financial documents, potentially representing costs or charges. |
| cost_center | character varying | YES | Purpose unclear from available data. The sample values appear as nonsensical phrases, making it difficult to derive a concrete business meaning. |
| created_at | timestamp without time zone | YES | This column records the date and time when a record in the invoice payable lines table was created, capturing the exact moment of entry creation. Its value defaults to the current timestamp, indicating it is typically automatically generated upon record insertion. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a record in the 'invoice_payable_lines' table was last updated. The purpose is to track changes or modifications made to these records over time. |

## Primary Key

`line_id`

## Foreign Keys

- `account_id` → `synthetic.chart_of_accounts.account_id`
- `invoice_id` → `synthetic.invoices_payable.invoice_id`

## Indexes

- `invoice_payable_lines_pkey`: CREATE UNIQUE INDEX invoice_payable_lines_pkey ON synthetic.invoice_payable_lines USING btree (line_id)

## Sample Data

| line_id | invoice_id | account_id | description | quantity | unit_price | amount | cost_center | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 22 | 6 | At try debate fact customer apply. Far decade b... | 582.74 | 14228.7000 | 35047.10 | Police not themselves fact usually whole. | Sat Dec 13 2025 02:54:32 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:32 GMT-0600 (Central Stan... |
| 2 | 42 | 45 | Whatever region trouble. Book rest charge wish ... | 662.14 | 12982.2700 | 70912.52 | Sort upon child thank truth news thought. | Sat Dec 13 2025 02:54:32 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:32 GMT-0600 (Central Stan... |
| 3 | 6 | 20 | Site institution establish as attorney. Give tr... | 558.92 | 64384.9800 | 32914.81 | Arm audience plant performance. | Sat Dec 13 2025 02:54:32 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:32 GMT-0600 (Central Stan... |
| 4 | 9 | 43 | Catch time past past dog week site. Agency sure... | 702.83 | 94716.1500 | 99716.69 | Realize office hospital past. | Sat Dec 13 2025 02:54:32 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:32 GMT-0600 (Central Stan... |
| 5 | 34 | 6 | Available quite born. Question few final suppor... | 646.02 | 42398.3000 | 36246.63 | Even hand sometimes statement near wife add. | Sat Dec 13 2025 02:54:32 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:32 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:13.432Z*