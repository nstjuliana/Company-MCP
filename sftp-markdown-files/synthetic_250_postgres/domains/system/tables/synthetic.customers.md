# customers

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.customers" table represents customer profiles within a business entity, capturing essential information such as personal details (e.g., name, email, and phone), authentication (password hash), and activity metrics (e.g., registration and last login dates). It tracks customer status with fields like "is_verified" and "is_active," financial interaction through "total_orders" and "total_spent," and timestamps for record management. This table serves as a standalone entity holding customer-centric data with no direct relationships to other tables in the database.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| customer_id | integer | NO | This column represents a unique identifier for each customer, used to differentiate them within the database. The values indicate sequential numbering for customer records. |
| email | character varying | NO | The column contains the email addresses of customers, serving as a unique identifier and primary means of electronic communication for each customer within the database. |
| password_hash | character varying | YES | This column stores the hashed version of customers' passwords, ensuring security by not retaining their actual passwords. Purpose unclear from available data. |
| first_name | character varying | YES | This column contains the given names of individuals, likely representing customers. The purpose appears to be storing first names for identification or personalization purposes in a business context. |
| last_name | character varying | YES | Represents the family or surname of individuals within the customer dataset. This information is used to identify and organize customer records systematically. |
| phone | character varying | YES | This column contains contact numbers for customers, which may include international dialing codes and extension numbers. The variety in formatting suggests the data encompasses both domestic and international phone numbers. |
| date_of_birth | date | YES | This column represents the birth dates of individuals in the customers table, indicating when they were born. The inclusion of date values in both standard and daylight saving time reflects time zone variations. |
| gender | character varying | YES | This column represents the gender identity of customers, with possible values including female, male, and other. Purpose unclear from available data. |
| registration_date | timestamp without time zone | YES | This column stores the date and time when a customer completed their registration process. It helps track customer onboarding by capturing the moment they become registered users on the system. |
| last_login | timestamp without time zone | YES | This column indicates the most recent date and time a customer accessed their account, reflecting both daylight saving and standard time adjustments. Purpose unclear from available data. |
| is_verified | boolean | YES | This column indicates whether a customer's status has been confirmed and approved. The default assumption is that a customer is not verified unless explicitly marked as verified. |
| is_active | boolean | YES | Indicates whether a customer is currently considered active or inactive, with "true" representing active status. A significant portion of customers appear to be inactive based on the provided sample values. |
| customer_tier | character varying | YES | Purpose unclear from available data. |
| total_orders | integer | YES | This column represents the total number of orders made by a customer, where higher values indicate more frequent purchases. The purpose of these recorded values is not explicitly clear from the available data. |
| total_spent | numeric | YES | This column represents the total monetary value that each customer has spent over their purchasing history. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a customer's record was first created in the system. The exact purpose of storing the creation timestamp is unclear from the available data. |
| updated_at | timestamp without time zone | YES | Indicates the most recent date and time when a customer's record was modified. The purpose is to track updates to customer information. |

## Primary Key

`customer_id`

## Indexes

- `customers_email_key`: CREATE UNIQUE INDEX customers_email_key ON synthetic.customers USING btree (email)
- `customers_pkey`: CREATE UNIQUE INDEX customers_pkey ON synthetic.customers USING btree (customer_id)

## Sample Data

| customer_id | email | password_hash | first_name | last_name | phone | date_of_birth | gender | registration_date | last_login | is_verified | is_active | customer_tier | total_orders | total_spent | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | fmorales@example.org | 34aae1fb33bb7c3ca07197ee015b2011aea544942373ce7... | Debra | Snow | 001-897-970-3127x271 | Thu Feb 20 2025 00:00:00 GMT-0600 (Central Stan... | female | Wed Aug 21 2024 13:47:55 GMT-0500 (Central Dayl... | Thu Jun 19 2025 20:16:58 GMT-0500 (Central Dayl... | true | true | On minute candidate. | 8982 | 373.64 | Sat Dec 13 2025 02:55:39 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:39 GMT-0600 (Central Stan... |
| 2 | samanthaboyd@example.org | f0b174a56ad64c914a3218f5b90dcb96e10e3db292012c3... | Brian | Hudson | 756-767-6845x3811 | Thu Apr 24 2025 00:00:00 GMT-0500 (Central Dayl... | female | Thu Jun 26 2025 16:45:53 GMT-0500 (Central Dayl... | Sun Nov 09 2025 15:29:36 GMT-0600 (Central Stan... | false | false | Likely close bit. | 4095 | 163.27 | Sat Dec 13 2025 02:55:39 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:39 GMT-0600 (Central Stan... |
| 3 | garciaronnie@example.org | d5ce6234b88bfdeeda9e0a1012d8ff16ae53de0425e4e91... | Ryan | Smith | +1-787-612-8849x640 | Thu May 02 2024 00:00:00 GMT-0500 (Central Dayl... | other | Mon Aug 26 2024 07:47:00 GMT-0500 (Central Dayl... | Thu Dec 14 2023 20:53:00 GMT-0600 (Central Stan... | false | false | My point financial. | 3615 | 262.98 | Sat Dec 13 2025 02:55:39 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:39 GMT-0600 (Central Stan... |
| 4 | xphillips@example.net | 59dad8d593d0a89bf72a02d9f57ce969e69011dc2f8d28a... | Trevor | Rodriguez | (630)762-7432x92201 | Fri Mar 14 2025 00:00:00 GMT-0500 (Central Dayl... | female | Fri Oct 18 2024 13:20:43 GMT-0500 (Central Dayl... | Sun Jun 23 2024 23:12:53 GMT-0500 (Central Dayl... | true | false | Three rate. | 4665 | 648.46 | Sat Dec 13 2025 02:55:39 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:39 GMT-0600 (Central Stan... |
| 5 | joyflores@example.org | df0bdc2c5ba0c5bb7dbd6e94c1445d1b8a0f1815d98afc3... | Sherry | Arroyo | 448-291-2478x530 | Wed Feb 05 2025 00:00:00 GMT-0600 (Central Stan... | other | Wed Mar 20 2024 07:40:46 GMT-0500 (Central Dayl... | Mon Nov 24 2025 21:36:51 GMT-0600 (Central Stan... | false | false | Establish player. | 3081 | 853.48 | Sat Dec 13 2025 02:55:39 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:55:39 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:07.060Z*