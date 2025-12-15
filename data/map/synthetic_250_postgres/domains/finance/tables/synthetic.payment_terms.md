# payment_terms

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.payment_terms" table represents the payment terms associated with transactions, capturing important details such as term codes, term descriptions, and the conditions for discounts, reflected in columns like "term_code," "days_due," and "discount_percentage." With "term_id" as the primary key, it does not reference any other tables and is not referenced by others, suggesting it serves as a standalone resource potentially utilized by other components of the system to standardize and manage payment conditions. The table is essential for defining financial agreements, highlighted by attributes such as the percentage discount for early payment and the relevant due dates.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| term_id | integer | NO | This column represents a unique identifier for each record in the payment terms table, ensuring each payment term can be individually referenced. It sequentially assigns numbers to new entries as they are added. |
| term_code | character varying | YES | Purpose unclear from available data. |
| term_name | character varying | NO | This column represents phrases or mottos that encapsulate or describe specific payment terms or conditions in a creative or abstract manner. These entries appear to use figurative language or metaphorical expressions likely meant to convey unique aspects of various payment agreements. |
| days_due | integer | YES | This column represents the number of days within which a payment is due, after which it may be considered late. The data suggests it records varying grace periods for payments, as indicated by the different numerical values. |
| discount_percentage | numeric | YES | This column represents the percentage discount offered on payment terms within a certain context, potentially indicating the level of price reduction applicable to a transaction or agreement. The values suggest significant variability, indicating discounts can range widely for different transactions. |
| discount_days | integer | YES | This column likely represents the number of days within which a discount is available for payment, offering insights into payment term conditions. The wide range of values suggests variability in the length of time different discounts are applicable. |
| description | text | YES | This column contains miscellaneous phrases or sentences that appear to be randomly generated and do not convey clear or consistent business meaning. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column captures the date and time when a record in the payment_terms table was initially created. The default value indicates it reflects the current timestamp at the moment of record insertion, and since it's nullable, not all records may have an assigned timestamp. |
| updated_at | timestamp without time zone | YES | This column records the last time each entry in the payment terms was modified. It ensures that any changes to payment terms are tracked with a precise timestamp. |

## Primary Key

`term_id`

## Indexes

- `payment_terms_pkey`: CREATE UNIQUE INDEX payment_terms_pkey ON synthetic.payment_terms USING btree (term_id)
- `payment_terms_term_code_key`: CREATE UNIQUE INDEX payment_terms_term_code_key ON synthetic.payment_terms USING btree (term_code)

## Sample Data

| term_id | term_code | term_name | days_due | discount_percentage | discount_days | description | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | VPDSKVIXLP | Building mouth song. Magazine nature force fire... | 23 | 74.36 | 7 | Degree peace your dark. Benefit long cup fire. | Sat Dec 13 2025 02:55:30 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:30 GMT-0600 (Central Stan... |
| 2 | VWYAOYKNQE | Economic reflect day individual law. His record... | 19 | 52.25 | 532 | Note nature draw cultural at bad anyone. Receiv... | Sat Dec 13 2025 02:55:30 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:30 GMT-0600 (Central Stan... |
| 3 | TLVJXGHBYC | Represent rule strategy his. Again rise game po... | 1 | 37.50 | 210 | Design share wind room cold cover option. Laugh... | Sat Dec 13 2025 02:55:30 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:30 GMT-0600 (Central Stan... |
| 4 | SFFDJAYNGZ | Congress third artist pick successful share. Pa... | 23 | 80.43 | 418 | Own happy rather skill response give theory. Co... | Sat Dec 13 2025 02:55:30 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:30 GMT-0600 (Central Stan... |
| 5 | HQXIRRYDAZ | Challenge management state seat itself yourself... | 12 | 10.66 | 436 | Past sister impact. Much firm myself affect cal... | Sat Dec 13 2025 02:55:30 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:30 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:21.083Z*