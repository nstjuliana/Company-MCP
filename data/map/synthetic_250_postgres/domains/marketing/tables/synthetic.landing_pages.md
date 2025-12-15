# landing_pages

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.landing_pages" table represents the business entity of landing pages used in digital marketing campaigns, characterized by campaign-specific identifiers, URLs, content, metadata, status, and timestamps for publication and modification. The primary key, "page_id," uniquely identifies each landing page, with a foreign key relationship to an unspecified table suggesting a linkage to broader campaign data. This table’s role in the data model is to store essential information and attributes of landing pages, facilitating their management and association with marketing campaigns.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| page_id | integer | NO | This column uniquely identifies each landing page with a sequential number. It serves as the primary means of referring to specific landing pages within the system. |
| campaign_id | integer | YES | This field appears to refer to a unique identifier associated with a specific marketing campaign connected to the landing pages. The exact purpose and usage are unclear from the available data. |
| page_name | character varying | NO | This column represents descriptive titles or themes for various landing pages, likely capturing concepts or subjects relevant to the content presented on each page. The purpose remains unclear beyond providing an overview or thematic focus based on the sample values. |
| url_slug | character varying | YES | This column contains URL links, likely referencing specific landing pages for different websites, used to direct users to particular sections of the businesses' web presence. The URLs are primarily in business and organizational formats, suggesting their use in online marketing or commerce. |
| html_content | text | YES | This column stores short text excerpts or descriptions likely associated with various web pages or web-related content. Purpose unclear from available data. |
| meta_title | character varying | YES | This column represents brief descriptive titles or headlines associated with various landing pages, potentially used for summarizing or capturing the essence of page content. Purpose unclear from available data. |
| meta_description | text | YES | Purpose unclear from available data. The text entries appear to be fragments of various sentences or statements. |
| status | character varying | YES | This column indicates the current state or progress of a landing page, such as whether it is active, inactive, or pending. It helps track and manage the availability and readiness of landing pages. |
| published_at | timestamp without time zone | YES | Represents the date and time at which a particular landing page was published. It may not always have a value, indicating some pages might not yet be published. |
| created_at | timestamp without time zone | YES | This column records the date and time when a landing page entry was created. It reflects the initial timestamp set by the system and defaults to the current time upon entry creation. |
| updated_at | timestamp without time zone | YES | This column records the date and time a landing page record was last updated. The default value indicates it captures the current timestamp unless specified otherwise. |

## Primary Key

`page_id`

## Foreign Keys

- `campaign_id` → `synthetic.marketing_campaigns.campaign_id`

## Indexes

- `landing_pages_pkey`: CREATE UNIQUE INDEX landing_pages_pkey ON synthetic.landing_pages USING btree (page_id)
- `landing_pages_url_slug_key`: CREATE UNIQUE INDEX landing_pages_url_slug_key ON synthetic.landing_pages USING btree (url_slug)

## Sample Data

| page_id | campaign_id | page_name | url_slug | html_content | meta_title | meta_description | status | published_at | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 16 | Rate strong leg region need concern American. W... | https://morris-crawford.org/ | Quite size writer something. Adult figure forme... | Foot test bit. | Near without support. Now treatment although se... | active | Wed Jul 02 2025 21:07:04 GMT-0500 (Central Dayl... | Sat Dec 13 2025 03:14:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:15 GMT-0600 (Central Stan... |
| 2 | 36 | Trip cultural learn. Candidate medical official... | https://palmer.net/ | However present national short simply wide leve... | Book white later. | Season career policy unit. Pressure fear later ... | active | Tue Nov 18 2025 03:22:58 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:15 GMT-0600 (Central Stan... |
| 3 | 11 | Behind TV PM cover price politics. Man movement... | https://www.lopez.com/ | Crime learn finish provide former budget. Late ... | Would among word already. | Like available individual finally. Nor son son ... | active | Tue Jun 17 2025 12:28:31 GMT-0500 (Central Dayl... | Sat Dec 13 2025 03:14:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:15 GMT-0600 (Central Stan... |
| 4 | 27 | Foot join if town collection change. | https://www.lucas.biz/ | Rich article question in ahead concern score. H... | Threat none contain rate. | Nor hear front age. Leader painting it voice. | inactive | Fri Nov 15 2024 01:15:49 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:15 GMT-0600 (Central Stan... |
| 5 | 45 | Question common argue once decade finally. Lead... | http://johnson.com/ | Among argue nice this memory present. Security ... | Movement knowledge coach natural certainly. | Character realize million really score. Wonder ... | pending | Tue Sep 16 2025 23:40:28 GMT-0500 (Central Dayl... | Sat Dec 13 2025 03:14:15 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:15 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:43:24.307Z*