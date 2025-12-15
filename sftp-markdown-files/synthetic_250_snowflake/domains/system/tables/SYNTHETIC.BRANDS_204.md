# BRANDS_204

**Database:** synthetic_250_snowflake
**Schema:** SYNTHETIC
**Description:** The SYNTHETIC.BRANDS_204 table encapsulates information about distinct brands, identified by the primary key BRAND_ID, with details such as NAME, DESCRIPTION, and various attributes related to checkout, wishlist, and cart interactions. Despite lacking explicit foreign key relationships, the table likely serves as a standalone entity within the database, potentially used for categorizing or detailing brand-specific information in the context of a larger retail or e-commerce application. This table plays a crucial role in managing brand metadata that could influence user interactions during shopping sessions.

**Row Count:** 10

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| BRAND_ID | NUMBER | NO | This column represents unique identifiers assigned to different brands within the dataset. Each value is a distinct number associated with a specific brand entity. |
| NAME | TEXT | YES | This column represents a sequence of identifiers or labels assigned to brand entities within the "BRANDS_204" category. Purpose unclear from available data. |
| DESCRIPTION | TEXT | NO | This column contains descriptions for entries in the BRANDS_204 table. Each entry likely contains a unique identifier or narrative distinguishing the different brand entities. |
| CHECKOUT_224_ATTR_0 | NUMBER | YES | This column likely denotes a specific attribute or feature related to the checkout process for different brands, as inferred from the sequential nature of the sample values. Purpose unclear from available data. |
| CHECKOUT_224_ATTR_1 | NUMBER | YES | This column likely represents a numerical attribute related to a checkout process or transaction, possibly an identifier or a status code associated with different brands or products. Purpose unclear from available data. |
| WISHLIST_224_ATTR_2 | NUMBER | YES | This column likely represents a unique identifier for specific attributes associated with a customer's wishlist related to brands. Purpose unclear from available data. |
| WISHLIST_224_ATTR_3 | TEXT | YES | Purpose unclear from available data. |
| CART_224_ATTR_4 | BOOLEAN | YES | Purpose unclear from available data. |
| VERSION | NUMBER | NO | This column represents the sequential versioning or iteration number of brand entries, indicating different states or updates of a brand entity in ascending order. Each increment denotes a new version, ensuring consistent tracking of brand modifications over time. |

## Primary Key

`BRAND_ID`

## Sample Data

| BRAND_ID | NAME | DESCRIPTION | CHECKOUT_224_ATTR_0 | CHECKOUT_224_ATTR_1 | WISHLIST_224_ATTR_2 | WISHLIST_224_ATTR_3 | CART_224_ATTR_4 | VERSION |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | BRANDS_204 1 | Description for BRANDS_204 1 | null | null | null | Sample WISHLIST_224_ATTR_3 1 | true | 100 |
| 2 | BRANDS_204 2 | Description for BRANDS_204 2 | 101 | 101 | 101 | Sample WISHLIST_224_ATTR_3 2 | false | 101 |
| 3 | BRANDS_204 3 | Description for BRANDS_204 3 | 102 | 102 | 102 | Sample WISHLIST_224_ATTR_3 3 | true | 102 |
| 4 | BRANDS_204 4 | Description for BRANDS_204 4 | null | null | null | Sample WISHLIST_224_ATTR_3 4 | false | 103 |
| 5 | BRANDS_204 5 | Description for BRANDS_204 5 | 104 | 104 | 104 | Sample WISHLIST_224_ATTR_3 5 | true | 104 |

*Generated at: 2025-12-14T23:39:38.972Z*