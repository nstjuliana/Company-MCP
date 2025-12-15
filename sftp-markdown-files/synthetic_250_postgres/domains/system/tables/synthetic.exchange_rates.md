# exchange_rates

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.exchange_rates` table represents a collection of historical currency exchange rates between various currency pairs, identified by `rate_id` as the primary key. Each entry records the rate at which one currency (`from_currency`) was exchanged for another (`to_currency`) on a specific date (`rate_date`), along with the source of the exchange information. While the table lacks explicit foreign key relationships, its role in the data model appears to be storing exchange rate histories that could support financial analytic operations or currency conversion calculations.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| rate_id | integer | NO | This column represents a unique identifier for each record in the exchange rates table, incrementing sequentially. |
| from_currency | character varying | NO | This column represents a code for different currencies involved in exchange rate transactions. It specifies the originating currency code from which an exchange rate is being calculated. |
| to_currency | character varying | NO | This column represents the target currency code used in exchange rates, indicating the currency to which values are converted. Purpose unclear from available data as the codes are not standard ISO currency codes. |
| rate_date | date | NO | This column represents the date on which a particular exchange rate is applicable. The values indicate specific days throughout the year, including adjustments for daylight saving time. |
| exchange_rate | numeric | NO | This column represents the conversion rates between two currencies within a synthetic or simulated environment. The values reflect how much of one currency is needed to obtain a unit of another currency at a given point in time. |
| source | character varying | YES | Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column captures the date and time when an exchange rate record was initially created, reflecting the standard time zone where the data originates. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when the exchange rate information was last updated. Purpose unclear from available data beyond indicating update timing. |

## Primary Key

`rate_id`

## Foreign Keys

- `from_currency` → `synthetic.currencies.currency_code`
- `to_currency` → `synthetic.currencies.currency_code`

## Indexes

- `exchange_rates_pkey`: CREATE UNIQUE INDEX exchange_rates_pkey ON synthetic.exchange_rates USING btree (rate_id)

## Sample Data

| rate_id | from_currency | to_currency | rate_date | exchange_rate | source | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | QRC | JWZ | Mon Dec 16 2024 00:00:00 GMT-0600 (Central Stan... | 63.81910000 | With away environment show water paper control. | Sat Dec 13 2025 02:55:04 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:04 GMT-0600 (Central Stan... |
| 2 | AKR | RIF | Sat Oct 19 2024 00:00:00 GMT-0500 (Central Dayl... | 84.37690000 | Feeling food method interest hotel standard. | Sat Dec 13 2025 02:55:04 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:04 GMT-0600 (Central Stan... |
| 3 | YJT | QOM | Wed Jan 08 2025 00:00:00 GMT-0600 (Central Stan... | 47.09440000 | Machine project trade. | Sat Dec 13 2025 02:55:04 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:04 GMT-0600 (Central Stan... |
| 4 | XJU | PTO | Tue Jun 03 2025 00:00:00 GMT-0500 (Central Dayl... | 9.11370000 | Among most for begin technology seem. | Sat Dec 13 2025 02:55:04 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:04 GMT-0600 (Central Stan... |
| 5 | GCJ | QHK | Tue Nov 25 2025 00:00:00 GMT-0600 (Central Stan... | 18.48810000 | Mr while art phone bit send because. | Sat Dec 13 2025 02:55:04 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:04 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:05.226Z*