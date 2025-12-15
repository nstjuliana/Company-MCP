# shipping_methods

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.shipping_methods" table captures the details of various shipping methods available, with "shipping_method_id" serving as the primary key. Columns include attributes such as "method_name", "carrier", "base_rate", "per_kg_rate", "estimated_days_min", "estimated_days_max", "is_active", and timestamps for creation and updates, indicating the specifics of each shipping method's cost structure and estimated delivery times. This table stands independently within the database, as evidenced by the absence of foreign key relationships or references to other tables, possibly serving as a reference for logistics and order fulfillment modules.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| shipping_method_id | integer | NO | This column uniquely identifies each shipping method available in the system. It ensures that every shipping method has a distinct number for reference and management purposes. |
| method_name | character varying | NO | Purpose unclear from available data. |
| carrier | character varying | YES | Purpose unclear from available data. |
| base_rate | numeric | NO | This column represents the fixed starting price for different shipping strategies available to customers. The values suggest a variety of base costs, potentially reflecting differences in delivery speed or service quality. |
| per_kg_rate | numeric | YES | This column represents the cost associated with shipping items based on their weight, expressed in currency units per kilogram. The varied sample values suggest differing rates that may depend on factors such as distance or shipping speed. |
| estimated_days_min | integer | YES | This column likely represents the minimum number of days estimated for a package to be delivered using a specific shipping method. Values indicate the lower boundary of the expected delivery timeframe, suggesting varying efficiency levels between different methods. |
| estimated_days_max | integer | YES | This column represents the maximum estimated number of days for a shipment to be delivered using a specific shipping method. It helps set customer expectations by indicating the upper limit of delivery timeframes. |
| is_active | boolean | YES | This column indicates whether a shipping method is currently active for use in operations. If the value is true, the shipping method is active; if false or null, it is considered inactive. |
| created_at | timestamp without time zone | YES | This column records the date and time when a shipping method entry was created in the system. The exact timestamp reflects the moment of entry, with the default being the current time upon record insertion. |
| updated_at | timestamp without time zone | YES | This column records the date and time when entries in the shipping methods table were last updated. The use of a default timestamp suggests this record is automatically populated upon changes to the data. |

## Primary Key

`shipping_method_id`

## Indexes

- `shipping_methods_pkey`: CREATE UNIQUE INDEX shipping_methods_pkey ON synthetic.shipping_methods USING btree (shipping_method_id)

## Sample Data

| shipping_method_id | method_name | carrier | base_rate | per_kg_rate | estimated_days_min | estimated_days_max | is_active | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Including sort laugh trade. Foreign write what ... | Center agency establish smile public. Tough for... | 2.60 | 68.13 | 22 | 4 | false | Sat Dec 13 2025 02:56:38 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:38 GMT-0600 (Central Stan... |
| 2 | Little factor because girl. Maybe plant school ... | Energy education growth east upon. Certainly ch... | 37.36 | 92.91 | 4 | 27 | false | Sat Dec 13 2025 02:56:38 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:38 GMT-0600 (Central Stan... |
| 3 | Find such Republican. Letter south control leas... | Another anyone all increase police. Space gover... | 15.38 | 8.11 | 27 | 23 | false | Sat Dec 13 2025 02:56:38 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:38 GMT-0600 (Central Stan... |
| 4 | Many voice allow whatever financial arm. Intere... | Democratic later look thought away. Outside tim... | 45.41 | 95.52 | 20 | 22 | true | Sat Dec 13 2025 02:56:38 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:38 GMT-0600 (Central Stan... |
| 5 | Nothing available focus marriage. Study questio... | Minute well such respond record south. Line cal... | 32.94 | 4.38 | 20 | 15 | false | Sat Dec 13 2025 02:56:38 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:38 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:42:47.875Z*