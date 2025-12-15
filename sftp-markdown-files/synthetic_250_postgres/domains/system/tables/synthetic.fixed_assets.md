# fixed_assets

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.fixed_assets` table represents a collection of tangible long-term resources owned by an organization, detailing each asset's unique attributes such as acquisition cost, useful life, and depreciation. With columns like `asset_id`, `acquisition_date`, `depreciation_method`, and `current_value`, the table captures detailed information about each asset's financial and operational status, without linking to other tables. This standalone table serves a critical function by tracking the lifecycle of fixed assets, from acquisition to disposal, aiding in financial reporting and asset management.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| asset_id | integer | NO | This column uniquely identifies each fixed asset within the dataset, ensuring that each asset can be easily referenced and tracked. The values indicate a sequential numbering system for assets. |
| asset_tag | character varying | YES | Purpose unclear from available data. The sample values appear to be diverse and do not suggest a consistent pattern for interpreting the expected content or purpose. |
| asset_name | character varying | NO | This column contains descriptions of various assets, with entries resembling phrases or titles that might relate to asset names or themes. Purpose unclear from available data. |
| category | character varying | YES | Purpose unclear from available data. |
| acquisition_date | date | YES | This column represents the date on which a fixed asset was acquired within the organization. It is used to track the purchase dates of assets for record-keeping and accounting purposes. |
| acquisition_cost | numeric | YES | The column represents the initial monetary value paid for acquiring fixed assets. This value can vary significantly across different assets, as evidenced by the range of the sample values provided. |
| useful_life_years | integer | YES | Represents the expected duration in years that a fixed asset is considered to remain functional and generate value for the business. Purpose unclear from available data. |
| salvage_value | numeric | YES | This column represents the estimated residual value of fixed assets at the end of their useful life, which can still be recovered or sold. The values reflect the predicted amount to be obtained from disposal or resale. |
| depreciation_method | character varying | YES | Purpose unclear from available data. |
| accumulated_depreciation | numeric | YES | The column represents the cumulative depreciation amounts attributed to fixed assets over time. These values indicate the total reduction in value of the assets due to factors such as wear and tear. |
| current_value | numeric | YES | This column represents the monetary value assigned to fixed assets at a given point in time. Purpose unclear from available data. |
| location | character varying | YES | Purpose unclear from available data. The sample values consist of abstract phrases without specific business context or location references. |
| status | character varying | YES | This column represents the current state or condition of a fixed asset, indicating whether it is pending, active, completed, or cancelled. It helps track the lifecycle status of assets in the system. |
| disposal_date | date | YES | This column records the date on which a fixed asset is disposed of or is planned to be disposed of within the business. The specific timing reflects the conversion or removal of assets from the company's balance sheet. |
| created_at | timestamp without time zone | YES | This column records the date and time when an entry in the fixed assets table was created. The timestamp reflects when the data was initially entered into the system, defaulting to the current time upon entry. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a fixed asset record was last modified. Updates default to the current timestamp indicating the most recent change to asset details. |

## Primary Key

`asset_id`

## Indexes

- `fixed_assets_asset_tag_key`: CREATE UNIQUE INDEX fixed_assets_asset_tag_key ON synthetic.fixed_assets USING btree (asset_tag)
- `fixed_assets_pkey`: CREATE UNIQUE INDEX fixed_assets_pkey ON synthetic.fixed_assets USING btree (asset_id)

## Sample Data

| asset_id | asset_tag | asset_name | category | acquisition_date | acquisition_cost | useful_life_years | salvage_value | depreciation_method | accumulated_depreciation | current_value | location | status | disposal_date | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Unit policy never need. | Couple pull senior from performance ground. Hea... | Really song Republican like any amount break. T... | Wed Oct 23 2024 00:00:00 GMT-0500 (Central Dayl... | 96779.53 | 2021 | 325.89 | Play treat ok. | 280.30 | 785.87 | Life interest special economy crime value note.... | pending | Thu Aug 01 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:54:51 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:51 GMT-0600 (Central Stan... |
| 2 | High total debate base. | Industry whom he face adult. Bed information th... | Kind campaign couple. Mention raise right forme... | Mon Sep 22 2025 00:00:00 GMT-0500 (Central Dayl... | 11477.39 | 2024 | 199.80 | Later serious wall rest may also administration. | 997.26 | 179.93 | Opportunity mind free imagine above quickly ima... | cancelled | Thu Sep 11 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:54:51 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:51 GMT-0600 (Central Stan... |
| 3 | In those road style certain popular. | Their successful station sell thus official ene... | Very activity case station. Someone quickly pla... | Fri Sep 12 2025 00:00:00 GMT-0500 (Central Dayl... | 2788.92 | 2025 | 461.62 | Arrive Mr act. | 708.37 | 438.45 | Keep only compare. Also remain morning. Soon fe... | pending | Fri Jun 07 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:54:51 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:51 GMT-0600 (Central Stan... |
| 4 | There citizen will specific describe. | Do already case require sit space be. Appear se... | Everybody TV rule sport real yourself. Property... | Sun Jan 26 2025 00:00:00 GMT-0600 (Central Stan... | 83145.05 | 2020 | 818.97 | Particular capital worry role call. | 795.66 | 409.14 | Throw central stage well. Financial even affect... | completed | Mon Jun 24 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:54:51 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:51 GMT-0600 (Central Stan... |
| 5 | Idea begin tell size. | Million performance adult actually forward. Mys... | Prepare decide anyone Republican travel wall me... | Sun Jun 15 2025 00:00:00 GMT-0500 (Central Dayl... | 14003.99 | 2022 | 242.02 | Or evidence half. | 658.66 | 715.24 | Tough training contain message cell. Friend may... | completed | Wed Sep 11 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:54:51 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:51 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:07.297Z*