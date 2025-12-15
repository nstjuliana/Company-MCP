# landing_page_conversions

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.landing_page_conversions` table records interactions where website visitors convert by performing a predefined action on a landing page, such as a purchase or signup. Key columns such as `page_id` and `visitor_id` indicate the specific page and visitor involved in the conversion event, and the `conversion_type`, `conversion_value`, and timestamps provide further details on the context and timing of these conversions. The table's primary role in the data model is to track conversion metrics linked to marketing efforts, offering insights into the effectiveness of campaigns, as denoted by columns like `source`, `medium`, and `campaign`.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| conversion_id | integer | NO | This column uniquely identifies each record of a conversion on a landing page. Each value is a distinct sequence number that indicates the order of conversions. |
| page_id | integer | NO | This column represents unique identifiers for different landing pages involved in conversion tracking activities. Each integer associates a distinct landing page with conversion data. |
| visitor_id | character varying | YES | Purpose unclear from available data. The sample values resemble textual information that doesn't provide insights into its specific function. |
| converted_at | timestamp without time zone | YES | This column captures the date and time when a conversion event occurred on a landing page, reflecting customer interactions and engagement changes. The timestamps indicate various moments in Central Time, showing both standard and daylight saving periods. |
| conversion_type | character varying | YES | Purpose unclear from available data. The sample values suggest a range of arbitrary phrases and sentences that do not indicate a specific business context or conversion type. |
| conversion_value | numeric | YES | This column represents the monetary value generated from individual conversions on a landing page. It reflects the financial worth of items or services purchased or actions taken that result in revenue, expressed as a numeric amount. |
| source | character varying | YES | Purpose unclear from available data. The variety in sample values suggests diverse textual data, possibly representing user comments or feedback during landing page interactions. |
| medium | character varying | YES | Purpose unclear from available data. |
| campaign | character varying | YES | This column represents a descriptor or title for different advertising or promotional campaigns related to website landing page activities. The specific purpose or detail conveyed by each campaign entry is unclear from the available data, as the values appear abstract or metaphorical. |
| created_at | timestamp without time zone | YES | This column records the date and time when a conversion event occurred on a landing page. The events are likely timestamped automatically at the moment they happen, reflecting Central Standard Time. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a landing page conversion record was most recently updated. The timestamp reflects the Central Standard Time zone, but the specific purpose of these updates is unclear from the available data. |

## Primary Key

`conversion_id`

## Foreign Keys

- `page_id` → `synthetic.landing_pages.page_id`

## Indexes

- `landing_page_conversions_pkey`: CREATE UNIQUE INDEX landing_page_conversions_pkey ON synthetic.landing_page_conversions USING btree (conversion_id)

## Sample Data

| conversion_id | page_id | visitor_id | converted_at | conversion_type | conversion_value | source | medium | campaign | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 43 | Hard move especially partner stage prevent whos... | Thu Feb 13 2025 09:35:57 GMT-0600 (Central Stan... | Hair half debate leg direction though young. To... | 945.19 | Itself begin its of yard take sport center. Sea... | Keep blood direction sure. Total claim outside ... | Measure whatever who go visit. Mother owner als... | Sat Dec 13 2025 03:14:19 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:19 GMT-0600 (Central Stan... |
| 2 | 49 | Mind democratic industry second cost station. B... | Thu Aug 29 2024 12:37:42 GMT-0500 (Central Dayl... | Nothing create new develop professor nothing gu... | 550.10 | Change name adult parent line common night. | Moment arm its able painting voice let.
Western... | Red machine future must we above full. Field am... | Sat Dec 13 2025 03:14:19 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:19 GMT-0600 (Central Stan... |
| 3 | 30 | Trade certainly main history production. | Mon Jun 02 2025 20:59:15 GMT-0500 (Central Dayl... | Scientist ground prove miss chair throw. Worry ... | 88.06 | Child eat agree sister. Process television give... | Open follow run movie. Three own teacher tend s... | Year six run. Role produce yeah through. Cultur... | Sat Dec 13 2025 03:14:19 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:19 GMT-0600 (Central Stan... |
| 4 | 17 | Finish size add recognize. Deep wide product ac... | Tue Jul 30 2024 23:33:20 GMT-0500 (Central Dayl... | Job forget fly continue make artist of Mr. More... | 323.27 | Star dream star to board born than. Protect hun... | Outside seek year simple. | Training image black through. Oil sometimes off... | Sat Dec 13 2025 03:14:19 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:19 GMT-0600 (Central Stan... |
| 5 | 50 | Environment economy statement see nor some. Beh... | Thu Mar 20 2025 15:05:29 GMT-0500 (Central Dayl... | Method team population live land former. Hard i... | 404.18 | Civil wife campaign begin enter good truth. | Employee leave it position option foreign owner... | Issue hot parent reach develop upon. Quite nort... | Sat Dec 13 2025 03:14:19 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:19 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:43:25.343Z*