# supplier_products

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.supplier_products" table is designed to represent the association between suppliers and their respective products, likely detailing the inventory or offerings managed by suppliers. As indicated by its primary key, "supplier_product_id," this table uniquely identifies each supplier-product relationship. Though no specific column details or data are available, its role likely involves facilitating the linkage of suppliers to product data, possibly referencing a table of undefined structure.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| supplier_product_id | integer | NO | This column uniquely identifies each product provided by suppliers within the system. It serves as a primary key for linking suppliers to their respective products. |
| supplier_id | integer | NO | This column identifies the unique identifier for each supplier associated with the products, serving as a reference to distinguish between different suppliers. |
| product_id | integer | NO | This column uniquely identifies products in relation to their suppliers. Purpose unclear from available data. |
| supplier_sku | character varying | YES | The purpose of this column is unclear from available data. |
| unit_cost | numeric | YES | This column likely represents the cost associated with a single unit of a product supplied by a vendor. It may be used for pricing analysis or inventory cost management, although specific applications are unclear from the available data. |
| minimum_order_qty | integer | YES | Specifies the smallest quantity of a product that can be ordered from a supplier. If not explicitly set, it defaults to a quantity of one. |
| lead_time_days | integer | YES | This column likely represents the estimated number of days from order placement to delivery for products supplied. Purpose unclear from available data. |
| is_preferred | boolean | YES | Indicates whether a supplier's product is marked as preferred. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a supplier product entry is created. It helps in tracking the addition of new products to the supplier list. |
| updated_at | timestamp without time zone | YES | This column records the date and time of the most recent update to the supplier product information. It helps track changes to ensure data remains current and accurate. |

## Primary Key

`supplier_product_id`

## Foreign Keys

- `supplier_id` → `synthetic.suppliers.supplier_id`

## Indexes

- `supplier_products_pkey`: CREATE UNIQUE INDEX supplier_products_pkey ON synthetic.supplier_products USING btree (supplier_product_id)

*Generated at: 2025-12-14T23:42:47.194Z*