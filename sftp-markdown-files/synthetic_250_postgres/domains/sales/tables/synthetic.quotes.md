# quotes

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.quotes" table represents a business entity for managing sales quotes, capturing details such as quote numbers, associated accounts, opportunity IDs, and financial metrics like subtotal, discount, and grand total. It is likely connected to other tables through foreign keys referencing entities like opportunities and accounts, though specific relationships are undefined. The table serves as a critical component in the sales order process within the database, providing comprehensive information about individual sales quotes along with their current statuses and associated timestamps.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| quote_id | integer | NO | This column uniquely identifies each individual record within the table, sequentially representing distinct quote entries. Purpose unclear from available data. |
| quote_number | character varying | YES | This column likely represents a unique identifier for individual quotes, as indicated by the diversity of the provided numeric sample values. Purpose unclear from available data beyond identification. |
| opportunity_id | integer | YES | This column likely represents unique identifiers associated with potential business deals or sales opportunities. Purpose unclear from available data. |
| account_id | integer | YES | This column likely stores identifiers for user accounts associated with quotes in the system. Purpose unclear from available data. |
| contact_id | integer | YES | Purpose unclear from available data. |
| quote_name | character varying | YES | This column appears to store brief narrative or conceptual expressions, possibly representing slogans, summaries, or titles related to strategic, cultural, or technological themes. The purpose is unclear from the available data. |
| status | character varying | YES | This column represents the current lifecycle stage of a quote, indicating whether it is awaiting action, currently in use, or not active, with "draft" being the initial status if unspecified. |
| expiration_date | date | YES | This column likely contains dates by which specific actions, agreements, or offers associated with entries in the "synthetic.quotes" table are no longer valid or are due to expire. The dates suggest a future timeframe, indicating deadlines or expiration periods relevant to the table's entries. |
| subtotal | numeric | YES | This column represents the total value of items or services before any additional charges such as taxes or discounts are applied. The values indicate the initial aggregation of costs for quotes provided within the system. |
| discount | numeric | YES | This column represents the monetary amount discounted from a total quoted price or service cost, as evidenced by the sample values. It indicates deductions applied, potentially as part of promotions or negotiated deals. |
| tax | numeric | YES | This column represents the monetary amount of tax associated with a financial transaction or quote. The values indicate varying amounts, suggesting the tax is calculated based on differing transaction amounts or conditions. |
| shipping | numeric | YES | This column likely represents the cost associated with the shipping of goods or services in a numeric form. The provided sample values suggest a range of shipping costs that vary depending on specific circumstances or corresponding entities. |
| grand_total | numeric | YES | This column represents the total monetary value associated with individual quotes. Purpose unclear from available data. |
| billing_address | text | YES | This column stores the complete billing address of customers, including street address, city, state, and ZIP code. It serves to identify the location associated with customer billing for transactions or services. |
| shipping_address | text | YES | This column contains postal addresses that are used for the shipment of goods associated with individual quotes. The addresses include street information, city names, state abbreviations, and postal codes, indicating diverse locations across different states. |
| description | text | YES | This column seems to capture abstract or thematic phrases likely related to titles or summaries of creative or artistic endeavors. The content suggests a focus on various subjects or activities, possibly indicative of descriptive text about quotes or expressions used in different contexts. |
| owner_id | integer | YES | This column likely identifies the individual or entity responsible for or associated with a quote. The purpose is unclear from the available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a quote was created within the system. The purpose of tracking this information is unclear from the available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when information in the quotes table was last updated. It allows for tracking changes or modifications made to each record. |

## Primary Key

`quote_id`

## Foreign Keys

- `account_id` → `synthetic.accounts.account_id`
- `contact_id` → `synthetic.contacts.contact_id`
- `opportunity_id` → `synthetic.opportunities.opportunity_id`

## Indexes

- `quotes_pkey`: CREATE UNIQUE INDEX quotes_pkey ON synthetic.quotes USING btree (quote_id)
- `quotes_quote_number_key`: CREATE UNIQUE INDEX quotes_quote_number_key ON synthetic.quotes USING btree (quote_number)

## Sample Data

| quote_id | quote_number | opportunity_id | account_id | contact_id | quote_name | status | expiration_date | subtotal | discount | tax | shipping | grand_total | billing_address | shipping_address | description | owner_id | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 511133010753502 | 1 | 3 | null | Window everything moment simply explain rule. C... | pending | Sun Jul 21 2024 00:00:00 GMT-0500 (Central Dayl... | 722.19 | 535.74 | 286.69 | 502.22 | 697.86 | 70858 Benjamin Ford, Williamsonville, IN 15129 | 60809 Sean Landing, New Jessemouth, MP 71732 | Research name skill sound music. Know everythin... | 441 | Sat Dec 13 2025 03:18:24 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:24 GMT-0600 (Central Stan... |
| 2 | 811337049462455 | 12 | 14 | null | Keep major worker. Fly discussion green. | active | Mon May 20 2024 00:00:00 GMT-0500 (Central Dayl... | 524.39 | 240.97 | 619.78 | 252.42 | 354.44 | 4153 Julia Mission Apt. 666, Brownfurt, IL 31031 | 611 Rogers Forges, New Johnborough, VA 15454 | Rate discover manage baby letter. Magazine piec... | 815 | Sat Dec 13 2025 03:18:24 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:24 GMT-0600 (Central Stan... |
| 3 | 920045820721624 | 26 | 11 | null | Focus force region your season. Sister station ... | inactive | Mon Jun 17 2024 00:00:00 GMT-0500 (Central Dayl... | 959.30 | 459.00 | 243.21 | 697.24 | 299.97 | 58067 Ashley Ville Suite 465, Apriltown, AR 02277 | 04645 Hanson Lights Apt. 487, Georgechester, AK... | Painting teacher how care kitchen art whom morn... | 848 | Sat Dec 13 2025 03:18:24 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:24 GMT-0600 (Central Stan... |
| 4 | 904315071741647 | 6 | 84 | null | There stand strategy big always while. Since ch... | pending | Fri Sep 05 2025 00:00:00 GMT-0500 (Central Dayl... | 759.59 | 93.50 | 379.26 | 552.70 | 56.11 | 2447 Kimberly Mount, Tiffanyland, VT 35386 | PSC 4894, Box 0094, APO AA 45033 | Today doctor wife oil popular. Night successful... | 10 | Sat Dec 13 2025 03:18:24 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:24 GMT-0600 (Central Stan... |
| 5 | 737805342519187 | 45 | 22 | null | Camera Mrs land kid southern it. Send realize b... | active | Sat Nov 30 2024 00:00:00 GMT-0600 (Central Stan... | 499.86 | 433.91 | 784.38 | 565.86 | 857.96 | 7714 Michael Mission Suite 025, Lake Christophe... | 998 Ellis Islands, West Pedro, SC 28874 | Wear environment second especially from. Rememb... | 98 | Sat Dec 13 2025 03:18:24 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:24 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:57.144Z*