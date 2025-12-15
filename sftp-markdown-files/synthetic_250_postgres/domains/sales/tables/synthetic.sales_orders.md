# sales_orders

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.sales_orders` table represents the details of sales orders within the synthetic_250_postgres database, capturing essential attributes such as order dates, billing and shipping information, and financial details like subtotal, discount, tax, and grand total. It is linked via foreign keys to undefined tables, possibly denoting related entities such as customers or product listings, and serves as a central repository for tracking and managing sales orders within the business. Despite the absence of foreign key details, the table's primary key, `sales_order_id`, uniquely identifies each order, and columns like `order_number`, `account_id`, and `status` facilitate business operations and reporting.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| sales_order_id | integer | NO | This column uniquely identifies each sales order within the system, ensuring that every transaction is distinct and traceable. Each value represents a new and sequential order entry in the sales process. |
| order_number | character varying | NO | This column represents unique identifiers assigned to each sales order processed by the company. These identifiers help track and manage individual transactions within the sales operation. |
| quote_id | integer | YES | This field likely represents a unique identifier for quotes associated with sales orders, possibly linking orders to their respective quotes for pricing or terms reference. Purpose unclear from available data. |
| opportunity_id | integer | YES | Represents a numeric identifier linking sales orders to specific sales opportunities. Allows for the association of sales transactions with potential business deals. |
| account_id | integer | YES | This column likely represents unique identifiers for customer accounts involved in sales orders, allowing linkage to specific customers. Purpose unclear from available data. |
| contact_id | integer | YES | Purpose unclear from available data. |
| order_date | date | NO | This column records the specific date on which each sales order was placed, with values reflecting different time zones according to daylight saving time changes. It is a non-nullable field, ensuring that every sales order is associated with a distinct order date. |
| status | character varying | YES | This column indicates the current state of a sales order, with possible statuses including "active," "inactive," and "pending." It captures whether the order is actively being processed, not currently active, or awaiting further action. |
| subtotal | numeric | YES | This column represents the pre-tax total monetary value of items listed in a sales order. It accounts for the aggregate cost prior to any additional charges or discounts. |
| discount | numeric | YES | This column represents the monetary amount deducted from the original sales order price, allowing buyers to pay a lesser amount for their purchase. The values indicate discounts applied to various sales orders, with amounts ranging from small to substantial. |
| tax | numeric | YES | This column likely represents the monetary amount of tax applied to sales orders. The values indicate variable tax amounts that are associated with different sales transactions. |
| shipping | numeric | YES | This column likely represents the shipping cost associated with sales orders, reflecting a financial value that varies for each transaction. The purpose is to capture shipping expenses, which are often a component of the total order cost. |
| grand_total | numeric | YES | This column represents the final total amount for sales orders, including any applicable taxes, fees, or discounts. The amounts are presented in a monetary format, reflecting the overall charge for each order. |
| billing_address | text | YES | This column contains the complete mailing addresses associated with the billing details for sales orders, including street addresses, city names, state abbreviations, and postal codes. These addresses indicate the locations to which invoices or billing information are sent for sales transactions. |
| shipping_address | text | YES | This column captures the full shipping address for orders, reflecting diverse locations, including street addresses, suites or units, and sometimes military or diplomatic post office boxes. The presence of state abbreviations and ZIP codes indicates U.S.-based delivery destinations. |
| owner_id | integer | YES | This column likely represents the identifier for individuals responsible for specific sales orders, indicating who manages or owns each order within the sales system. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column captures the date and time when a sales order was initially recorded or created in the system. Purpose unclear from available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a sales order was last updated. It captures changes in the order's status or details, reflecting the most recent activity. |

## Primary Key

`sales_order_id`

## Foreign Keys

- `account_id` → `synthetic.accounts.account_id`
- `contact_id` → `synthetic.contacts.contact_id`
- `opportunity_id` → `synthetic.opportunities.opportunity_id`
- `quote_id` → `synthetic.quotes.quote_id`

## Indexes

- `sales_orders_order_number_key`: CREATE UNIQUE INDEX sales_orders_order_number_key ON synthetic.sales_orders USING btree (order_number)
- `sales_orders_pkey`: CREATE UNIQUE INDEX sales_orders_pkey ON synthetic.sales_orders USING btree (sales_order_id)

## Sample Data

| sales_order_id | order_number | quote_id | opportunity_id | account_id | contact_id | order_date | status | subtotal | discount | tax | shipping | grand_total | billing_address | shipping_address | owner_id | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 512090181749731 | 4 | 28 | 85 | null | Sun Mar 10 2024 00:00:00 GMT-0600 (Central Stan... | active | 236.77 | 260.99 | 315.01 | 800.82 | 700.73 | 36098 Sarah Center Suite 045, Reidville, RI 86275 | 05975 Jose Spring Suite 594, North Allen, ME 21853 | 754 | Sat Dec 13 2025 03:18:31 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:31 GMT-0600 (Central Stan... |
| 2 | 084182865490787 | 21 | 21 | 58 | null | Wed Apr 17 2024 00:00:00 GMT-0500 (Central Dayl... | inactive | 233.61 | 943.55 | 136.11 | 770.15 | 108.97 | 1519 Audrey Mount Suite 770, Claytonshire, MS 8... | PSC 6169, Box 4135, APO AE 23023 | 109 | Sat Dec 13 2025 03:18:31 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:31 GMT-0600 (Central Stan... |
| 3 | 848369559582770 | 11 | 29 | 60 | null | Thu May 01 2025 00:00:00 GMT-0500 (Central Dayl... | inactive | 406.51 | 535.92 | 964.63 | 207.64 | 308.31 | 69156 Harper Mews, Port Alexandraburgh, NM 56169 | 35120 Diaz Radial, Silvamouth, WI 62017 | 272 | Sat Dec 13 2025 03:18:31 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:31 GMT-0600 (Central Stan... |
| 4 | 349438563375984 | 8 | 6 | 21 | null | Sun Feb 16 2025 00:00:00 GMT-0600 (Central Stan... | pending | 304.21 | 704.70 | 603.30 | 215.02 | 856.57 | 870 Ann Corners Apt. 133, Bishopburgh, IL 26982 | 41707 Duane Parkway, Ingramchester, IA 32703 | 152 | Sat Dec 13 2025 03:18:31 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:31 GMT-0600 (Central Stan... |
| 5 | 879081322082204 | 6 | 46 | 32 | null | Fri Jul 05 2024 00:00:00 GMT-0500 (Central Dayl... | inactive | 396.24 | 48.95 | 298.84 | 820.09 | 173.87 | 1978 Robert Glens, Thomaston, AS 38631 | Unit 5990 Box 0284, DPO AE 17948 | 975 | Sat Dec 13 2025 03:18:31 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:18:31 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:42:02.441Z*