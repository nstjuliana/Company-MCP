# office_locations

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.office_locations` table maintains detailed information about office locations, likely for a business or organization, identified uniquely by the `location_id`. It includes various attributes such as the physical address (with `address_line1`, `address_line2`, `city`, `state_province`, `postal_code`, `country_code`), the name of each location (`location_name`), time zone (`timezone`), and whether it serves as the headquarters (`is_headquarters`), along with timestamps for record creation and updates (`created_at`, `updated_at`). With no foreign key relationships, this table functions in isolation within the data model, providing essential locational data without referencing or being referenced by other tables.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| location_id | integer | NO | Unique identifier assigned sequentially to each office location for differentiation and referencing purposes. |
| location_name | character varying | NO | Purpose unclear from available data. The sample values suggest a storage of abstract, sentence-like text but do not reveal a specific business context or purpose. |
| address_line1 | character varying | YES | This column stores the primary address detail for various office locations, typically including street number, street name, and possibly suite or apartment information. It helps in identifying the specific geographic site of offices within the organization. |
| address_line2 | character varying | YES | This column represents additional address information for office locations, commonly specifying suite or apartment numbers. It helps to precisely identify the location within a building or complex. |
| city | character varying | YES | This column captures the names of cities where office locations are situated, reflecting a variety of fictional geographic areas. Each entry represents a distinct city contributing to the company's operational landscape. |
| state_province | character varying | YES | This column lists the state or province where an office location is situated, reflecting various regions across the United States. Purpose unclear from available data. |
| postal_code | character varying | YES | This column represents the postal codes associated with office locations. The values appear to be numeric strings, potentially used for identifying geographical areas or mail delivery regions. |
| country_code | character varying | YES | This column indicates the ISO country codes representing the location of various offices. Each value corresponds to the country in which an office is located. |
| timezone | character varying | YES | Purpose unclear from available data. |
| is_headquarters | boolean | YES | This column indicates whether an office location serves as the company's main administrative center, with possible values of true for headquarters and false for other locations. The purpose is to distinguish between the primary headquarters and subsidiary office locations. |
| created_at | timestamp without time zone | YES | This column records the date and time when each office location entry was initially created. The timestamps suggest that entries are added at coinciding moments, possibly indicating batch creation. |
| updated_at | timestamp without time zone | YES | This column records the timestamp for when the office location information was last updated. Its default value indicates updates occur automatically to reflect the current time when no other value is provided. |

## Primary Key

`location_id`

## Indexes

- `office_locations_pkey`: CREATE UNIQUE INDEX office_locations_pkey ON synthetic.office_locations USING btree (location_id)

## Sample Data

| location_id | location_name | address_line1 | address_line2 | city | state_province | postal_code | country_code | timezone | is_headquarters | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Occur red course. Finish charge real improve si... | 733 Grant Fork Suite 437 | Suite 758 | Keithshire | Utah | 71698 | MU | Stand west source fact explain research. | false | Sat Dec 13 2025 02:53:53 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:53:53 GMT-0600 (Central Stan... |
| 2 | Experience arrive shoulder present discussion s... | 8872 Nelson Valleys Apt. 527 | Suite 205 | Ashleyborough | Idaho | 80580 | DZ | Still middle beautiful protect continue cell. | true | Sat Dec 13 2025 02:53:53 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:53:53 GMT-0600 (Central Stan... |
| 3 | How staff second. Authority interest red must a... | 512 Rice Stream | Apt. 004 | Nunezside | Nevada | 70222 | MU | Easy get every visit right. | false | Sat Dec 13 2025 02:53:53 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:53:53 GMT-0600 (Central Stan... |
| 4 | Deal beyond almost our reflect.
Scientist I doc... | 4408 Connie Meadow | Suite 056 | Heatherchester | Georgia | 39807 | MT | Senior list support feeling. | false | Sat Dec 13 2025 02:53:53 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:53:53 GMT-0600 (Central Stan... |
| 5 | Trial receive region however dream focus execut... | 7725 Donald Plains Suite 280 | null | Port Melanieton | Wisconsin | 01337 | NG | Successful discuss religious across. | false | Sat Dec 13 2025 02:53:53 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:53:53 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:15.334Z*