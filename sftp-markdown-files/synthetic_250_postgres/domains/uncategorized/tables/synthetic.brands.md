# brands

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.brands` table represents a collection of brands, characterized by unique identifiers (`brand_id`), descriptive names, website URLs, and logo links, with an indicator if a brand is featured (`is_featured`). This table does not have any direct relationships with other tables in the database, suggesting that it serves as a standalone reference for brand information. The presence of timestamps (`created_at` and `updated_at`) indicates that the table supports tracking the creation and modification of brand entries.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| brand_id | integer | NO | This column represents a unique identifier assigned to each brand in the system, indicating its sequential order of creation. It ensures that every brand has a distinct and traceable identity within the dataset. |
| brand_name | character varying | NO | Purpose unclear from available data. The sample values appear disjointed and do not provide clear insight into a cohesive business context. |
| slug | character varying | YES | This column represents a URL-friendly version of brand identifiers, likely used to create readable and SEO-friendly links by joining descriptive words with hyphens. Purpose unclear from available data. |
| logo_url | character varying | YES | This column contains URLs linking to the brand logos of various companies. The links appear to point to different domains, suggesting they are hosted on various web platforms. |
| description | text | YES | This column likely contains brief narrative-style descriptions or summaries related to brands, potentially highlighting operational aspects, partnerships, services, market activities, or business strategies. Purpose unclear from available data due to the varied nature of the text. |
| website | character varying | YES | This column lists the official websites associated with various brands, serving as online portals for business information and customer interaction. The URLs predominantly use a secure protocol and vary in domain types such as .com, .biz, and .org. |
| is_featured | boolean | YES | This column indicates whether a brand is currently promoted or highlighted, with true representing featured status and false representing non-featured status. The purpose of distinguishing featured brands is unclear from the available data. |
| created_at | timestamp without time zone | YES | This column represents the date and time a brand entry was created in the system. It captures the moment a brand is registered, using the current timestamp by default, but can also be left empty. |
| updated_at | timestamp without time zone | YES | This column records the date and time when the information in the brands table was last modified. If no update has been made, it defaults to the current timestamp, indicating the initial creation time of the entry. |

## Primary Key

`brand_id`

## Indexes

- `brands_brand_name_key`: CREATE UNIQUE INDEX brands_brand_name_key ON synthetic.brands USING btree (brand_name)
- `brands_pkey`: CREATE UNIQUE INDEX brands_pkey ON synthetic.brands USING btree (brand_id)
- `brands_slug_key`: CREATE UNIQUE INDEX brands_slug_key ON synthetic.brands USING btree (slug)

## Sample Data

| brand_id | brand_name | slug | logo_url | description | website | is_featured | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Especially cold discuss. To few car would sudde... | movement-region | http://barrett-hughes.com/ | Beautiful operation place officer partner minut... | https://www.hammond.com/ | true | Sat Dec 13 2025 02:55:49 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:49 GMT-0600 (Central Stan... |
| 2 | Already foreign natural remember. Major draw gr... | design-inside-house | https://www.marshall.com/ | Treatment involve discussion doctor with wish u... | https://morgan.com/ | true | Sat Dec 13 2025 02:55:49 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:49 GMT-0600 (Central Stan... |
| 3 | Animal accept matter. Popular this also over co... | but-contain | https://www.brown.biz/ | Show usually learn. Service month assume curren... | https://www.gutierrez.biz/ | false | Sat Dec 13 2025 02:55:49 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:49 GMT-0600 (Central Stan... |
| 4 | Property tend quickly almost. Sure newspaper gl... | argue-board-stop | http://www.crawford-koch.info/ | Training democratic free choice old. Action wel... | https://sullivan-carr.com/ | false | Sat Dec 13 2025 02:55:49 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:49 GMT-0600 (Central Stan... |
| 5 | Account upon door safe. Doctor water military c... | much-especially-his | https://www.lara-smith.com/ | Share big phone upon two. Seven sister far resp... | http://ellison.com/ | false | Sat Dec 13 2025 02:55:49 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:49 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:20.082Z*