# accounts

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.accounts` table represents business accounts, capturing details such as account name, type, industry, contact information, employee count, and annual revenue. It primarily identifies accounts through a unique `account_id` and is not directly referenced by other tables, suggesting a standalone role in the data model. The table also includes metadata fields like `created_at` and `updated_at` to track record changes, and it accommodates account hierarchy via a nullable `parent_account_id`.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| account_id | integer | NO | This column uniquely identifies each account in the system, with sequential numeric values indicating the order of creation. It serves as a central identifier for account-related records. |
| account_name | character varying | NO | This column represents descriptive phrases or narrative text likely used for labeling or describing entities or activities within accounts. Purpose unclear from available data. |
| account_type | character varying | YES | This column appears to categorize accounts based on different themes or characteristics, such as ownership, usage purpose, associated roles, or storing functionalities. Purpose unclear from available data due to varied sample values. |
| industry | character varying | YES | Purpose unclear from available data. |
| website | character varying | YES | This column contains the URLs for the websites associated with various accounts. It likely serves as a contact or information point for these online business or personal entities. |
| phone | character varying | YES | This column contains contact phone numbers associated with customer accounts. The numbers are in various formats, including those with extensions, indicating multiple possible formats for phone entries. |
| fax | character varying | YES | This column contains fax numbers associated with accounts, often with additional extension numbers indicated. The numbers are formatted in various ways, including parentheses, dashes, and dots, reflecting a diversity of regions or styles. |
| employees_count | integer | YES | This column likely represents the number of employees associated with each account in the system. It captures employee counts ranging from small to relatively large numbers, as demonstrated by the sample values provided. |
| annual_revenue | numeric | YES | This column represents the total revenue generated annually by an account, which is expressed in monetary terms as evidenced by the sample values provided. The purpose is to capture financial performance data for each account year-over-year. |
| billing_address | text | YES | This column lists the mailing addresses associated with individual or entity accounts, capturing both domestic and military-based locations as illustrated by full addresses including street and suite numbers, city, state abbreviations, and postal codes. Purpose unclear from available data. |
| shipping_address | text | YES | This column contains the full shipping addresses, including street, city, state, and zip code, for the accounts in the system. These addresses represent locations where items can be delivered to account holders. |
| description | text | YES | This column contains various text entries that appear to represent statements or reflections, possibly related to projects, concepts, and personal or organizational experiences. The exact purpose of these texts is unclear from the available data. |
| owner_id | integer | YES | This column likely represents an identifier for an individual or entity that owns or is associated with each account record. The exact nature of the relationship is unclear from the data provided. |
| parent_account_id | integer | YES | This column signifies a linkage to another account, possibly representing an organizational hierarchy or grouping of accounts. Its purpose is unclear from the available data but likely involves identifying a connection or categorization between accounts. |
| is_active | boolean | YES | This column indicates whether an account is currently active. The default setting suggests accounts are generally expected to be active unless specified otherwise. |
| created_at | timestamp without time zone | YES | This column represents the date and time when an account was created, defaulting to the current timestamp at creation. The purpose is to track the inception of account records but its nullable nature suggests it can be optionally recorded or adjusted. |
| updated_at | timestamp without time zone | YES | This column records the date and time when an account was last modified or updated. The sample values suggest routine updates occurring at the same timestamp, indicative of synchronization or batch processing. |

## Primary Key

`account_id`

## Foreign Keys

- `parent_account_id` → `synthetic.accounts.account_id`

## Indexes

- `accounts_pkey`: CREATE UNIQUE INDEX accounts_pkey ON synthetic.accounts USING btree (account_id)

## Sample Data

| account_id | account_name | account_type | industry | website | phone | fax | employees_count | annual_revenue | billing_address | shipping_address | description | owner_id | parent_account_id | is_active | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Rise black natural daughter need talk series. C... | new | Feel picture city development. Site past lose a... | http://hogan.com/ | +1-641-619-9039 | (901)765-8592x6455 | 102 | 542.37 | USNV Elliott, FPO AP 62776 | 7049 Tara Corners Apt. 799, Port Travis, PW 40652 | Model age project recently. Nothing brother boa... | 3523 | null | false | Sat Dec 13 2025 02:58:25 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:25 GMT-0600 (Central Stan... |
| 2 | Feeling local draw figure. Plant child month ne... | owner | Whole serious way realize morning character. We... | https://www.hunter.com/ | 762-830-1180 | 9996262098 | 307 | 569.33 | 893 Reed Meadow Apt. 119, Jamesborough, VA 18308 | 177 Pugh Wall Suite 569, East Jamesberg, TX 05853 | Away let project drug church check. Open trip e... | 9531 | 1 | true | Sat Dec 13 2025 02:58:25 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:25 GMT-0600 (Central Stan... |
| 3 | Two fact into nothing as learn reach western. A... | purpose | Reality cost behind worker.
See more my system. | http://www.green.biz/ | (454)509-3923 | 414-811-5440x9426 | 737 | 886.52 | 45684 Blair Corners Suite 544, North Amyland, M... | 1669 Dana Lodge, Amberland, PW 94440 | Every remember total enough recently Mr often. ... | 3192 | 2 | true | Sat Dec 13 2025 02:58:25 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:25 GMT-0600 (Central Stan... |
| 4 | Break determine get that executive magazine. Pa... | role | Your president degree ok. Put well rule degree ... | https://chang.info/ | 8095589900 | 618-313-1287x19485 | 257 | 754.56 | 1770 Donna Pines Apt. 250, East Timothy, WI 93478 | 91899 Little Trafficway Suite 036, New Amanda, ... | Past floor face lose happen. While Congress way... | 9853 | 2 | false | Sat Dec 13 2025 02:58:25 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:25 GMT-0600 (Central Stan... |
| 5 | Father follow energy social affect. Culture wal... | various | Establish instead other anything find. Allow su... | http://www.long.com/ | 001-744-502-0939x103 | 001-591-239-8336x649 | 646 | 176.53 | 91097 Thomas Key Suite 746, West Andrewbury, NY... | 04646 Dylan Parkway, Seanborough, WI 47889 | Do before quite technology represent specific a... | 8312 | 4 | false | Sat Dec 13 2025 02:58:25 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:58:25 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:03.717Z*