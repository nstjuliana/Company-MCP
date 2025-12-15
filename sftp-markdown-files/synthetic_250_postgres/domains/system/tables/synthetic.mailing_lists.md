# mailing_lists

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The "synthetic.mailing_lists" table represents a collection of mailing lists, each defined by attributes such as a unique identifier (list_id), a name (list_name), a description, and metadata regarding its activity status (is_active), number of subscribers (subscriber_count), and timestamps for creation and last update. With no foreign keys or references to other tables, this standalone table likely serves to manage distinct mailing list entities within the application. While the current row count is zero, the provided sample row illustrates potential content and usage for cataloging and organizing mailing lists.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| list_id | integer | NO | This column uniquely identifies each entry in the mailing lists, serving as a sequential identifier for list records. |
| list_name | character varying | NO | This column represents the titles or names of various mailing lists, which appear to be creatively or thematically titled, possibly to capture attention or convey the list's focus or purpose. The titles suggest a diverse range of interests or topics such as TV support, nature, science, or cultural themes. |
| description | text | YES | This column contains textual descriptions related to various topics or activities. The purpose is unclear from the available data. |
| is_active | boolean | YES | This column indicates whether a mailing list is currently active or not, where true means active and false means inactive. The default value is active, suggesting that new entries are presumed active unless specified otherwise. |
| subscriber_count | integer | YES | This column represents the number of individuals who are subscribed to a particular mailing list. Since it is nullable, the count might not always be recorded, but when it is, it reflects figures like those in the sample values, indicating the list's subscriber size. |
| created_at | timestamp without time zone | YES | Indicates the date and time when an entry was added to the mailing list. It automatically records this information unless otherwise specified. |
| updated_at | timestamp without time zone | YES | This column indicates the datetime at which a record in the mailing lists was last modified. The repetition of the same timestamp suggests this was set automatically to the timestamp when each entry was modified, which defaults to the current system timestamp upon update. |

## Primary Key

`list_id`

## Indexes

- `mailing_lists_pkey`: CREATE UNIQUE INDEX mailing_lists_pkey ON synthetic.mailing_lists USING btree (list_id)

## Sample Data

| list_id | list_name | description | is_active | subscriber_count | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Specific TV care support. Card recognize detail... | Early teach artist fight house. Its film than h... | true | 78 | Sat Dec 13 2025 03:14:09 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:09 GMT-0600 (Central Stan... |
| 2 | Seem here at once seek same poor. Plant green s... | Understand eight near loss Congress. Director a... | true | 100 | Sat Dec 13 2025 03:14:09 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:09 GMT-0600 (Central Stan... |
| 3 | Color billion son magazine nature nature. Anima... | Walk conference sea activity almost continue. C... | true | 40 | Sat Dec 13 2025 03:14:09 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:09 GMT-0600 (Central Stan... |
| 4 | Push trip catch. Scientist benefit small agree ... | Box debate move decide. | true | 75 | Sat Dec 13 2025 03:14:09 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:09 GMT-0600 (Central Stan... |
| 5 | People indicate feel entire. Despite identify o... | Seat natural different even vote. Improve forei... | true | 40 | Sat Dec 13 2025 03:14:09 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:09 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:15.133Z*