# gift_cards

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The synthetic.gift_cards table represents the business entity of gift card transactions, capturing essential details such as the unique gift card identifier (gift_card_id), card code, balances (initial and current), currency, and customer-related information (purchaser_customer_id, recipient_email, message). This table also tracks the lifecycle of a gift card with timestamps for creation and updates, alongside the purchase and expiry dates, and its activation status (is_active). As the primary key is gift_card_id and there are no foreign keys defined, this table primarily functions to manage gift card data independently within the synthetic_250_postgres database.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| gift_card_id | integer | NO | Represents an identifier for gift cards, ensuring each gift card is uniquely recognized within the system. Purpose unclear from available data. |
| card_code | character varying | NO | This column represents unique identification codes assigned to gift cards. The codes appear to be alphanumeric and consistently have a fixed length, indicating a standardized format for card identification. |
| initial_balance | numeric | NO | This column represents the initial monetary value assigned to gift cards at the time of issuance. Purpose unclear from available data. |
| current_balance | numeric | NO | This column represents the remaining monetary amount available on a gift card for use. The values indicate the current spending capacity associated with each gift card in the system. |
| currency | character varying | YES | This column specifies the type of currency associated with the gift cards, with examples including Japanese Yen, US Dollar, Euro, British Pound, and Canadian Dollar. It defaults to US Dollar if not explicitly stated. |
| purchaser_customer_id | integer | YES | This column represents the unique identifier for customers who purchase gift cards. The purpose of this identifier is to link gift card transactions to specific customer accounts, allowing for tracking and analysis of purchasing behavior. |
| recipient_email | character varying | YES | This column contains the email addresses of individuals who are designated to receive gift cards. Purpose unclear from available data. |
| message | text | YES | Purpose unclear from available data. The entries appear to contain fragmented sentences or abstract phrases without a clear cohesive theme. |
| purchase_date | timestamp without time zone | YES | This column captures the date and time when a gift card was purchased, allowing tracking of transactions over different time periods, particularly around when they occur in relation to Central Standard and Central Daylight Time. Purpose unclear from available data. |
| expiry_date | timestamp without time zone | YES | The column records the date and time when a gift card is no longer valid for use. The values indicate expiration dates for gift cards across different years, acknowledging potential variations in expiration policies. |
| is_active | boolean | YES | Indicates whether a gift card is currently valid and can be used. Default is that all gift cards are active unless specified otherwise. |
| created_at | timestamp without time zone | YES | This column records the date and time when a gift card entry is created, indicating the initiation of each gift card record. The values suggest that these timestamps are automatically set at the moment of creation, typically reflecting the current time. |
| updated_at | timestamp without time zone | YES | This column captures the most recent date and time when the record was updated. The default setting suggests updates are automatically timestamped upon modification, but the specific business context for updates is unclear from the available data. |

## Primary Key

`gift_card_id`

## Foreign Keys

- `purchaser_customer_id` → `synthetic.customers.customer_id`

## Indexes

- `gift_cards_card_code_key`: CREATE UNIQUE INDEX gift_cards_card_code_key ON synthetic.gift_cards USING btree (card_code)
- `gift_cards_pkey`: CREATE UNIQUE INDEX gift_cards_pkey ON synthetic.gift_cards USING btree (gift_card_id)

## Sample Data

| gift_card_id | card_code | initial_balance | current_balance | currency | purchaser_customer_id | recipient_email | message | purchase_date | expiry_date | is_active | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | IKXUSJQRXH | 389.94 | 320.04 | JPY | 21 | ttyler@example.net | Anything medical vote down Republican water dis... | Sun Jan 21 2024 05:09:46 GMT-0600 (Central Stan... | Mon Nov 17 2025 11:34:06 GMT-0600 (Central Stan... | false | Sat Dec 13 2025 02:56:46 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:46 GMT-0600 (Central Stan... |
| 2 | HZEUSLNFKM | 375.51 | 827.74 | USD | 4 | sanderselizabeth@example.net | Grow usually art no think sign big perhaps. Reg... | Wed May 01 2024 19:22:32 GMT-0500 (Central Dayl... | Mon Jan 27 2025 15:22:48 GMT-0600 (Central Stan... | true | Sat Dec 13 2025 02:56:46 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:46 GMT-0600 (Central Stan... |
| 3 | KJMRAXBJHP | 239.62 | 597.00 | EUR | 32 | damonyoder@example.com | Here environmental expert organization. Town ad... | Mon Aug 04 2025 21:22:25 GMT-0500 (Central Dayl... | Fri Sep 20 2024 11:42:12 GMT-0500 (Central Dayl... | false | Sat Dec 13 2025 02:56:46 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:46 GMT-0600 (Central Stan... |
| 4 | TAZOZLMHKJ | 949.36 | 269.29 | GBP | 30 | jared39@example.com | See statement forward different teach managemen... | Sun Jun 09 2024 10:01:09 GMT-0500 (Central Dayl... | Sun Oct 26 2025 20:47:50 GMT-0500 (Central Dayl... | false | Sat Dec 13 2025 02:56:46 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:46 GMT-0600 (Central Stan... |
| 5 | ELPEIYINZL | 65.46 | 28.91 | EUR | 2 | benjaminlambert@example.org | Suffer appear knowledge worry. Unit light some ... | Thu Jul 10 2025 20:21:21 GMT-0500 (Central Dayl... | Fri May 17 2024 05:08:52 GMT-0500 (Central Dayl... | false | Sat Dec 13 2025 02:56:46 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:46 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:16.626Z*