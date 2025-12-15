# coupon_usage

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.coupon_usage` table appears to represent records of coupon usage events, where each record is uniquely identified by the `usage_id` primary key. The absence of foreign key details suggests undefined relationships to other tables, while the table itself is not referenced by any other tables, indicating it might be a standalone or final destination entity for tracking coupon uses without further relational ties. With zero rows and no column details, the exact nature and attributes involved in logging coupon usage remain unspecified.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| usage_id | integer | NO | This column uniquely identifies each record of coupon usage within the table, as indicated by its sequentially generated values. Purpose unclear from available data due to lack of sample values. |
| coupon_id | integer | NO | This column uniquely identifies each coupon used in the system, linking coupon usage records to specific promotional offers. |
| order_id | integer | NO | Purpose unclear from available data. |
| customer_id | integer | YES | Purpose unclear from available data. |
| discount_applied | numeric | NO | The column likely represents the amount of a discount applied during a coupon usage transaction. Without sample values, the exact business context remains unclear. |
| used_at | timestamp without time zone | YES | This column records the date and time when a coupon was used. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a coupon usage event was initially logged in the system. The exact business context of these records is not clear from the available information. |
| updated_at | timestamp without time zone | YES | Represents the date and time when a record in the coupon usage table was last modified. |

## Primary Key

`usage_id`

## Foreign Keys

- `coupon_id` → `synthetic.coupons.coupon_id`
- `customer_id` → `synthetic.customers.customer_id`
- `order_id` → `synthetic.orders.order_id`

## Indexes

- `coupon_usage_pkey`: CREATE UNIQUE INDEX coupon_usage_pkey ON synthetic.coupon_usage USING btree (usage_id)

*Generated at: 2025-12-14T23:40:02.665Z*