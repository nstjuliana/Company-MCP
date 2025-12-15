# bank_accounts

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.bank_accounts` table represents bank account details, capturing essential information such as account names, numbers, bank details, types, and balances, with a primary key of `bank_account_id`. While it has a foreign key `gl_account_id` indicating linkage to another table, the specifics of this relationship are not defined, but it suggests integration with a general ledger system. The table is crucial for encapsulating individual account records, holding meta-information like creation and update timestamps alongside balance details, ensuring it is a key component in modeling financial data.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| bank_account_id | integer | NO | This column represents a unique identifier assigned to each bank account in the system. The sequence of integer values implies it serves as a primary key for the table, ensuring each account can be distinctly identified. |
| account_name | character varying | NO | This column appears to hold descriptive titles or phrases, possibly representing the names or identifiers of individual bank accounts. Purpose unclear from available data. |
| account_number | character varying | YES | This column represents unique identifiers assigned to individual bank accounts, which are composed of numeric strings of varying lengths. Purpose unclear from available data. |
| routing_number | character varying | YES | The column contains numerical identifiers that likely represent banking routing numbers used to facilitate the exchange of funds between financial institutions. These values appear to be arbitrary long strings of digits, suggesting they may be placeholders in this synthetic dataset. |
| bank_name | character varying | YES | Purpose unclear from available data. |
| account_type | character varying | YES | Purpose unclear from available data. Sample values do not provide clear indication of what the data represents in business terms. |
| currency | character varying | YES | This column represents the type of currency associated with a bank account, indicating the denomination in which transactions or balances are recorded. Common currencies included are the Euro, US Dollar, British Pound, Canadian Dollar, and Japanese Yen. |
| current_balance | numeric | YES | This column represents the amount of money currently available in a bank account, reflecting the immediate accessible funds for transactions. The values typically vary significantly among different accounts, indicating differing levels of financial activity or account holder prosperity. |
| gl_account_id | integer | YES | This column likely represents identifiers for general ledger accounts associated with bank accounts. Each identifier is a unique number that links bank transactions to their corresponding general ledger account for financial tracking and reporting. |
| is_active | boolean | YES | Indicates whether a bank account is currently active. A value of "true" suggests an active account status, while "false" denotes inactivity. |
| created_at | timestamp without time zone | YES | This column captures the date and time when a bank account entry was created, defaulting to the current timestamp at the moment of creation. Its main usage appears to be tracking the creation date of each record in the bank accounts table. |
| updated_at | timestamp without time zone | YES | This column captures the date and time when a bank account record was last updated. Its purpose is unclear from the available data. |

## Primary Key

`bank_account_id`

## Foreign Keys

- `gl_account_id` → `synthetic.chart_of_accounts.account_id`

## Indexes

- `bank_accounts_pkey`: CREATE UNIQUE INDEX bank_accounts_pkey ON synthetic.bank_accounts USING btree (bank_account_id)

## Sample Data

| bank_account_id | account_name | account_number | routing_number | bank_name | account_type | currency | current_balance | gl_account_id | is_active | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Attorney use discuss week this democratic to. R... | 75153672097506699128 | 56859441649331115685 | Color security by. Among respond prevent act ea... | doctor | EUR | 952.79 | 10 | false | Sat Dec 13 2025 02:54:35 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:35 GMT-0600 (Central Stan... |
| 2 | Culture forward same leg measure here. Law arou... | 43968483596000182087 | 16388193927191899381 | Long page benefit forward best modern available... | last | USD | 126.23 | 16 | false | Sat Dec 13 2025 02:54:35 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:35 GMT-0600 (Central Stan... |
| 3 | Garden east man process artist technology. Fly ... | 44654482187398212558 | 87740503151346508656 | Turn ready despite make entire look man. Film c... | degree | GBP | 382.85 | 37 | true | Sat Dec 13 2025 02:54:35 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:35 GMT-0600 (Central Stan... |
| 4 | Top see seven mind worry area activity. Along s... | 97114917946190692395 | 10832786686899842003 | Vote former political you there trouble. Behind... | full | CAD | 153.44 | 29 | false | Sat Dec 13 2025 02:54:35 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:35 GMT-0600 (Central Stan... |
| 5 | Year return would build. Various trouble phone ... | 89762177942921017274 | 82151750796313240496 | Too recognize wind five particular hot loss eve... | somebody | GBP | 443.94 | 5 | true | Sat Dec 13 2025 02:54:35 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:35 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:03.940Z*