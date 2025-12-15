# quote_lines

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.quote_lines` table represents individual line items within a quote, each identified by a unique `quote_line_id`. It includes details such as the associated `quote_id`, `product_id`, product name, quantity, unit price, discount, and line total, indicating the financial specifics of each quoted item. This table plays a critical role in detailing the components of a quote, contributing to the broader structure of quote management, with a foreign key relationship to another undefined table.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| quote_line_id | integer | NO | This column represents a unique identifier assigned to each individual line item within a quote, ensuring each line is distinct and can be referenced separately. It is incrementally assigned with each new line item added to a quote. |
| quote_id | integer | NO | This column likely represents unique identifiers associated with specific quotes in a transactional or proposal system. Each value corresponds to a distinct quote entry within the dataset. |
| product_id | integer | YES | This column likely represents unique identifiers assigned to various products involved in quoting processes. The purpose or nature of these products remains unclear from the available data. |
| product_name | character varying | YES | This column represents descriptive phrases or titles that seem to summarize or highlight abstract or conceptual content related to a wide array of subjects or entities. The purpose is unclear from the available data, as the provided phrases are varied and lack a cohesive theme. |
| quantity | numeric | NO | This column represents the amount of a particular item or service quoted, expressed in units or currency. Purpose unclear from available data. |
| unit_price | numeric | NO | This column represents the price per unit associated with each line item in a quotation or proposal. It reflects the monetary cost assigned to single units of goods or services that are being quoted. |
| discount | numeric | YES | This column represents the monetary amount reduced from the original price of each quoted item or service, potentially indicating promotional or negotiated savings. Purpose unclear from available data. |
| line_total | numeric | YES | This column represents the total monetary amount associated with each line item within a quotation. Purpose unclear from available data. |
| description | text | YES | This column contains textual descriptions or statements that appear to relate to a variety of topics, including business, personal experiences, or abstract concepts. Purpose unclear from available data. |
| sort_order | integer | YES | This column likely specifies the sequence in which individual items or entries are organized within a quote, with higher values indicating later positions. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a quote line entry was created. It reflects the creation timestamp in a consistent manner, but its specific business purpose is unclear from the available data. |
| updated_at | timestamp without time zone | YES | This column likely records the date and time when a record in the quote_lines table was last updated, with current timestamps used by default. This timestamp indicates the most recent activity or modification made to a quote line entry. |

## Primary Key

`quote_line_id`

## Foreign Keys

- `quote_id` → `synthetic.quotes.quote_id`

## Indexes

- `quote_lines_pkey`: CREATE UNIQUE INDEX quote_lines_pkey ON synthetic.quote_lines USING btree (quote_line_id)

## Sample Data

| quote_line_id | quote_id | product_id | product_name | quantity | unit_price | discount | line_total | description | sort_order | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 45 | 887 | Scientist race add lot. Instead thousand newspa... | 132.69 | 1470.97 | 322.10 | 247.55 | Four candidate raise sort. | 864 | Sat Dec 13 2025 03:18:28 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:28 GMT-0600 (Central Stan... |
| 2 | 44 | 403 | Billion book property throughout them great imp... | 489.46 | 5778.48 | 268.72 | 414.23 | Service without choose involve establish risk. ... | 463 | Sat Dec 13 2025 03:18:28 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:28 GMT-0600 (Central Stan... |
| 3 | 5 | 649 | Long generation threat represent couple. Amount... | 794.60 | 7691.15 | 402.85 | 749.80 | Example media physical than already. Least bag ... | 712 | Sat Dec 13 2025 03:18:28 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:28 GMT-0600 (Central Stan... |
| 4 | 24 | 466 | Sign head paper father can both meeting. Respon... | 950.25 | 3279.62 | 2.47 | 774.14 | Common air nothing debate require increase argu... | 751 | Sat Dec 13 2025 03:18:28 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:28 GMT-0600 (Central Stan... |
| 5 | 6 | 749 | Ahead girl skill describe. Road message near al... | 972.15 | 6352.06 | 697.29 | 850.11 | Bad remember company right. Eight seem pattern ... | 815 | Sat Dec 13 2025 03:18:28 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:28 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:57.018Z*