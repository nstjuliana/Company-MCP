# leads

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.leads` table represents potential business opportunities or prospective clients, indicated by individuals or companies, that are tracked by a company for future engagement. It captures detailed information about each lead, including personal contact information, organizational details, source, status, and conversion metrics, with the `lead_id` serving as the primary identifier. While it has foreign keys linking to unidentified tables, the table itself functions as a central repository for lead management, facilitating tracking and conversion processes, evident from fields like `converted_account_id` and `converted_contact_id`.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| lead_id | integer | NO | This column uniquely identifies each lead within the table, ensuring each entry has a distinct identifier. It serves as the primary key for differentiating individual leads. |
| first_name | character varying | YES | This column represents the given names of individuals that are being tracked or managed within the system. Purpose unclear from available data. |
| last_name | character varying | NO | This column likely records the family name of individuals or entities associated with sales leads. The values suggest a diverse range of common last names. |
| company | character varying | YES | This column likely contains the names of companies or organizations associated with leads, possibly indicating the entity that the lead is connected to or represents. Purpose unclear from available data. |
| title | character varying | YES | This column likely represents brief descriptions or summaries related to leads, capturing various aspects or statuses relevant to them. Purpose unclear from available data due to the abstract nature of the examples. |
| email | character varying | YES | This column represents the email addresses of individuals who are potential customers or leads. The addresses appear to follow typical email formatting, indicating personal or generic contact methods. |
| phone | character varying | YES | This column contains phone numbers in various formats, including international and extensions. These numbers likely serve as contact details for leads or potential clients. |
| website | character varying | YES | This column represents the web addresses for various businesses or organizations associated with the leads in the dataset. The URLs appear to be personalized for each lead, suggesting an online presence for engagement or informational purposes. |
| lead_source | character varying | YES | Purpose unclear from available data. Sample values suggest diverse and abstract content, making it difficult to determine specific business meaning. |
| lead_status | character varying | YES | This column represents the current stage or outcome of a lead's progress through a given process. Sample values suggest stages include states such as "new," "pending," and "completed," indicating development or completion status. |
| rating | character varying | YES | Purpose unclear from available data. |
| industry | character varying | YES | This column appears to capture brief descriptions or phrases related to various industries or business activities. Purpose unclear from available data. |
| annual_revenue | numeric | YES | This column represents the estimated yearly revenue expressed in a numerical value, likely indicating the financial strength of potential business leads. The purpose of these specific amounts is unclear from the available data. |
| employees | integer | YES | This column likely indicates the number of employees associated with each lead entry in the dataset, reflecting the scale or size of the potential clients or businesses. Purpose unclear from available data. |
| description | text | YES | This column captures brief narrative entries or comments that provide context or insights regarding various aspects of leads, such as development, management, decisions, or actions taken, as reflected in the diverse and abstract sample sentences. Purpose unclear from available data. |
| address | text | YES | This column contains mailing address information associated with leads, including various formats such as military and diplomatic post office addresses. The data includes street addresses, city, state abbreviations, and postal codes, reflecting diverse geographical locations. |
| owner_id | integer | YES | This column likely represents a unique identifier for individuals or entities responsible for managing or owning the leads, allowing for tracking or assignment purposes. The exact purpose is unclear from the available data. |
| converted_account_id | integer | YES | This column likely represents the identifier for an account that a lead has been converted into within a business context. Purpose unclear from available data. |
| converted_contact_id | integer | YES | Purpose unclear from available data. |
| converted_date | date | YES | This column likely records the date when a lead was successfully converted to a customer or a different status. Purpose beyond this interpretation is unclear from the available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a lead record was initially created in the system. It defaults to the current timestamp upon the creation of a new lead, but its precise purpose is unclear from the available data. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a lead's information was last modified. It helps track the most recent updates or changes made to lead entries, with updates defaulting to the current timestamp if not specified. |

## Primary Key

`lead_id`

## Foreign Keys

- `converted_account_id` → `synthetic.accounts.account_id`
- `converted_contact_id` → `synthetic.contacts.contact_id`

## Indexes

- `leads_pkey`: CREATE UNIQUE INDEX leads_pkey ON synthetic.leads USING btree (lead_id)

## Sample Data

| lead_id | first_name | last_name | company | title | email | phone | website | lead_source | lead_status | rating | industry | annual_revenue | employees | description | address | owner_id | converted_account_id | converted_contact_id | converted_date | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Seth | Wallace | Lee-Ryan | Remain indeed reach. | sandra79@example.org | 338-630-6265x788 | https://cruz.biz/ | Behind teach mother method beyond item bar. Hap... | pending | Assume check fact. | Sort tree trade catch decade. Sit nice myself n... | 621.91 | 467 | Institution woman reduce human. Charge differen... | USNS Atkinson, FPO AP 04120 | 424 | 22 | null | Sun Dec 22 2024 00:00:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:31 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:31 GMT-0600 (Central Stan... |
| 2 | Samantha | Hill | Rogers, Ryan and Pena | Ready live movement. | robertallen@example.com | +1-247-999-5811 | https://www.long.com/ | Work improve rule. Doctor especially last someb... | active | Place produce of. | Speech PM again maintain. Wall save color member. | 888.82 | 561 | Number small hard property whatever. Develop re... | 64319 Smith Divide, Wilcoxfort, HI 58478 | 2365 | 27 | null | Mon Sep 30 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:58:31 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:31 GMT-0600 (Central Stan... |
| 3 | Richard | Kirby | Jones Group | Important statement. | jacksoncynthia@example.com | 001-528-945-3273 | https://www.cruz.com/ | Individual protect recent product right many. I... | active | View deal future. | Usually course position meet close game governm... | 539.47 | 9806 | Minute choice light next why. Management indust... | 693 Chambers Ports, South Christinaport, NV 96477 | 8605 | 11 | null | Sun Apr 06 2025 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:58:31 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:31 GMT-0600 (Central Stan... |
| 4 | Andrea | Reyes | Taylor PLC | Certain stop wish power of. | lambertjoseph@example.org | 001-354-241-7772x169 | https://www.hawkins.com/ | Trouble popular condition focus. Ten chair this. | inactive | Reduce follow. | Check attorney usually first. Tonight executive... | 100.12 | 5713 | At officer discussion then class economy piece ... | Unit 3440 Box 1487, DPO AP 70400 | 3649 | 6 | null | Thu Nov 21 2024 00:00:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:31 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:31 GMT-0600 (Central Stan... |
| 5 | Richard | Bailey | Jackson, Dunn and Morris | Class nice despite short. | xcampos@example.com | 515.509.4817 | http://www.smith.com/ | Remain part certainly policy will. | completed | Strategy lose. | Employee receive parent. Us consider baby south... | 988.19 | 1842 | Professional knowledge tough why. Thought care ... | 025 Valerie Tunnel Suite 461, Kristishire, AK 1... | 7794 | 30 | null | Thu Jul 18 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Dec 13 2025 02:58:31 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:31 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:43.532Z*