# coupons

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.coupons" table captures data related to discount coupons, each uniquely identified by "coupon_id," featuring attributes like "coupon_code," "description," "discount_type," and "discount_value" to specify the nature and extent of the promotion. It logs conditions such as "minimum_purchase" and "maximum_discount," along with constraints on usage through "usage_limit," "usage_count," and "per_customer_limit." This standalone table serves a key role in managing promotional activities, with time-bound parameters ("start_date," "end_date") and status tracking ("is_active") for each coupon, emphasizing its application within customer purchase workflows.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| coupon_id | integer | NO | This column represents a unique identifier assigned sequentially to each coupon in the system. It ensures each coupon can be distinctly recognized and referenced. |
| coupon_code | character varying | NO | This column represents a series of unique identification codes, commonly used for promotional offers or discounts. The purpose of these codes within the business context remains unclear from the available data. |
| description | character varying | YES | This column contains abstract or nonsensical text entries that appear to form incomplete sentences. Purpose unclear from available data. |
| discount_type | character varying | NO | Purpose unclear from available data. |
| discount_value | numeric | NO | This column represents the monetary value of discounts offered by coupons in a business setting, as indicated by the numeric sample values. These figures reflect direct reductions on purchases provided to customers. |
| minimum_purchase | numeric | YES | This column represents the minimum purchase amount required to be eligible for a discount or offer associated with a coupon. The sample values suggest that the required purchase thresholds can range widely, depending on the specific promotion. |
| maximum_discount | numeric | YES | This column represents the highest monetary value that can be deducted from a purchase when using a coupon. It implies a limit on discounts that vary widely, with some values reaching several hundred dollars. |
| usage_limit | integer | YES | This column likely represents the maximum number of times a coupon can be used. Purpose unclear from available data. |
| usage_count | integer | YES | This column represents the number of times a particular coupon has been used. The values indicate varied usage frequency, suggesting that some coupons are more popular or applicable than others. |
| per_customer_limit | integer | YES | This column likely specifies the maximum number of times a customer can use a specific coupon, with higher numbers indicating fewer restrictions per individual customer. The purpose is to manage coupon distribution and usage frequency among customers, though further context is needed for definitive understanding. |
| start_date | timestamp without time zone | YES | This column indicates the date and time when a coupon becomes valid and can be used by customers. The values represent various start dates in the years 2024 and 2025, generally aligning with Central Time. |
| end_date | timestamp without time zone | YES | This column likely represents the expiration date and time for promotional coupons, indicating the deadline after which the coupons are no longer valid for use. The values suggest a timeframe during which the coupons can be redeemed. |
| is_active | boolean | YES | Indicates whether a coupon is currently valid for use. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a coupon was initially created, as indicated by the current timestamps and default value. The precise moment of creation can be crucial for tracking the activation period of each coupon. |
| updated_at | timestamp without time zone | YES | This column records the last date and time a coupon entry was updated in the system. Purpose unclear from available data. |

## Primary Key

`coupon_id`

## Indexes

- `coupons_coupon_code_key`: CREATE UNIQUE INDEX coupons_coupon_code_key ON synthetic.coupons USING btree (coupon_code)
- `coupons_pkey`: CREATE UNIQUE INDEX coupons_pkey ON synthetic.coupons USING btree (coupon_id)

## Sample Data

| coupon_id | coupon_code | description | discount_type | discount_value | minimum_purchase | maximum_discount | usage_limit | usage_count | per_customer_limit | start_date | end_date | is_active | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | GPSLQJJMFX | Century term especially thank. | Congress | 833.08 | 673.11 | 734.58 | 7739 | 818 | 2655 | Mon Aug 19 2024 09:18:01 GMT-0500 (Central Dayl... | Tue Jan 14 2025 04:05:39 GMT-0600 (Central Stan... | true | Sat Dec 13 2025 02:56:43 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:43 GMT-0600 (Central Stan... |
| 2 | YOONYRKDXS | Leader suddenly oil best watch trade. Say never... | early | 282.46 | 749.25 | 667.06 | 2116 | 177 | 3269 | Tue Jul 09 2024 21:21:43 GMT-0500 (Central Dayl... | Mon Apr 01 2024 10:26:39 GMT-0500 (Central Dayl... | true | Sat Dec 13 2025 02:56:43 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:43 GMT-0600 (Central Stan... |
| 3 | YIXVRHNUIV | Color of evidence weight room. He want trip res... | himself | 605.75 | 100.90 | 415.98 | 8090 | 310 | 3846 | Sun Oct 27 2024 02:22:03 GMT-0500 (Central Dayl... | Wed Apr 17 2024 23:29:38 GMT-0500 (Central Dayl... | true | Sat Dec 13 2025 02:56:43 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:43 GMT-0600 (Central Stan... |
| 4 | ONAGBUFBSE | Memory might government alone per. Treat indivi... | leg | 556.83 | 999.26 | 358.79 | 4274 | 365 | 2599 | Sun May 12 2024 10:53:14 GMT-0500 (Central Dayl... | Wed Oct 15 2025 20:11:51 GMT-0500 (Central Dayl... | true | Sat Dec 13 2025 02:56:43 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:43 GMT-0600 (Central Stan... |
| 5 | OCTBXEQCKD | Then understand write consumer military part jo... | need | 827.95 | 894.46 | 31.97 | 1044 | 345 | 7056 | Wed Aug 20 2025 18:45:27 GMT-0500 (Central Dayl... | Wed Nov 06 2024 04:47:54 GMT-0600 (Central Stan... | true | Sat Dec 13 2025 02:56:43 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:56:43 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:05.308Z*