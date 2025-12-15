# vendors

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.vendors` table represents a business entity that stores detailed information about vendors, including identifiers such as `vendor_id` and `vendor_code`, contact information like `contact_name` and `email`, and logistical details such as `address`, `city`, and `country`. This table serves as a repository for vendor management, potentially supporting functionalities like procurement or partner relations by recording `tax_id`, `payment_terms`, and status through `is_active`. While it currently has no relationships with other tables, it serves as a standalone catalog pivotal for managing vendor data within the database.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| vendor_id | integer | NO | This column represents a unique identifier assigned to each vendor entry within the database. It ensures that each vendor can be distinctly recognized and referenced. |
| vendor_code | character varying | YES | This column represents a unique identifier for vendors in the system. The specific purpose or format of these identifiers is unclear from the available data. |
| vendor_name | character varying | NO | This column represents the names of various vendor entities, which could be businesses, partnerships, or individual providers. The names suggest a formal listing of suppliers or contractors engaging in transactions or services. |
| contact_name | character varying | YES | This column represents the names of individuals associated with vendors, likely serving as primary contact persons. It captures the first and last names of these contact individuals. |
| email | character varying | YES | This column represents the contact email addresses for various vendors. It includes a range of email domains, possibly indicating personal or organizational email addresses associated with vendor contacts. |
| phone | character varying | YES | This column stores the contact numbers for vendors, which may include country codes and extensions, formatted in various ways such as dashes, parentheses, or dots. Purpose unclear from available data. |
| address_line1 | character varying | YES | This column represents the primary address or location details of vendors, including street names, numbers, and apartment or suite identifiers. It captures detailed physical addresses necessary for contact and correspondence purposes within the vendor management context. |
| city | character varying | YES | This column lists the names of cities where vendors are based or operate. It helps identify the geographic locations associated with the vendors. |
| state | character varying | YES | This column represents the U.S. state where a vendor is located or operates. The specific purpose of tracking this location data is unclear from the available information. |
| postal_code | character varying | YES | This column represents the postal codes associated with the addresses of vendors, allowing identification of geographic regions within a mailing address. The purpose is unclear from available data but likely relates to location-based categorization or shipping processes. |
| country | character varying | YES | This column represents the name of the country associated with each vendor, indicating the vendor's geographical location or operational base. Purpose unclear from available data. |
| tax_id | character varying | YES | Purpose unclear from available data. |
| payment_terms | character varying | YES | Purpose unclear from available data. |
| is_active | boolean | YES | Indicates whether a vendor is currently active, with true representing active status and false representing inactive status. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column captures the date and time when a record was created in the vendors table. It defaults to the current timestamp, indicating the initial entry point for each vendor's information. |
| updated_at | timestamp without time zone | YES | Records the date and time when the vendor information was last updated, using the default current timestamp if unspecified. Purpose unclear from available data if it involves further status tracking or auditing functions. |

## Primary Key

`vendor_id`

## Indexes

- `vendors_pkey`: CREATE UNIQUE INDEX vendors_pkey ON synthetic.vendors USING btree (vendor_id)
- `vendors_vendor_code_key`: CREATE UNIQUE INDEX vendors_vendor_code_key ON synthetic.vendors USING btree (vendor_code)

## Sample Data

| vendor_id | vendor_code | vendor_name | contact_name | email | phone | address_line1 | city | state | postal_code | country | tax_id | payment_terms | is_active | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ZUVGNOQIBL | Ramos-Brown | Laurie Giles | kellysmith@example.com | 235-596-6533 | 85743 Cassidy Radial Suite 800 | Port Angelaville | Montana | 19062 | Pitcairn Islands | Maintain analysis require issue drop building. | Test guess respond risk week home. | true | Sat Dec 13 2025 02:54:25 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:25 GMT-0600 (Central Stan... |
| 2 | BINKAGYWGM | Kelley, Munoz and Sullivan | Kirk York | antonio51@example.net | 001-326-877-5046 | 284 Jessica Spring | Reedside | West Virginia | 83922 | Moldova | Six clearly central about suddenly watch without. | Expect heavy far education size. | true | Sat Dec 13 2025 02:54:25 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:25 GMT-0600 (Central Stan... |
| 3 | LXWAJDDJON | Whitney Ltd | Elizabeth Gonzalez | roger42@example.com | 001-429-643-6109x098 | 81464 Williams Villages Apt. 607 | Danielton | Nevada | 02172 | Chad | Guy friend traditional dark. Could sea late cost. | Have quickly benefit easy within pass go. | true | Sat Dec 13 2025 02:54:25 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:25 GMT-0600 (Central Stan... |
| 4 | ZNOGBWWIKZ | Henderson, Guerrero and Gomez | Breanna Brown | rmitchell@example.net | (276)347-8562x50845 | 99925 Andrade Prairie Apt. 861 | East Abigailmouth | Wisconsin | 14534 | El Salvador | More teach focus four action. | Strategy brother several business stuff social. | true | Sat Dec 13 2025 02:54:25 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:25 GMT-0600 (Central Stan... |
| 5 | VMABFOAUQI | Cain and Sons | Kelsey Smith | dwalsh@example.com | 001-321-991-0507 | 574 Bailey Squares | Angelchester | Pennsylvania | 15752 | Tuvalu | Easy lawyer its debate poor. | Respond despite white way. | true | Sat Dec 13 2025 02:54:25 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:25 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:31.431Z*