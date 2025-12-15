# shopping_carts

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "shopping_carts" table in the "synthetic_250_postgres" database represents the e-commerce shopping carts used by customers. It tracks attributes such as the customer ID, session details, monetary totals (subtotal, discount, tax), and timestamps of last activity, creation, and update. Although there are undefined foreign key relationships, the presence of "customer_id" suggests interaction with a customer-related table, highlighting this table's central role in capturing the transactional context of a shopping cart within an online retail system.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| cart_id | integer | NO | This column represents the unique identifier for individual shopping carts within the system. Each number in the sequence distinguishes a separate shopping cart. |
| customer_id | integer | YES | This column likely represents a unique identifier for customers associated with various shopping carts. Purpose unclear from available data. |
| session_id | character varying | YES | Purpose unclear from available data. |
| currency | character varying | YES | This column represents the type of currency used in transactions within shopping carts. It defaults to US dollars but can include other currencies such as euros, Japanese yen, Canadian dollars, and British pounds. |
| subtotal | numeric | YES | This column represents the total monetary amount of items in a shopping cart before any discounts or taxes are applied. The values suggest typical shopping cart totals, reflecting varied spending patterns of customers. |
| discount_total | numeric | YES | This column likely represents the total discount applied to a customer's shopping cart during a transaction. The figures suggest monetary amounts, indicating cost savings given in various transaction entries. |
| tax_total | numeric | YES | This column represents the total tax amount associated with a shopping cart transaction. The values indicate the tax applied to purchases, which can vary widely, suggesting diverse cart values and potential tax rates. |
| last_activity | timestamp without time zone | YES | This column records the date and time of the most recent interaction or update associated with a shopping cart. It helps track user activity within the shopping cart over time. |
| created_at | timestamp without time zone | YES | This column records the date and time when a shopping cart was created. The value defaults to the current system timestamp at the moment of creation. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a shopping cart was last modified or updated. It automatically captures the current timestamp when a change occurs, indicating the most recent activity within the cart. |

## Primary Key

`cart_id`

## Foreign Keys

- `customer_id` → `synthetic.customers.customer_id`

## Indexes

- `shopping_carts_pkey`: CREATE UNIQUE INDEX shopping_carts_pkey ON synthetic.shopping_carts USING btree (cart_id)

## Sample Data

| cart_id | customer_id | session_id | currency | subtotal | discount_total | tax_total | last_activity | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 20 | Scientist coach structure. Task which professor... | EUR | 209.84 | 981.11 | 424.81 | Wed Feb 12 2025 16:55:39 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:20 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:20 GMT-0600 (Central Stan... |
| 2 | 49 | White born plan cut book. Mind major about road... | USD | 77.74 | 774.69 | 757.33 | Thu Mar 27 2025 13:03:44 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:56:20 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:20 GMT-0600 (Central Stan... |
| 3 | 3 | Size will sport pretty. Pull build wait gun. | EUR | 107.82 | 793.06 | 513.48 | Wed Oct 22 2025 16:15:34 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:56:20 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:20 GMT-0600 (Central Stan... |
| 4 | 4 | Mind want ok everything. Necessary bank never g... | JPY | 118.92 | 253.01 | 66.25 | Tue Oct 21 2025 11:45:57 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:56:20 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:20 GMT-0600 (Central Stan... |
| 5 | 43 | President civil yes. | USD | 754.55 | 782.37 | 920.10 | Sun Mar 23 2025 13:11:21 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:56:20 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:20 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:30.818Z*