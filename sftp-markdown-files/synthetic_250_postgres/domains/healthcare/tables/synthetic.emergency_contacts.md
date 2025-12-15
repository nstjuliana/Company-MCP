# emergency_contacts

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "emergency_contacts" table in the "synthetic" schema appears to represent the contact details for emergency contacts associated with employees, identified by the "employee_id" column. It features essential information such as the contact's name, relationship to the employee, primary and secondary phone numbers, and email, serving as a crucial data point in employee emergency management, with relationships inferred to worker or employee tables potentially via the "employee_id." This table's role in the data model allows for organizing and referencing emergency contacts effectively, though it currently does not explicitly relate to other tables.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| contact_id | integer | NO | This column represents a unique identifier assigned sequentially to each emergency contact entry, ensuring distinction between individual records. |
| employee_id | integer | NO | This column represents an identifier uniquely assigned to an employee, used to associate them with emergency contact information. The repeated occurrence of certain values suggests that some employees may have multiple emergency contacts listed. |
| contact_name | character varying | NO | This column represents the names of individuals who serve as emergency contacts for others, typically to be used in situations requiring prompt communication or assistance. The names reflect a diverse range of common first and last names, suggesting no specific demographic focus. |
| relationship | character varying | YES | Purpose unclear from available data. |
| phone_primary | character varying | YES | This column contains the primary contact phone numbers for emergency contacts, reflecting a variety of formats including extensions and international dialing codes. The purpose is to maintain a key communication channel for reaching emergency contacts. |
| phone_secondary | character varying | YES | This column contains secondary phone numbers for emergency contacts, which can include a variety of formats such as international dialing codes, extensions, and different delimiter styles. The numbers appear to be used for contacting individuals during emergencies if the primary phone number is unavailable. |
| email | character varying | YES | This column contains the email addresses of individuals listed as emergency contacts. These email addresses are used for contacting specific persons associated with emergency situations related to the main entity in question. |
| is_primary | boolean | YES | This column indicates whether an emergency contact is designated as the main point of contact for a person. A value of "true" suggests the contact is primary, while "false" indicates they are not. |
| created_at | timestamp without time zone | YES | This column records the date and time when a specific emergency contact record was created. It defaults to capturing the current timestamp at the moment of record creation. |
| updated_at | timestamp without time zone | YES | This column records the date and time when the emergency contact information was last modified or confirmed. It helps track changes or updates to the contact details for accountability and accuracy. |

## Primary Key

`contact_id`

## Foreign Keys

- `employee_id` → `synthetic.employees.employee_id`

## Indexes

- `emergency_contacts_pkey`: CREATE UNIQUE INDEX emergency_contacts_pkey ON synthetic.emergency_contacts USING btree (contact_id)

## Sample Data

| contact_id | employee_id | contact_name | relationship | phone_primary | phone_secondary | email | is_primary | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 21 | Anthony Rodgers | Agent play myself bag east work miss officer. | 267-367-7619x52496 | 409.421.7645x1770 | angelaking@example.com | false | Sat Dec 13 2025 03:20:37 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:20:37 GMT-0600 (Central Stan... |
| 2 | 7 | Elizabeth Wagner | Key price follow couple. | (984)489-8735 | 529.893.3570x240 | mgonzalez@example.net | true | Sat Dec 13 2025 03:20:37 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:20:37 GMT-0600 (Central Stan... |
| 3 | 1 | James Ferguson | Career lawyer one discussion reveal. | +1-276-322-7353x3406 | (763)434-0142x15634 | klewis@example.net | false | Sat Dec 13 2025 03:20:37 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:20:37 GMT-0600 (Central Stan... |
| 4 | 29 | Catherine Robinson | Least exist entire guy respond science. | 449-644-9574x21884 | (438)615-1291x1647 | lroberts@example.net | false | Sat Dec 13 2025 03:20:37 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:20:37 GMT-0600 (Central Stan... |
| 5 | 49 | Wanda Thompson | Rock follow prepare perform month many. | +1-418-634-7923x0578 | 431-608-1246x43786 | juliehuerta@example.net | false | Sat Dec 13 2025 03:20:37 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:20:37 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:40.765Z*