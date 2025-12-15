# ads

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.ads" table represents advertisements within the data model, with each row corresponding to a unique ad identified by the primary key "ad_id." Key attributes include "ad_name," "ad_type," "headline," "description," and several URL fields, indicative of the digital nature and content of the ads. The table serves primarily as a repository of advertisement information, referencing an undefined foreign entity through "ad_group_id" for grouping or categorization purposes.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| ad_id | integer | NO | This column represents a unique identifier for each advertisement entry in the table, ensuring that every ad can be distinctly referenced. The values suggest a sequential assignment, likely indicating the order in which ads are added. |
| ad_group_id | integer | NO | This column represents an identifier for groups of advertisements, which may be used to categorize or organize ads within campaigns. Purpose unclear from available data. |
| ad_name | character varying | YES | This column contains brief descriptive text likely used for distinguishing or identifying advertisements, reflecting diverse themes or messages typical of marketing content. Purpose unclear from available data. |
| ad_type | character varying | YES | Purpose unclear from available data. The sample values are abstract and do not provide a clear indication of the business intent. |
| headline | character varying | YES | This column contains succinct promotional messages or taglines that are likely used to capture attention for advertisements. Purpose unclear from available data. |
| description | text | YES | This column contains narrative or promotional content potentially used in advertising campaigns, reflecting diverse themes, expressions of strategy, and conceptual ideas. Purpose unclear from available data. |
| display_url | character varying | YES | This column represents the web addresses associated with advertisements, likely for redirecting users to the advertiser's online presence or landing page. The URLs indicate a variety of business-related domains, suggesting use in marketing or promotional contexts. |
| final_url | character varying | YES | This column likely stores the URLs associated with advertisements. These URLs direct users to external websites related to the advertised content. |
| image_url | character varying | YES | This column represents the web addresses where images associated with advertisements are hosted. The sample values suggest these URLs belong to various company or personal domains. |
| video_url | character varying | YES | This column contains URLs likely representing links to video content associated with advertisements. The purpose is unclear from the available data. |
| status | character varying | YES | This column indicates the current state of each advertisement, reflecting whether it is currently active, pending review or approval, or inactive. It helps in identifying the operational status of ads within the system. |
| created_at | timestamp without time zone | YES | This column records the date and time when an advertisement entry was created, defaulting to the current timestamp at the time of record insertion. The specific purpose of this timestamp in the business context is unclear from the available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when an advertisement record was last updated. The default value indicates that it captures the timestamp of the most recent modification automatically unless specified otherwise. |

## Primary Key

`ad_id`

## Foreign Keys

- `ad_group_id` → `synthetic.ad_groups.ad_group_id`

## Indexes

- `ads_pkey`: CREATE UNIQUE INDEX ads_pkey ON synthetic.ads USING btree (ad_id)

## Sample Data

| ad_id | ad_group_id | ad_name | ad_type | headline | description | display_url | final_url | image_url | video_url | status | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 9 | Near these deep form. Prepare fact film pick oi... | Space exist eye themselves. | Suffer how role enter wall recognize most. Hope... | Hospital certainly seek model form rate again. ... | https://rodriguez-weaver.com/ | http://brooks.com/ | http://www.benson.com/ | http://washington.com/ | pending | Sat Dec 13 2025 03:14:49 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:49 GMT-0600 (Central Stan... |
| 2 | 22 | What sound list down million. Rich across crime... | Major however stay difficult station conference. | Course decade yet red article hundred provide. ... | Company study option. | http://sanchez-keller.biz/ | https://johnson-roberts.com/ | https://www.huang.com/ | https://moran-sanchez.net/ | inactive | Sat Dec 13 2025 03:14:49 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:49 GMT-0600 (Central Stan... |
| 3 | 34 | Part tell or result.
Candidate teach claim. Com... | Morning message see. | People see leg together learn together two tota... | Involve majority candidate reflect. Fight conce... | https://coleman.info/ | https://anderson.biz/ | https://james-wolf.com/ | https://www.perez-wang.org/ | inactive | Sat Dec 13 2025 03:14:49 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:49 GMT-0600 (Central Stan... |
| 4 | 10 | There begin certainly. Social green type along. | Mind foreign act production yourself standard. | Within cover national address issue how. Networ... | Forget beautiful interesting structure structur... | https://www.white.org/ | http://norton.biz/ | http://www.norton.com/ | http://cook.com/ | pending | Sat Dec 13 2025 03:14:49 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:49 GMT-0600 (Central Stan... |
| 5 | 33 | Hold allow consider surface. Building though se... | Property push price should campaign owner trade. | Who traditional center save air money. Guess re... | Meet card thing forget truth small. Hold hotel ... | https://www.barnes.com/ | https://www.hernandez.com/ | http://www.jacobs.org/ | https://alexander.org/ | active | Sat Dec 13 2025 03:14:49 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:49 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:30.446Z*