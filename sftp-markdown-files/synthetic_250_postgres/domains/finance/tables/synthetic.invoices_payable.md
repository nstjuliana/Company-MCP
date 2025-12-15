# invoices_payable

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.invoices_payable` table represents accounts payable invoices within a business entity that tracks financial obligations to vendors. With `invoice_id` as the primary key, it captures details such as invoice numbers, vendor identifiers, invoice and due dates, and financial amounts like total and tax in specific currencies, which indicates its role in managing vendor payments. Its relationship with other tables is minimal, featuring an undefined foreign key relationship, suggesting a focus on internal financial transaction recording rather than wider data model integration.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| invoice_id | integer | NO | This column uniquely identifies each payable invoice in the invoices database through sequential numbering. Each number corresponds to a specific invoice, ensuring distinct traceability and reference for financial transactions. |
| invoice_number | character varying | NO | This column represents unique identifiers assigned to invoices awaiting payment, each consisting of a large, distinct numerical sequence to ensure identification. These identifiers are essential for tracking and managing invoice-related transactions in the accounts payable process. |
| vendor_id | integer | NO | This column likely represents a unique identifier assigned to various vendors involved in transactions related to invoices payable. These identifiers allow for distinguishing and referencing specific vendors within the financial operations of the entity. |
| invoice_date | date | NO | Represents the date an invoice is issued or becomes payable. This field is always populated and indicates the timeline for payment obligations. |
| due_date | date | YES | This column represents the date by which an invoice is expected to be paid. The values suggest that the dates are adjusted for Central Time, accounting for both standard and daylight savings time changes. |
| total_amount | numeric | NO | This column represents the total monetary value owed for each invoice that the business needs to pay. It reflects sizable amounts that suggest these are significant financial obligations, likely involving substantial purchases or services. |
| tax_amount | numeric | YES | This column represents the monetary value of taxes that are associated with each payable invoice. The amounts typically reach into tens of thousands, indicating possibly substantial business transactions or a high tax rate. |
| currency | character varying | YES | This column denotes the currency used for each transaction, indicating the type of money in which the payable invoice is recorded. The default currency is US Dollars, though other currencies like Japanese Yen, British Pounds, and Canadian Dollars are also present. |
| status | character varying | YES | This column indicates the current processing state of an invoice, such as whether it is pending, completed, or cancelled. It helps track the invoice's lifecycle status in the payment process for payable accounts. |
| payment_date | date | YES | This column indicates the scheduled date on which outstanding invoices are expected to be paid. It accommodates instances where no payment date has been determined yet, as it allows for null values. |
| notes | text | YES | This column contains free-form annotations or comments pertaining to invoices that may include descriptions of events, actions, or thoughts related to the invoice processing. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when an invoice was created or recorded in the system. The time reflects the Central Standard Time zone. |
| updated_at | timestamp without time zone | YES | This column records the date and time of the most recent update to an invoice entry. The value defaults to the current time when an update occurs, indicating the last modification timestamp. |

## Primary Key

`invoice_id`

## Foreign Keys

- `vendor_id` → `synthetic.vendors.vendor_id`

## Indexes

- `invoices_payable_pkey`: CREATE UNIQUE INDEX invoices_payable_pkey ON synthetic.invoices_payable USING btree (invoice_id)

## Sample Data

| invoice_id | invoice_number | vendor_id | invoice_date | due_date | total_amount | tax_amount | currency | status | payment_date | notes | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 51374028265652936756 | 15 | Sat Apr 20 2024 00:00:00 GMT-0500 (Central Dayl... | Sat Sep 07 2024 00:00:00 GMT-0500 (Central Dayl... | 41439.98 | 82759.18 | JPY | completed | Thu Jun 13 2024 00:00:00 GMT-0500 (Central Dayl... | Doctor figure plant. Series wife east large per... | Sat Dec 13 2025 02:54:29 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:29 GMT-0600 (Central Stan... |
| 2 | 42209470544765839018 | 47 | Tue May 27 2025 00:00:00 GMT-0500 (Central Dayl... | Mon Nov 18 2024 00:00:00 GMT-0600 (Central Stan... | 9599.08 | 42733.72 | GBP | pending | Sat Jun 28 2025 00:00:00 GMT-0500 (Central Dayl... | Strong artist tax memory. Toward chair that lat... | Sat Dec 13 2025 02:54:29 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:29 GMT-0600 (Central Stan... |
| 3 | 94804688698908763427 | 10 | Thu Apr 11 2024 00:00:00 GMT-0500 (Central Dayl... | Mon Oct 28 2024 00:00:00 GMT-0500 (Central Dayl... | 68713.42 | 47479.36 | USD | active | Sat Nov 16 2024 00:00:00 GMT-0600 (Central Stan... | Knowledge lay lose wall be threat. Stuff idea a... | Sat Dec 13 2025 02:54:29 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:29 GMT-0600 (Central Stan... |
| 4 | 67138731403191666162 | 6 | Fri Jul 26 2024 00:00:00 GMT-0500 (Central Dayl... | Thu Apr 17 2025 00:00:00 GMT-0500 (Central Dayl... | 43244.46 | 74484.44 | GBP | inactive | Fri Sep 27 2024 00:00:00 GMT-0500 (Central Dayl... | Rich poor it they hotel very away. Conference l... | Sat Dec 13 2025 02:54:29 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:29 GMT-0600 (Central Stan... |
| 5 | 67071671489579257852 | 36 | Tue Apr 30 2024 00:00:00 GMT-0500 (Central Dayl... | Mon Jul 29 2024 00:00:00 GMT-0500 (Central Dayl... | 6092.10 | 95666.80 | CAD | pending | Sun Mar 31 2024 00:00:00 GMT-0500 (Central Dayl... | Wonder ago per factor. Development kid economy ... | Sat Dec 13 2025 02:54:29 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:29 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:40:03.104Z*