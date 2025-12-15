# bank_transactions

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.bank_transactions` table represents records of transactions occurring in bank accounts, uniquely identified by `transaction_id`. Each transaction includes details such as the associated `bank_account_id`, `transaction_date`, `transaction_type`, `amount`, and transaction metadata like `description`, `reference_number`, and reconciliation status with `is_reconciled` and `reconciled_date`. This table plays a central role in tracking individual bank transactions and, although it is not currently linked to other tables via foreign keys, it might relate to account management data in a broader financial data model.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| transaction_id | integer | NO | This column represents a unique identifier assigned sequentially to each transaction in the bank transactions table. It ensures that every transaction can be distinctly referenced within the system. |
| bank_account_id | integer | NO | This column identifies individual bank accounts associated with transactions using unique numerical identifiers. Each integer represents a specific bank account involved in the recorded financial activities. |
| transaction_date | date | NO | This column represents the specific date on which each bank transaction occurred, capturing both standard and daylight saving time variations in the Central time zone. It is a mandatory field, as evident from the absence of null values. |
| transaction_type | character varying | YES | Purpose unclear from available data. |
| amount | numeric | NO | This column represents the monetary amounts involved in individual bank transactions. The values indicate sums handled in these transactions, typically represented in a currency format without any apparent decimal restrictions. |
| description | character varying | YES | This column seems to capture brief narrative summaries or statements, possibly related to transaction details or context descriptions. Purpose unclear from available data. |
| reference_number | character varying | YES | This column likely contains unique identifiers assigned to individual bank transactions, serving as a reference for tracking and managing transaction records. The purpose of these identifiers is to facilitate the retrieval and verification of transaction details. |
| is_reconciled | boolean | YES | Indicates whether a bank transaction has been reconciled in the financial records. Reconciliation status is often necessary to ensure transaction accuracy and integrity. |
| reconciled_date | date | YES | This column captures the date on which a bank transaction has been reconciled, indicating the confirmation of transaction accuracy between records. The values suggest it can represent dates across different months and years, highlighting the periodic nature of reconciliation in banking activities. |
| created_at | timestamp without time zone | YES | This column indicates the date and time when a bank transaction record was created. It defaults to the current timestamp, capturing when the transaction entry is logged. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a bank transaction record was last updated. The default value indicates that it is automatically set to the current time when any updates occur. |

## Primary Key

`transaction_id`

## Foreign Keys

- `bank_account_id` → `synthetic.bank_accounts.bank_account_id`

## Indexes

- `bank_transactions_pkey`: CREATE UNIQUE INDEX bank_transactions_pkey ON synthetic.bank_transactions USING btree (transaction_id)

## Sample Data

| transaction_id | bank_account_id | transaction_date | transaction_type | amount | description | reference_number | is_reconciled | reconciled_date | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 38 | Mon Dec 02 2024 00:00:00 GMT-0600 (Central Stan... | great | 35354.22 | Wife guess production nothing employee. Side au... | 00468797521008486542 | true | Wed Aug 21 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:54:38 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:38 GMT-0600 (Central Stan... |
| 2 | 19 | Thu Oct 30 2025 00:00:00 GMT-0500 (Central Dayl... | second | 49539.93 | Himself central close area second focus entire.... | 90706487235838951752 | false | Sat Jan 20 2024 00:00:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:38 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:38 GMT-0600 (Central Stan... |
| 3 | 19 | Fri Nov 15 2024 00:00:00 GMT-0600 (Central Stan... | agency | 53715.41 | Minute recently reach land can. | 32553827438326225063 | true | Sun Jul 21 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:54:38 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:38 GMT-0600 (Central Stan... |
| 4 | 28 | Tue May 14 2024 00:00:00 GMT-0500 (Central Dayl... | eat | 13480.10 | Task author time improve interest. Until we eat... | 41852039710104433050 | false | Mon Feb 10 2025 00:00:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:38 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:38 GMT-0600 (Central Stan... |
| 5 | 47 | Sat Jan 20 2024 00:00:00 GMT-0600 (Central Stan... | partner | 36641.19 | Star American oil important after. Type theory ... | 75019325267494222166 | false | Tue Jan 23 2024 00:00:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:38 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:38 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:03.347Z*