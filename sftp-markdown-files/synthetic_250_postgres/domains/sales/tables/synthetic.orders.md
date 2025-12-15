# orders

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.orders" table represents an entity for tracking order transactions within the database, identified uniquely by the primary key "order_id". It is designed to establish undefined relationships with other entities, likely capturing dependencies or breaking down components associated with each order. Despite the absence of concrete column details or sample data, the table likely plays a central role in handling transactional information, influencing or interfacing with other parts of the overall data model.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| order_id | integer | NO | This column uniquely identifies each order within the system, automatically generating a new identifier for every new entry to ensure no duplicates. |
| order_number | character varying | NO | This field represents the unique identifier assigned to each order in the system, ensuring that every transaction can be distinctly recognized and referenced. |
| customer_id | integer | YES | This field likely identifies a specific customer associated with an order. Purpose unclear from available data. |
| order_date | timestamp without time zone | NO | This column captures the precise date and time when an order is recorded in the system. It is automatically populated with the current date and time at the moment of order entry, ensuring accurate order tracking. |
| status | character varying | YES | Represents the current progress state of an order, with a common initial setting as pending. |
| subtotal | numeric | NO | Purpose unclear from available data. |
| discount_total | numeric | YES | The column represents the total discount amount applied to an order. It captures any reductions or special offers reducing the order's overall price, defaulting to zero if no discount is applied. |
| shipping_total | numeric | YES | Represents the total cost charged for shipping an order. The amount can be null, indicating shipping details may not be applicable or available. |
| tax_total | numeric | YES | This column represents the total tax amount applied to an order. Purpose unclear from available data due to lack of sample values. |
| grand_total | numeric | NO | This field represents the total monetary amount of an order, inclusive of any additional charges such as taxes or fees. It is mandatory to have a value, indicating it is essential for completing an order transaction. |
| currency | character varying | YES | This column likely indicates the currency in which an order is transacted or reported. The default value suggests that transactions typically occur in U.S. dollars. |
| shipping_address_id | integer | YES | This column likely identifies the specific location to which an order should be shipped. Purpose unclear from available data. |
| billing_address_id | integer | YES | This field likely represents the identifier for the address associated with the billing information for an order, allowing reference to specific billing addresses. Purpose unclear from available data due to lack of sample values. |
| shipping_method_id | integer | YES | The identifier for the method used to ship an order. Purpose unclear from available data. |
| payment_method | character varying | YES | This column records how customers choose to pay for their orders. Purpose unclear from available data. |
| notes | text | YES | Purpose unclear from available data. |
| ip_address | character varying | YES | Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when an order is created. It helps track the timing of order placements within the system. |
| updated_at | timestamp without time zone | YES | This column records the date and time when an order record was last modified. This information is used to track updates or changes made to each order entry. |

## Primary Key

`order_id`

## Foreign Keys

- `billing_address_id` → `synthetic.customer_addresses.address_id`
- `customer_id` → `synthetic.customers.customer_id`
- `shipping_address_id` → `synthetic.customer_addresses.address_id`
- `shipping_method_id` → `synthetic.shipping_methods.shipping_method_id`

## Indexes

- `orders_order_number_key`: CREATE UNIQUE INDEX orders_order_number_key ON synthetic.orders USING btree (order_number)
- `orders_pkey`: CREATE UNIQUE INDEX orders_pkey ON synthetic.orders USING btree (order_id)

*Generated at: 2025-12-14T23:41:55.870Z*