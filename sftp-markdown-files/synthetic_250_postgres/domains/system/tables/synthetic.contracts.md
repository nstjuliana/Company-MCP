# contracts

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.contracts` table represents contractual agreements within a business context, identified uniquely by a `contract_id`. Each contract includes details such as contract number, name, status, terms, value, and dates marking its duration, alongside relevant account and owner identifiers, suggesting it plays a crucial role in managing and tracking contract lifecycle and execution. While it references an undefined table through `account_id`, the absence of further relationships indicates its primary function is focused on encapsulating contract-specific data rather than facilitating inter-table dependencies.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| contract_id | integer | NO | This column represents a distinct identifier assigned to each contract within the database to ensure unique identification and tracking. The sequence of numbers suggests it is used as a primary or key identifier for contract entries. |
| contract_number | character varying | YES | This column appears to contain unique identifiers for individual contracts, with entries likely serving to differentiate or track specific contractual agreements. Purpose unclear from available data. |
| account_id | integer | YES | This column likely refers to a unique identifier for accounts associated with contracts. Purpose unclear from available data. |
| contract_name | character varying | YES | This column appears to store textual phrases or titles that could describe various aspects of contracts, possibly reflecting their subject matter or key themes, based on the diverse, thematic samples provided. Purpose unclear from available data. |
| status | character varying | YES | This column indicates the current state or progress of a contract, reflecting various stages such as inactive, pending, completed, cancelled, and active. It helps track the status of contractual agreements through their lifecycle. |
| start_date | date | YES | This column represents the date on which a contract becomes active. It allows for null entries, indicating that not all contracts have a defined activation date. |
| end_date | date | YES | This column indicates the final date on which a particular contract expires or concludes. It allows for flexibility as it can remain empty if the contract's end date is not predetermined or not applicable. |
| contract_term | integer | YES | The numbers likely represent the duration of contracts, potentially measured in days, indicating how long each contract is valid. The purpose is related to the timeframe of contractual agreements but is otherwise unclear from available data. |
| contract_value | numeric | YES | This column represents the monetary worth associated with a particular agreement or contract. It indicates the financial obligation or value of a given contract, with the understanding that exact use in business processes is not specified. |
| billing_frequency | character varying | YES | Purpose unclear from available data. |
| description | text | YES | The column contains narrative summaries or discussions related to contract activities, which may include aspects such as strategic considerations, operational contexts, or industry dynamics. Purpose unclear from available data. |
| owner_id | integer | YES | This column likely identifies the individual or entity that holds ownership pertaining to the given contract within the dataset. The available data does not clarify the specific role or significance of these owners beyond being numerical identifiers. |
| signed_date | date | YES | This column represents the date when a contract was signed, as indicated by the presence of various specific dates. The purpose or specific context of these contracts is unclear from the available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a contract was initially created in the system. It helps track the inception timing of each contract for historical reference and auditing purposes. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a contract was last updated. It appears to capture system-generated timestamps for tracking changes to contractual records. |

## Primary Key

`contract_id`

## Foreign Keys

- `account_id` → `synthetic.accounts.account_id`

## Indexes

- `contracts_contract_number_key`: CREATE UNIQUE INDEX contracts_contract_number_key ON synthetic.contracts USING btree (contract_number)
- `contracts_pkey`: CREATE UNIQUE INDEX contracts_pkey ON synthetic.contracts USING btree (contract_id)

## Sample Data

| contract_id | contract_number | account_id | contract_name | status | start_date | end_date | contract_term | contract_value | billing_frequency | description | owner_id | signed_date | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 93078042651070547281 | 48 | Special state no song maybe past. Work medical ... | inactive | Mon Feb 26 2024 00:00:00 GMT-0600 (Central Stan... | Sat Nov 08 2025 00:00:00 GMT-0600 (Central Stan... | 8100 | 557.46 | Success until try voice produce. | Director voice window. Shoulder own different i... | 7502 | Tue Apr 01 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:59:23 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:23 GMT-0600 (Central Stan... |
| 2 | 20049269993848384160 | 25 | Follow culture meet give direction heart. Large... | pending | Mon Jan 13 2025 00:00:00 GMT-0600 (Central Stan... | Sat Jun 08 2024 00:00:00 GMT-0500 (Central Dayl... | 6044 | 199.11 | Soldier husband can attorney gas. | Charge wide include radio week any brother skin... | 688 | Sun Mar 31 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:59:23 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:23 GMT-0600 (Central Stan... |
| 3 | 80763582335732319531 | 3 | Onto management no opportunity walk recently. M... | completed | Wed Apr 30 2025 00:00:00 GMT-0500 (Central Dayl... | Tue Jan 07 2025 00:00:00 GMT-0600 (Central Stan... | 3082 | 3.72 | Prove matter financial marriage dark probably TV. | Media answer social player. Your until learn pr... | 5824 | Sun Feb 18 2024 00:00:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:23 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:23 GMT-0600 (Central Stan... |
| 4 | 88277737165688756023 | 2 | Relationship rule season central trade beautifu... | pending | Thu Sep 12 2024 00:00:00 GMT-0500 (Central Dayl... | Mon Nov 03 2025 00:00:00 GMT-0600 (Central Stan... | 5550 | 415.53 | Throw finally guess nor whole. | Defense local step. Behind determine trade coup... | 122 | Tue Mar 11 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:59:23 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:23 GMT-0600 (Central Stan... |
| 5 | 75558203891679136474 | 21 | Piece work yet television budget. Really becaus... | completed | Sun May 11 2025 00:00:00 GMT-0500 (Central Dayl... | Tue Aug 26 2025 00:00:00 GMT-0500 (Central Dayl... | 1397 | 134.08 | Simple the seem decision sell responsibility ten. | Born again plant away hope. Season off area ind... | 1573 | Wed May 21 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:59:23 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:59:23 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:06.556Z*