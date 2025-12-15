# promotions

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.promotions` table represents promotional activities or campaigns within a business, explicitly detailing their attributes such as the promotion name, type, discount specifications, conditions, timeline, and status. It independently maintains information relevant to marketing efforts, as there are no direct foreign key relationships connecting it to other tables. Serving as a key component in the data model, it manages promotional details and allows for the prioritization and life cycle tracking of individual promotions through its various attributes.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| promotion_id | integer | NO | This column uniquely identifies each promotion in a sequential order. Purpose unclear from available data. |
| promotion_name | character varying | NO | Purpose unclear from available data. The values appear to be sentence fragments related to various actions or themes, but their specific business context or significance is not evident. |
| promotion_type | character varying | YES | Purpose unclear from available data. |
| discount_type | character varying | YES | Purpose unclear from available data. |
| discount_value | numeric | YES | This column represents the monetary value of the discount applied in a promotional offer. Purpose unclear from available data. |
| conditions | jsonb | YES | Purpose unclear from available data. |
| start_date | timestamp without time zone | YES | This column represents the date and time when a promotion begins. It serves as the starting point for promotional events, allowing for tracking or scheduling purposes. |
| end_date | timestamp without time zone | YES | This column indicates the date and time a particular promotion is set to end. The values suggest it records the termination of promotions, possibly aligning with Central Time, but the exact purpose is not fully clear from the available data. |
| is_active | boolean | YES | This column indicates whether a promotion is currently considered valid or in effect. The default setting suggests promotions are typically active unless specified otherwise. |
| priority | integer | YES | This column likely indicates the importance or precedence of a promotion on a scale where higher values denote higher priority, with a default setting of zero for unspecified entries. |
| created_at | timestamp without time zone | YES | The column records the date and time when a promotion was initially created, capturing this information automatically at the time the record is entered. This helps track when promotions are added to the system. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a promotion entry was last updated. The default value suggests it records the current timestamp when a record is inserted or modified. |

## Primary Key

`promotion_id`

## Indexes

- `promotions_pkey`: CREATE UNIQUE INDEX promotions_pkey ON synthetic.promotions USING btree (promotion_id)

## Sample Data

| promotion_id | promotion_name | promotion_type | discount_type | discount_value | conditions | start_date | end_date | is_active | priority | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Toward with people I perform music. Stop althou... | test | alone | 220.10 | [object Object] | Tue Nov 25 2025 09:29:43 GMT-0600 (Central Stan... | Tue May 13 2025 04:04:23 GMT-0500 (Central Dayl... | false | 5 | Sat Dec 13 2025 02:57:05 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:57:05 GMT-0600 (Central Stan... |
| 2 | Wind well pattern behind assume material. Thous... | class | green | 368.98 | [object Object] | Fri Mar 22 2024 15:26:50 GMT-0500 (Central Dayl... | Sun May 25 2025 10:05:43 GMT-0500 (Central Dayl... | true | 2 | Sat Dec 13 2025 02:57:05 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:57:05 GMT-0600 (Central Stan... |
| 3 | We drive others difference suddenly side. Lette... | large | agent | 411.10 | [object Object] | Thu Aug 21 2025 23:26:01 GMT-0500 (Central Dayl... | Thu Feb 15 2024 08:20:11 GMT-0600 (Central Stan... | false | 1 | Sat Dec 13 2025 02:57:05 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:57:05 GMT-0600 (Central Stan... |
| 4 | Think wait necessary cost cost wonder attention... | brother | energy | 712.53 | [object Object] | Sun Nov 16 2025 13:54:03 GMT-0600 (Central Stan... | Mon Jul 08 2024 23:30:27 GMT-0500 (Central Dayl... | true | 3 | Sat Dec 13 2025 02:57:05 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:57:05 GMT-0600 (Central Stan... |
| 5 | Total world with number myself others. Hot carr... | military | someone | 959.03 | [object Object] | Sat May 11 2024 18:21:24 GMT-0500 (Central Dayl... | Mon Mar 25 2024 15:18:50 GMT-0500 (Central Dayl... | false | 4 | Sat Dec 13 2025 02:57:05 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:57:05 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:43:24.933Z*