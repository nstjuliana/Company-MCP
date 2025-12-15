# cart_items

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.cart_items` table represents individual items within a customer's shopping cart, where each row corresponds to a specific product variant added to a cart. Key columns include `cart_item_id` as the primary key, `cart_id` linking to a cart, `product_id` and `variant_id` identifying the product details, and `quantity` and `unit_price` capturing the purchase specifics. This table plays a central role in e-commerce operations by cataloging customer selections and providing pricing details for cart management and order processing.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| cart_item_id | integer | NO | This column uniquely identifies each item added to a cart with a sequential integer. Each value represents a distinct entry and is generated automatically as new items are added. |
| cart_id | integer | NO | This column represents a unique identifier for each shopping cart within the system, ensuring that items are correctly associated with the appropriate cart. The purpose is to track and manage items that have been added to various shopping carts by different users. |
| product_id | integer | NO | This column likely represents unique identifiers for products included in customer shopping carts. Each integer corresponds to a specific product that a customer is interested in purchasing. |
| variant_id | integer | YES | This column likely represents a numeric identifier associated with specific product variants in a shopping cart. Each number corresponds to a different variant option selected by customers. |
| quantity | integer | NO | This column represents the number of items included in a customer's shopping cart for a specific line item. It is a mandatory entry that defaults to a single item per line if not otherwise specified. |
| unit_price | numeric | NO | This column represents the price per unit for items included in customer shopping carts. These prices indicate the cost assigned to individual units before the final purchase. |
| added_at | timestamp without time zone | YES | The column records the date and time when an item was added to a shopping cart. Dates and times are represented in both Central Standard and Daylight Time. |
| created_at | timestamp without time zone | YES | This column records the date and time when each item was added to the cart. It helps track cart activity chronologically, although the specific purpose or usage context is unclear from the available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when an item in the shopping cart was last updated. It reflects the most recent modification made to the cart item. |

## Primary Key

`cart_item_id`

## Foreign Keys

- `cart_id` → `synthetic.shopping_carts.cart_id`
- `product_id` → `synthetic.products.product_id`
- `variant_id` → `synthetic.product_variants.variant_id`

## Indexes

- `cart_items_pkey`: CREATE UNIQUE INDEX cart_items_pkey ON synthetic.cart_items USING btree (cart_item_id)

## Sample Data

| cart_item_id | cart_id | product_id | variant_id | quantity | unit_price | added_at | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 49 | 43 | 22 | 170 | 61521.30 | Sat Feb 22 2025 11:17:27 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:25 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:25 GMT-0600 (Central Stan... |
| 2 | 24 | 28 | 13 | 508 | 63580.88 | Sat Sep 27 2025 03:44:25 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:56:25 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:25 GMT-0600 (Central Stan... |
| 3 | 5 | 35 | 14 | 294 | 26588.99 | Mon Mar 18 2024 14:10:01 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:56:25 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:25 GMT-0600 (Central Stan... |
| 4 | 20 | 37 | 26 | 823 | 22666.01 | Sat Jun 15 2024 10:23:04 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:56:25 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:25 GMT-0600 (Central Stan... |
| 5 | 48 | 6 | 46 | 864 | 57861.51 | Fri Jun 13 2025 17:51:06 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:56:25 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:25 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:20.400Z*