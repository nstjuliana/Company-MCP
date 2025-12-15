# intercompany_transactions

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.intercompany_transactions` table represents transactions between different accounts within the same corporate group, each identified by a unique primary key `ic_transaction_id`. It includes details such as the account involved (`ic_account_id`), the date of the transaction (`transaction_date`), the monetary value of the transaction (`amount`), and its current `status`, among other attributes. Though it contains a foreign key relationship undefined in the provided data, the table serves as a record-keeping structure for managing intercompany financial activities within the synthetic database.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| ic_transaction_id | integer | NO | This column uniquely identifies each transaction within the intercompany transactions dataset. It sequentially assigns an identifier to each transaction, ensuring distinct tracking. |
| ic_account_id | integer | NO | This column represents an identifier for accounts involved in intercompany transactions, ensuring unique identification of entities within the organization's internal financial exchanges. |
| transaction_date | date | NO | This column represents the dates on which intercompany transactions occur, capturing specific calendar days in various years including 2024 and 2025, observed in Central Standard or Daylight Time. The purpose is to track the timing of these financial events within the organizations involved. |
| amount | numeric | NO | The column represents the transaction amounts exchanged between companies within a corporate group. Each value indicates the monetary size of a particular transaction, highlighting varying levels of intercompany financial activity. |
| description | character varying | YES | This column contains detailed narratives or insights related to various transactions involving customers, highlighting activities or events with diverse entities. Purpose unclear from available data, but it may include commentary on transaction context or specifics. |
| reference_number | character varying | YES | This column represents unique identifiers assigned to each transaction within the intercompany transactions table. These identifiers help differentiate and track individual transactions. |
| status | character varying | YES | This column denotes the current stage or condition of intercompany transactions, reflecting various states such as 'active', 'pending', 'completed', 'cancelled', and 'inactive'. It is used to track the transaction's lifecycle and operational status. |
| created_at | timestamp without time zone | YES | This column records the date and time when an intercompany transaction was created. It is used to track the timing of each transaction's entry into the system. |
| updated_at | timestamp without time zone | YES | This column records the last modification date and time of intercompany transactions. Purpose unclear from available data. |

## Primary Key

`ic_transaction_id`

## Foreign Keys

- `ic_account_id` → `synthetic.intercompany_accounts.ic_account_id`

## Indexes

- `intercompany_transactions_pkey`: CREATE UNIQUE INDEX intercompany_transactions_pkey ON synthetic.intercompany_transactions USING btree (ic_transaction_id)

## Sample Data

| ic_transaction_id | ic_account_id | transaction_date | amount | description | reference_number | status | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 17 | Mon Jan 06 2025 00:00:00 GMT-0600 (Central Stan... | 37006.58 | Customer card music provide these. Middle autho... | 81014982022507895651 | active | Sat Dec 13 2025 02:55:26 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:26 GMT-0600 (Central Stan... |
| 2 | 43 | Mon Jul 14 2025 00:00:00 GMT-0500 (Central Dayl... | 20756.73 | Back here quickly situation product guess. Crim... | 68212432093173880222 | pending | Sat Dec 13 2025 02:55:26 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:26 GMT-0600 (Central Stan... |
| 3 | 25 | Thu Jul 10 2025 00:00:00 GMT-0500 (Central Dayl... | 47020.46 | North chance civil property wait eat. Participa... | 64729539384264008879 | completed | Sat Dec 13 2025 02:55:26 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:26 GMT-0600 (Central Stan... |
| 4 | 3 | Fri Feb 09 2024 00:00:00 GMT-0600 (Central Stan... | 4086.48 | Tv light conference force. Town current morning... | 10621309966229063470 | pending | Sat Dec 13 2025 02:55:26 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:26 GMT-0600 (Central Stan... |
| 5 | 7 | Thu Mar 07 2024 00:00:00 GMT-0600 (Central Stan... | 70403.25 | Doctor go manager the live include. Sometimes e... | 07132975335736105084 | cancelled | Sat Dec 13 2025 02:55:26 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:26 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:13.693Z*