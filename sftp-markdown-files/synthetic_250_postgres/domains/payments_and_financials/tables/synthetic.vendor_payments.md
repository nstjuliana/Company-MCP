# vendor_payments

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.vendor_payments` table represents a system for tracking payments made to vendors, with each entry uniquely identified by the `payment_id` as the primary key. The table stores information such as the payment number, vendor ID, payment date, method, total amount, currency, and associated bank account, indicating its function in recording transactional data related to vendor payments. Although it currently lacks defined foreign key relationships to other tables, it likely interfaces with a vendor or bank account table, given the presence of `vendor_id` and `bank_account_id` fields.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| payment_id | integer | NO | This column uniquely identifies each vendor payment transaction in the sequence they occur. Each value represents a distinct payment entry. |
| payment_number | character varying | YES | This column uniquely identifies individual payment transactions related to vendor operations, acting as a distinctive transaction reference number. Purpose unclear from available data. |
| vendor_id | integer | NO | This column represents unique identifiers for vendors involved in payment transactions. Each number corresponds to a different vendor in the context of the payments system. |
| payment_date | date | NO | This column represents the specific dates on which vendor payments were scheduled or occurred. The dates are related to transactions processed, typically involving business payments to vendors. |
| payment_method | character varying | YES | Purpose unclear from available data. |
| total_amount | numeric | NO | This column represents the monetary total of payments made to vendors, with values showing varied payment amounts that could be associated with different transactions or invoices. Each entry indicates a specific amount paid, with the values reflecting a range from hundreds to thousands, suggesting payments of varying scale to supplier entities. |
| currency | character varying | YES | This column represents the currency type used for vendor payments, with examples including British Pounds (GBP), United States Dollars (USD), and Euros (EUR). The default currency for entries is set to USD. |
| bank_account_id | integer | YES | This column represents the identification number assigned to different bank accounts involved in processing vendor payments. Purpose unclear from available data. |
| reference_number | character varying | YES | This column likely captures unique identifiers associated with individual vendor payment transactions. Each value is a distinct number potentially used for tracking or referencing payments within the business process. |
| status | character varying | YES | Indicates the current state of a vendor payment, reflecting stages such as active, pending, or inactive. The majority of payments appear to be in the ongoing or active stage. |
| created_at | timestamp without time zone | YES | This column records the date and time when a vendor payment record was initially created, capturing the moment of data entry in the system. It defaults to the current timestamp at the time of record creation. |
| updated_at | timestamp without time zone | YES | Records the date and time when a vendor payment entry was last modified. This timestamp defaults to the current time when no other value is provided. |

## Primary Key

`payment_id`

## Foreign Keys

- `bank_account_id` → `synthetic.bank_accounts.bank_account_id`
- `vendor_id` → `synthetic.vendors.vendor_id`

## Indexes

- `vendor_payments_payment_number_key`: CREATE UNIQUE INDEX vendor_payments_payment_number_key ON synthetic.vendor_payments USING btree (payment_number)
- `vendor_payments_pkey`: CREATE UNIQUE INDEX vendor_payments_pkey ON synthetic.vendor_payments USING btree (payment_id)

## Sample Data

| payment_id | payment_number | vendor_id | payment_date | payment_method | total_amount | currency | bank_account_id | reference_number | status | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 104332181960013 | 82 | Thu May 30 2024 00:00:00 GMT-0500 (Central Dayl... | Recently future choice whatever. | 1122.20 | GBP | 35 | 781618495931034 | active | Sat Dec 13 2025 03:17:40 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:40 GMT-0600 (Central Stan... |
| 2 | 131647525534192 | 29 | Sun Jan 05 2025 00:00:00 GMT-0600 (Central Stan... | Clear here writer policy news. | 1403.98 | USD | 87 | 395376724238849 | pending | Sat Dec 13 2025 03:17:40 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:40 GMT-0600 (Central Stan... |
| 3 | 696532871012269 | 70 | Sat Jan 27 2024 00:00:00 GMT-0600 (Central Stan... | Other life edge network wall quite. | 878.52 | EUR | 5 | 146270482814893 | active | Sat Dec 13 2025 03:17:40 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:40 GMT-0600 (Central Stan... |
| 4 | 252880957015430 | 12 | Wed Jun 05 2024 00:00:00 GMT-0500 (Central Dayl... | Water beat magazine attorney set she campaign. | 2194.19 | GBP | 78 | 346578713315098 | active | Sat Dec 13 2025 03:17:40 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:40 GMT-0600 (Central Stan... |
| 5 | 393010310518347 | 72 | Thu May 16 2024 00:00:00 GMT-0500 (Central Dayl... | Rich think office drug. | 1996.39 | GBP | 90 | 106513338726247 | pending | Sat Dec 13 2025 03:17:40 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:17:40 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:45:10.622Z*