# BUNDLES

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.BUNDLES table represents a collection of product bundles, identified by a unique BUNDLE_ID, with attributes such as NAME, DESCRIPTION, and various rating and wishlist attributes (e.g., WISHLIST_199_ATTR_0 and RATING_199_ATTR_2). This table functions independently within the data model with no specified relationships to or from other tables. It primarily serves to catalog bundle entities with both static descriptors and potentially dynamic rating and wishlist metrics.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| BUNDLE_ID | NUMBER | NO | A sequential identifier uniquely assigned to each bundle in the collection. Purpose unclear from available data. |
| NAME | TEXT | NO | This column represents sequential identifiers for bundled items or groups, as indicated by the numbering in their names. The exact purpose of these bundles is unclear from the available data. |
| DESCRIPTION | TEXT | YES | This column provides a textual overview or summary associated with each bundle in the database, specifically indicating sequentially numbered descriptions. The purpose is to offer users an overview of the bundle without additional technical or detailed specifications. |
| WISHLIST_199_ATTR_0 | NUMBER | NO | This column represents sequential identifiers likely used for organizing or categorizing items in a wishlist related to product bundles. The purpose of these identifiers is unclear from the available data. |
| CHECKOUT_199_ATTR_1 | NUMBER | YES | This column likely represents a categorical attribute associated with the checkout process, as suggested by the uniform numeric values. Purpose unclear from available data. |
| RATING_199_ATTR_2 | NUMBER | NO | This column likely represents a numeric rating or score related to a specific attribute (199) within a larger set of bundles. The purpose of this rating in business terms is unclear from the available data. |
| RATING_199_ATTR_3 | TEXT | NO | This column appears to represent a categorical rating or scoring attribute related to bundles, with values ranging from 1 to 10. The specific purpose or significance of this rating is unclear from the available data. |
| SHIPPING_199_ATTR_4 | NUMBER | YES | This column likely represents a categorical identifier or code related to a specific attribute of a shipping process or component. Purpose unclear from available data. |
| RATING_199_ATTR_5 | NUMBER | YES | This column appears to represent a category or classification indicated by numerical codes, possibly reflecting a level or score related to a rating system. The specific purpose or criteria for these codes is unclear from the available data. |

## Primary Key

`BUNDLE_ID`

## Sample Data

| BUNDLE_ID | NAME | DESCRIPTION | WISHLIST_199_ATTR_0 | CHECKOUT_199_ATTR_1 | RATING_199_ATTR_2 | RATING_199_ATTR_3 | SHIPPING_199_ATTR_4 | RATING_199_ATTR_5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | BUNDLES 1 | Description for BUNDLES 1 | 100 | null | 100 | Sample RATING_199_ATTR_3 1 | null | null |
| 2 | BUNDLES 2 | Description for BUNDLES 2 | 101 | 101 | 101 | Sample RATING_199_ATTR_3 2 | 101 | 101 |
| 3 | BUNDLES 3 | Description for BUNDLES 3 | 102 | 102 | 102 | Sample RATING_199_ATTR_3 3 | 102 | 102 |
| 4 | BUNDLES 4 | Description for BUNDLES 4 | 103 | null | 103 | Sample RATING_199_ATTR_3 4 | null | null |
| 5 | BUNDLES 5 | Description for BUNDLES 5 | 104 | 104 | 104 | Sample RATING_199_ATTR_3 5 | 104 | 104 |

*Generated at: 2025-12-14T23:39:37.931Z*