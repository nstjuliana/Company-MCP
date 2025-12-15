# packages

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.packages" table represents a collection of packages, each uniquely identified by the primary key "package_id," and associated with specific attributes such as "weight_kg," "length_cm," "width_cm," "height_cm," and a unique "tracking_number." While this table is not explicitly related to other tables via foreign keys, each package is likely part of a larger system for tracking shipments or deliveries, as suggested by its inclusion of "created_at" and "updated_at" timestamps. The table's role appears to be centralized around maintaining descriptive and logistical information about individual packages within the synthetic_250_postgres database.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| package_id | integer | NO | This column uniquely identifies each package within the system. It automatically assigns consecutive numbers to new entries, serving as the primary key for package records. |
| pack_id | integer | NO | This column appears to represent unique identifiers assigned to packages, ensuring each package can be individually distinguished within the system. Purpose unclear from available data. |
| package_number | integer | NO | Numerical identifier assigned to each package to ensure its unique distinction within the system. Purpose unclear from available data. |
| weight_kg | numeric | YES | This column represents the weight of individual packages in kilograms for a shipping or logistics context. The values range from around 14 to 96 kilograms, indicating varying sizes of packages. |
| length_cm | numeric | YES | This column represents the physical length of packages measured in centimeters. Purpose unclear from available data. |
| width_cm | numeric | YES | This column represents the width dimension of packages measured in centimeters, as evidenced by the sample values. Purpose unclear from available data. |
| height_cm | numeric | YES | This column represents the height of packages measured in centimeters. Purpose unclear from available data. |
| tracking_number | character varying | YES | This column likely represents a unique identifier for packages in a logistics or delivery system, allowing for the tracking of individual packages through various stages of transit. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a package entry is created. It reflects the moment the package was added to the system, with the ability to store unspecified timestamps. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a package record was last modified. The values indicate historical timestamps reflecting updates made to package details. |

## Primary Key

`package_id`

## Foreign Keys

- `pack_id` → `synthetic.pack_orders.pack_id`

## Indexes

- `packages_pkey`: CREATE UNIQUE INDEX packages_pkey ON synthetic.packages USING btree (package_id)

## Sample Data

| package_id | pack_id | package_number | weight_kg | length_cm | width_cm | height_cm | tracking_number | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 17 | 3576 | 46.822 | 31.45 | 115.30 | 658.33 | 56640860633128098907 | Sat Dec 13 2025 02:58:19 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:19 GMT-0600 (Central Stan... |
| 2 | 12 | 7786 | 14.068 | 586.82 | 372.28 | 377.91 | 19411212483889890279 | Sat Dec 13 2025 02:58:19 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:19 GMT-0600 (Central Stan... |
| 3 | 38 | 555 | 32.305 | 104.61 | 358.88 | 901.02 | 74510860302625836481 | Sat Dec 13 2025 02:58:19 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:19 GMT-0600 (Central Stan... |
| 4 | 11 | 6905 | 47.602 | 336.67 | 902.98 | 187.11 | 90744006300294332096 | Sat Dec 13 2025 02:58:19 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:19 GMT-0600 (Central Stan... |
| 5 | 23 | 5019 | 16.358 | 546.78 | 752.05 | 439.01 | 83893566039394158249 | Sat Dec 13 2025 02:58:19 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:19 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:21.143Z*