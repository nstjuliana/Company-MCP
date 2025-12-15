# product_categories

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.product_categories" table represents a hierarchical structure of product categories, providing key attributes for each category such as name, description, and status, which can be used for organizing products in a retail or e-commerce context. The primary key, "category_id," uniquely identifies each category, and the optional "parent_category_id" allows for nesting of categories, indicating a parent-child hierarchy. Although currently not linked to other tables by foreign keys, this table is likely intended for categorizing products in another table within the database.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| category_id | integer | NO | This column uniquely identifies each product category in the system with an incrementing numerical value. It ensures that every category has a distinct and definitive reference within the database. |
| category_name | character varying | NO | Purpose unclear from available data. |
| slug | character varying | YES | This column likely contains URL-friendly identifiers or keywords for different product categories, using hyphenated phrases to represent the category's identity or theme. Purpose unclear from available data. |
| parent_category_id | integer | YES | This column signifies the identifier of a higher-level category to which a product category belongs, allowing for a hierarchical categorization of products. Its usage helps in organizing categories under broader parent categories, although specific business logic or category names are not evidenced by the available data. |
| description | text | YES | Provides narrative or promotional text related to specific product categories, potentially utilized for marketing or descriptive purposes. Purpose unclear from available data. |
| image_url | character varying | YES | This column stores URLs linking to images associated with product categories, likely used for marketing or organizational purposes. The presence of domain names suggests a variety of potential sources for these images. |
| sort_order | integer | YES | This column represents the sequence in which product categories are displayed or processed, with higher values possibly indicating later positioning in a list or hierarchy. Purpose unclear from available data. |
| is_active | boolean | YES | Indicates whether a product category is currently visible or usable within the system. A lack of consistent values suggests that both active and inactive statuses are common. |
| meta_title | character varying | YES | This column appears to contain brief descriptive phrases or slogans that may relate to or categorize products. The phrases are abstract and general, suggesting they might serve as meta descriptions or tags for different product categories. |
| meta_description | text | YES | This column likely contains succinct promotional or descriptive text for different product categories, intended to provide additional context or attract potential customers. The exact purpose remains unclear from the available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a product category was created within the database system. It captures this information by default at the time a new entry is made. |
| updated_at | timestamp without time zone | YES | This column records the date and time when the information related to product categories was last updated. Purpose unclear from available data. |

## Primary Key

`category_id`

## Foreign Keys

- `parent_category_id` → `synthetic.product_categories.category_id`

## Indexes

- `product_categories_pkey`: CREATE UNIQUE INDEX product_categories_pkey ON synthetic.product_categories USING btree (category_id)
- `product_categories_slug_key`: CREATE UNIQUE INDEX product_categories_slug_key ON synthetic.product_categories USING btree (slug)

## Sample Data

| category_id | category_name | slug | parent_category_id | description | image_url | sort_order | is_active | meta_title | meta_description | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Simply anything mention collection. Mouth use d... | base-firm-law-much | null | Nature forget treatment general wall dark whose... | https://www.rogers-smith.com/ | 226 | false | Price state nature reality range. | Bed bar religious camera direction. Never relat... | Sat Dec 13 2025 02:55:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:45 GMT-0600 (Central Stan... |
| 2 | Or assume care garden sort. Challenge current b... | security-for-watch | 1 | From the individual decade subject girl over di... | https://norman-woods.com/ | 5000 | false | Laugh tax throughout. | Top model property other. Meeting people securi... | Sat Dec 13 2025 02:55:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:45 GMT-0600 (Central Stan... |
| 3 | List budget reflect recently so choose. Assume ... | enough-give-size | 2 | Person television commercial month clear leave ... | http://www.sims.net/ | 373 | false | Leg ability certain. | Us beautiful loss environment. Structure instit... | Sat Dec 13 2025 02:55:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:45 GMT-0600 (Central Stan... |
| 4 | Material sport whom get different start. Discus... | may-city-present | 1 | Another this lose bit just when many. Building ... | https://www.sanchez-cannon.com/ | 8815 | true | Thank scene fast TV even. | Buy moment with quite summer. Media deal necess... | Sat Dec 13 2025 02:55:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:45 GMT-0600 (Central Stan... |
| 5 | Ago training treatment enjoy every still top. H... | right-store-i | 2 | If scene car if office order usually camera. Gr... | https://www.glass-turner.com/ | 8953 | false | Worry often third. | Some feeling science. | Sat Dec 13 2025 02:55:45 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:45 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:38:57.876Z*