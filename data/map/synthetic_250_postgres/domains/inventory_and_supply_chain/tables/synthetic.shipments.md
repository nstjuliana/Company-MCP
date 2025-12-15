# shipments

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.shipments` table likely represents records of shipments within the business, each identified uniquely by `shipment_id` as the primary key. Without specific column names or data, the business context and relationships to other tables remain undefined, limiting insight into its precise role in the broader data model or relationships with other entities. The absence of data and defined foreign keys suggests this table is either a placeholder or poised for future development.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| shipment_id | integer | NO | This column uniquely identifies each shipment record within the database. It automatically generates a new identifier for every new shipment entry. |
| order_id | integer | NO | This column represents the unique identifier for each order associated with a shipment. It ensures that each shipment can be directly linked to its corresponding order in the business process. |
| tracking_number | character varying | YES | A unique identifier assigned to each shipment to facilitate its tracking and monitoring throughout the delivery process. |
| carrier | character varying | YES | The column indicates the name or identifier of the company responsible for transporting goods in shipments. Purpose unclear from available data due to lack of sample values. |
| shipped_date | timestamp without time zone | YES | This column indicates when the shipment process was initiated. Its purpose is unclear from available data. |
| delivered_date | timestamp without time zone | YES | This column records the date and time when shipments are confirmed as delivered. It is optional, indicating shipments may not always have delivery data entered. |
| status | character varying | YES | This field likely indicates the current condition or progress of a shipment and defaults to a preliminary state of being unprocessed or awaiting further action. Purpose unclear from available data due to lack of sample values. |
| shipping_cost | numeric | YES | Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a shipment entry was initially created in the database. Given its default value, it likely reflects the system time at the moment each record is added. |
| updated_at | timestamp without time zone | YES | Records the date and time when a shipment record was last modified. |

## Primary Key

`shipment_id`

## Foreign Keys

- `order_id` → `synthetic.orders.order_id`

## Indexes

- `shipments_pkey`: CREATE UNIQUE INDEX shipments_pkey ON synthetic.shipments USING btree (shipment_id)

*Generated at: 2025-12-14T23:42:47.975Z*