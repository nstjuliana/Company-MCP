# intercompany_accounts

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.intercompany_accounts` table captures details of intercompany transactions between entities, identified by the `ic_account_id` primary key. It records the originating entity (`entity_from`), the receiving entity (`entity_to`), associated general ledger account (`gl_account_id`), and timestamps for record maintenance (`created_at`, `updated_at`), with a boolean flag `is_active` indicating current activity status. Despite no explicit foreign key relationships defined, the table likely integrates with other financial records through `gl_account_id`, facilitating analysis of intercompany dealings within the synthetic business framework.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| ic_account_id | integer | NO | This column serves as a unique identifier for entries in the intercompany accounts table, sequentially allocating numbers to each new entry. It ensures distinct identification for organizational purposes in intercompany financial records. |
| entity_from | character varying | NO | This column appears to represent descriptions or notes pertaining to various transactions or interactions within intercompany accounts, possibly including actions or decisions made by entity managers. The purpose remains unclear from the available data. |
| entity_to | character varying | NO | The column appears to capture descriptive text or narrative related to transactions or activities involving multiple entities, possibly within an organization. Purpose unclear from available data, as the text is varied and lacks a consistent pattern indicative of specific business terms. |
| gl_account_id | integer | YES | Represents the identifier for a general ledger account used in recording intercompany transactions. Purpose unclear from available data. |
| is_active | boolean | YES | Indicates whether intercompany accounts are currently active or inactive. The default status is active, suggesting that new entries typically start as active unless specified otherwise. |
| created_at | timestamp without time zone | YES | This column records the date and time when an intercompany account entry was created, reflecting when an event or transaction was captured in the system. The purpose of this information is to track the timeline of account activities or updates. |
| updated_at | timestamp without time zone | YES | This column records the date and time when the intercompany account information was last updated. It automatically defaults to the current timestamp but can be nullable, indicating updates may not always occur. |

## Primary Key

`ic_account_id`

## Foreign Keys

- `gl_account_id` → `synthetic.chart_of_accounts.account_id`

## Indexes

- `intercompany_accounts_pkey`: CREATE UNIQUE INDEX intercompany_accounts_pkey ON synthetic.intercompany_accounts USING btree (ic_account_id)

## Sample Data

| ic_account_id | entity_from | entity_to | gl_account_id | is_active | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Key simply look important entire. Performance p... | Early side billion once thousand.
Can sense bil... | 4 | false | Sat Dec 13 2025 02:55:23 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:23 GMT-0600 (Central Stan... |
| 2 | Manager throughout address movement ability. Or... | Region institution region ago. Leave cultural p... | 42 | true | Sat Dec 13 2025 02:55:23 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:23 GMT-0600 (Central Stan... |
| 3 | Type team exist ground owner practice. Read ful... | Sit care support while will. Produce three fish... | 19 | true | Sat Dec 13 2025 02:55:23 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:23 GMT-0600 (Central Stan... |
| 4 | Film say five executive over. Remember hour alm... | Adult professor and green person everybody. | 17 | true | Sat Dec 13 2025 02:55:23 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:23 GMT-0600 (Central Stan... |
| 5 | Agent teach so on buy no. Third week industry f... | Charge choice million thing two relationship. S... | 13 | false | Sat Dec 13 2025 02:55:23 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:23 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:13.623Z*