# payment_allocations

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.payment_allocations` table represents the allocation of payments to invoices within a financial system, tracking how payment amounts are distributed. It uniquely identifies each allocation with `allocation_id` and relates to other tables through foreign keys, likely associating payments and invoices via `payment_id` and `invoice_id`, although specific relationships are undefined. This table serves to record and manage the distribution of funds against invoices, with timestamps indicating when allocations were created and last updated.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| allocation_id | integer | NO | This column represents a unique identifier for individual payment allocation records in the system, ensuring each one is distinctly tracked. |
| payment_id | integer | NO | This column represents unique identifiers for individual payment allocations within the system. Each value distinguishes a specific payment allocation from others. |
| invoice_id | integer | NO | This column represents unique identifiers for invoices related to specific payment allocations, correlating payment records to their respective invoices. |
| amount | numeric | NO | This column represents the monetary amounts allocated for payments in financial transactions. The values reflect various payment sizes, suggesting diverse financial activities or expenditures. |
| created_at | timestamp without time zone | YES | The column records the date and time when a payment allocation was created. It captures this information by default at the moment of entry creation. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a payment allocation record was last modified or updated. The uniformity of sample values suggests that these actions could have been made simultaneously or in bulk. |

## Primary Key

`allocation_id`

## Foreign Keys

- `invoice_id` → `synthetic.invoices_payable.invoice_id`
- `payment_id` → `synthetic.vendor_payments.payment_id`

## Indexes

- `payment_allocations_pkey`: CREATE UNIQUE INDEX payment_allocations_pkey ON synthetic.payment_allocations USING btree (allocation_id)

## Sample Data

| allocation_id | payment_id | invoice_id | amount | created_at | updated_at |
| --- | --- | --- | --- | --- | --- |
| 1 | 30 | 94 | 551.17 | Sat Dec 13 2025 03:17:44 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:44 GMT-0600 (Central Stan... |
| 2 | 42 | 83 | 993.19 | Sat Dec 13 2025 03:17:44 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:44 GMT-0600 (Central Stan... |
| 3 | 26 | 94 | 3399.63 | Sat Dec 13 2025 03:17:44 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:44 GMT-0600 (Central Stan... |
| 4 | 7 | 32 | 1923.98 | Sat Dec 13 2025 03:17:44 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:44 GMT-0600 (Central Stan... |
| 5 | 35 | 58 | 1410.42 | Sat Dec 13 2025 03:17:44 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:44 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:14.494Z*