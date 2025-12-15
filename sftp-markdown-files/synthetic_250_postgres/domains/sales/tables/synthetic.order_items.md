# order_items

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.order_items" table is designed to represent individual items associated with orders, uniquely identified by the "order_item_id" primary key. It establishes relationships with at least three other entities, as inferred from foreign key references, although the specific entities are undefined in the provided data. This table likely serves as a junction table in the data model, detailing the components of an order within the synthetic_250_postgres database.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| order_item_id | integer | NO | This column uniquely identifies each item within an order, ensuring that every entry is distinct and traceable in the context of an order's details. |
| order_id | integer | NO | Unique identifier for an individual order associated with items in a transaction. |
| product_id | integer | NO | This column identifies the specific product associated with each order item in the system, ensuring accurate tracking and management of products within customer orders. Purpose unclear from available data. |
| variant_id | integer | YES | Purpose unclear from available data. |
| product_name | character varying | YES | This column likely represents the name or title of a product in an order, but its specific role within the order is unclear from the available data. |
| sku | character varying | YES | Purpose unclear from available data. |
| quantity | integer | NO | This column records the number of units of a specific item included in a single order. It is a mandatory field and does not have a default value. |
| unit_price | numeric | NO | Represents the cost assigned to a single unit of an item within an order in the order_items table. |
| discount_amount | numeric | YES | This column represents the monetary amount deducted from the original price in the form of a discount for an order item. The value can be absent, indicating no discount was applied. |
| tax_amount | numeric | YES | This column represents the monetary amount collected as tax for each order item in a transactional context. The amount can be null, implying that tax information might be optional or not applicable in certain cases. |
| line_total | numeric | NO | Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when an order item entry is created. It defaults to the current timestamp, indicating the moment of record entry. |
| updated_at | timestamp without time zone | YES | Records the date and time when each order item record was last modified. This may include updates to any details within the order item. |

## Primary Key

`order_item_id`

## Foreign Keys

- `order_id` → `synthetic.orders.order_id`
- `product_id` → `synthetic.products.product_id`
- `variant_id` → `synthetic.product_variants.variant_id`

## Indexes

- `order_items_pkey`: CREATE UNIQUE INDEX order_items_pkey ON synthetic.order_items USING btree (order_item_id)

*Generated at: 2025-12-14T23:41:57.098Z*