# social_accounts

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.social_accounts` table represents social media accounts, detailing information such as the platform, account name, handle, and URL, along with metrics like the number of followers and account status (active or inactive). This table, identifiable by the primary key `account_id`, serves as a standalone entity within the database, as it neither references nor is referenced by other tables. The information captured, such as creation and update timestamps, suggests it supports tracking the activity and status of social media presences over time.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| account_id | integer | NO | This column uniquely identifies each record in the social accounts table, ensuring each social account has a distinct identifier. The sequential nature of the values suggests an order of creation or entry. |
| platform | character varying | NO | Purpose unclear from available data. |
| account_name | character varying | NO | Purpose unclear from available data. |
| account_handle | character varying | YES | The column appears to store phrases or sentences that seem more abstract and unrelated, potentially representing user-generated content or text blurbs associated with social media accounts. Purpose unclear from available data. |
| account_url | character varying | YES | This column contains URLs associated with various social accounts, which appear to represent the web addresses of individuals' or organizations' online profiles. The exact purpose or nature of these social accounts is unclear from the available data. |
| followers_count | integer | YES | This column represents the number of followers associated with a specific social media account. The values indicate varying levels of social media engagement for each account. |
| is_active | boolean | YES | This column indicates whether a social account is currently active. The default state is active, but it can be switched to inactive. |
| created_at | timestamp without time zone | YES | Represents the date and time when a social account record was created. The values suggest that entries default to the current timestamp if not otherwise specified. |
| updated_at | timestamp without time zone | YES | This column stores the date and time when a social account record was last updated. It is set to the current timestamp by default but can be null if no updates have occurred. |

## Primary Key

`account_id`

## Indexes

- `social_accounts_pkey`: CREATE UNIQUE INDEX social_accounts_pkey ON synthetic.social_accounts USING btree (account_id)

## Sample Data

| account_id | platform | account_name | account_handle | account_url | followers_count | is_active | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Not source phone per someone. | One use on. Plant read tell evening. | Worker talk box option herself part. Phone toni... | http://www.cortez.info/ | 98 | true | Sat Dec 13 2025 03:14:32 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:32 GMT-0600 (Central Stan... |
| 2 | Best call voice new again. | Full religious production bag. Ground behavior ... | There main small those case available listen ea... | http://www.smith.com/ | 76 | true | Sat Dec 13 2025 03:14:32 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:32 GMT-0600 (Central Stan... |
| 3 | Usually central Congress can middle bag stay. | Certain set thus born everything. Within decide... | Laugh per TV by memory ever. Account who center... | https://shannon.com/ | 30 | false | Sat Dec 13 2025 03:14:32 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:32 GMT-0600 (Central Stan... |
| 4 | Report hard its. Second life trial charge. | Offer individual leave final edge. Personal sty... | Change development popular represent. Type mana... | https://johnson.com/ | 100 | true | Sat Dec 13 2025 03:14:32 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:32 GMT-0600 (Central Stan... |
| 5 | One not rule approach economic upon history. | Exist reflect high subject teach now. Including... | Worry people bad set late wrong add. | https://www.austin-holmes.com/ | 77 | true | Sat Dec 13 2025 03:14:32 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:32 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:36.880Z*