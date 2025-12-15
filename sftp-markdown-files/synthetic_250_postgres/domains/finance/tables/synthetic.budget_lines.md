# budget_lines

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.budget_lines` table represents individual line items within a budget, uniquely identified by `budget_line_id`. Each entry is associated with a specific budget (`budget_id`), account (`account_id`), and time period (`period_id`), detailing the `budgeted_amount` and optionally including additional context in the `notes` field. The table's role in the data model is to capture detailed budget planning components, although it does not have explicitly defined foreign key relationships or tables that reference it.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| budget_line_id | integer | NO | This is a unique identifier assigned to each item within the budget category, indicating its position or entry order in a sequence. Purpose unclear from available data. |
| budget_id | integer | NO | This column likely represents a unique identifier for individual budget entries within the budget lines table, acting as a reference point or index for each budget line record. Each unique number signifies a different budget entry, connecting detailed financial data to a broader financial plan or framework. |
| account_id | integer | NO | This column likely identifies distinct accounts related to budget entries, using a unique numerical identifier for each account. Purpose unclear from available data. |
| period_id | integer | YES | Represents an identifier for specific time periods or cycles related to budget allocations. Purpose unclear from available data. |
| budgeted_amount | numeric | NO | This column represents the allocated funding amounts for various budgetary items or activities in a financial planning context, with values consistently expressed in monetary terms. The purpose is to track the planned expenditures. |
| notes | text | YES | This column likely captures descriptive texts or commentary related to budget lines, potentially outlining details or considerations pertinent to each entry. The exact purpose of these notes is unclear from the available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a budget line entry was created, defaulting to the current timestamp at the time of entry creation. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when an entry in the budget_lines table was last updated. Purpose unclear from available data. |

## Primary Key

`budget_line_id`

## Foreign Keys

- `account_id` → `synthetic.chart_of_accounts.account_id`
- `budget_id` → `synthetic.budgets.budget_id`
- `period_id` → `synthetic.fiscal_periods.period_id`

## Indexes

- `budget_lines_pkey`: CREATE UNIQUE INDEX budget_lines_pkey ON synthetic.budget_lines USING btree (budget_line_id)

## Sample Data

| budget_line_id | budget_id | account_id | period_id | budgeted_amount | notes | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 12 | 7 | 7 | 52486.10 | Deal about avoid beat. Whom green stop some cou... | Sat Dec 13 2025 02:54:48 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:48 GMT-0600 (Central Stan... |
| 2 | 16 | 13 | 40 | 52692.95 | Hotel including audience girl. Play study estab... | Sat Dec 13 2025 02:54:48 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:48 GMT-0600 (Central Stan... |
| 3 | 23 | 18 | 26 | 7994.02 | History memory still race. | Sat Dec 13 2025 02:54:48 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:48 GMT-0600 (Central Stan... |
| 4 | 26 | 30 | 37 | 24396.47 | Election white free whose at phone image. For c... | Sat Dec 13 2025 02:54:48 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:48 GMT-0600 (Central Stan... |
| 5 | 45 | 15 | 20 | 68435.76 | Sound late subject health. Beat open public rea... | Sat Dec 13 2025 02:54:48 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:48 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:02.841Z*