# depreciation_schedule

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.depreciation_schedule` table represents the scheduled depreciation entries for assets, detailing the depreciation amount, accumulated total, and book value over specified periods for effective asset management. The primary key `schedule_id` uniquely identifies each depreciation entry, and columns like `asset_id` and `period_id` suggest associations with assets and time periods, although specific table relationships are undefined. This table likely plays a critical role in tracking the depreciation process, as indicated by the `depreciation_date`, `depreciation_amount`, and `is_posted`, which collectively facilitate financial reporting and accounting procedures.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| schedule_id | integer | NO | This column uniquely identifies each entry within a series in a sequential order for a depreciation schedule. It serves as a primary key to ensure each record is distinct and traceable. |
| asset_id | integer | NO | This column likely represents a unique identifier assigned to each asset within a depreciation schedule, ensuring each asset is distinctly tracked. Purpose unclear from available data. |
| period_id | integer | YES | This column likely represents a numerical identifier for specific periods or intervals within a depreciation schedule. Purpose unclear from available data. |
| depreciation_date | date | NO | This column represents the scheduled dates on which asset depreciation values are recorded or reviewed within the system. The dates appear to track predetermined intervals for assessing the depreciating value of assets. |
| depreciation_amount | numeric | NO | This column represents the monetary value allocated as depreciation for specific assets within a schedule, expressed numerically with typical amounts ranging from hundreds to tens of thousands. The purpose is to quantify asset value reduction over time for accounting and financial reporting. |
| accumulated_total | numeric | YES | This column appears to represent the cumulative value of depreciation for an asset over time, possibly indicating how much an asset's value has decreased. Purpose unclear from available data without further context. |
| book_value | numeric | YES | This column represents the residual value of an asset at various points in time according to a depreciation schedule. Purpose unclear from available data without further business context. |
| is_posted | boolean | YES | Indicates whether an entry in the depreciation schedule has been officially recorded or confirmed. A value of true signifies it is posted, while a value of false means it is not. |
| created_at | timestamp without time zone | YES | This column records the date and time when each entry in the depreciation schedule table was created. It reflects the creation timestamp, defaulting to the current time at entry, but the specific business purpose of this information is unclear from the available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when records in the depreciation schedule were last updated, with entries defaulting to the current timestamp at the time of record modification. Purpose unclear from available data due to uniformity of sample values. |

## Primary Key

`schedule_id`

## Foreign Keys

- `asset_id` → `synthetic.fixed_assets.asset_id`
- `period_id` → `synthetic.fiscal_periods.period_id`

## Indexes

- `depreciation_schedule_pkey`: CREATE UNIQUE INDEX depreciation_schedule_pkey ON synthetic.depreciation_schedule USING btree (schedule_id)

## Sample Data

| schedule_id | asset_id | period_id | depreciation_date | depreciation_amount | accumulated_total | book_value | is_posted | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 17 | 6 | Thu Jul 17 2025 00:00:00 GMT-0500 (Central Dayl... | 37247.19 | 903.80 | 165.53 | false | Sat Dec 13 2025 02:54:54 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:54 GMT-0600 (Central Stan... |
| 2 | 41 | 20 | Mon Apr 07 2025 00:00:00 GMT-0500 (Central Dayl... | 72626.24 | 755.23 | 429.23 | true | Sat Dec 13 2025 02:54:54 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:54 GMT-0600 (Central Stan... |
| 3 | 46 | 7 | Fri Oct 04 2024 00:00:00 GMT-0500 (Central Dayl... | 208.52 | 476.81 | 132.70 | true | Sat Dec 13 2025 02:54:54 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:54 GMT-0600 (Central Stan... |
| 4 | 34 | 44 | Sun Aug 04 2024 00:00:00 GMT-0500 (Central Dayl... | 44562.18 | 8.06 | 343.57 | true | Sat Dec 13 2025 02:54:54 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:54 GMT-0600 (Central Stan... |
| 5 | 28 | 45 | Tue May 20 2025 00:00:00 GMT-0500 (Central Dayl... | 13304.30 | 70.83 | 383.07 | true | Sat Dec 13 2025 02:54:54 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:54 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:03.761Z*