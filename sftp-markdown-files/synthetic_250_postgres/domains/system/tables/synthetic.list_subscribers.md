# list_subscribers

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.list_subscribers` table represents a record of individuals who have subscribed to various lists, with fields capturing their contact information, subscription status, and timestamps for relevant actions. Each subscriber is uniquely identified by the `subscriber_id` and associated with a particular list through the `list_id` column, although specific relationships to other tables are not explicitly defined. This table plays a crucial role in tracking subscription lifecycle and activity, evidenced by fields such as `email`, `subscribed_at`, `unsubscribed_at`, and `status`.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| subscriber_id | integer | NO | This column uniquely identifies each subscriber within the list. Each integer value represents an individual subscriber record sequentially. |
| list_id | integer | NO | Represents unique identifiers for different lists to which subscribers are associated. Each number corresponds to a distinct list. |
| email | character varying | NO | This column contains the contact email addresses of individuals subscribed to a particular list, likely for communication or marketing purposes. Each entry ensures the identification and reachability of subscribers within the system. |
| first_name | character varying | YES | This column likely represents the given names of individuals who are subscribed to a list, as indicated by the sample values that are typical first names. Purpose unclear from available data. |
| last_name | character varying | YES | This column contains the family names of individuals who are part of a subscription list. Purpose unclear from available data. |
| subscribed_at | timestamp without time zone | YES | This column represents the date and time when a user subscribed to a list or service. The timestamps indicate various times across different dates, reflecting when the subscription action was recorded. |
| unsubscribed_at | timestamp without time zone | YES | This column indicates the date and time when a subscriber opted out or was removed from a mailing list. The purpose of recording this timestamp is likely for tracking user engagement and managing subscription statuses. |
| status | character varying | YES | This column represents the current state of a subscriber's relationship with a list, indicating whether their participation is 'active', 'inactive', or 'pending'. The default state for a new subscriber is 'active'. |
| source | character varying | YES | This column appears to capture textual descriptions or statements, possibly narratives or reflections, that could be related to user-generated content or interactions. Purpose unclear from available data. |
| created_at | timestamp without time zone | YES | This column records the date and time when a subscriber's information was added or updated in the list, reflecting their signup or modification timestamp. The times are stored in Central Standard Time, indicating regional relevance for the subscriber data. |
| updated_at | timestamp without time zone | YES | This column likely records the last time when a subscriber's information was updated, utilizing the current date and time as a default value. The timestamp value suggests that it tracks updates in Central Standard Time. |

## Primary Key

`subscriber_id`

## Foreign Keys

- `list_id` → `synthetic.mailing_lists.list_id`

## Indexes

- `list_subscribers_pkey`: CREATE UNIQUE INDEX list_subscribers_pkey ON synthetic.list_subscribers USING btree (subscriber_id)

## Sample Data

| subscriber_id | list_id | email | first_name | last_name | subscribed_at | unsubscribed_at | status | source | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 20 | karen33@example.org | Christy | Brown | Sat Jan 06 2024 00:18:14 GMT-0600 (Central Stan... | Tue May 20 2025 14:48:42 GMT-0500 (Central Dayl... | inactive | Involve all raise trip several technology. Empl... | Sat Dec 13 2025 03:14:12 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:12 GMT-0600 (Central Stan... |
| 2 | 15 | fbass@example.org | Amy | Vega | Thu Aug 01 2024 21:40:34 GMT-0500 (Central Dayl... | Sat May 18 2024 11:37:55 GMT-0500 (Central Dayl... | active | I baby role like interesting. Member shake impa... | Sat Dec 13 2025 03:14:12 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:12 GMT-0600 (Central Stan... |
| 3 | 47 | melissa54@example.com | Erin | Hanson | Wed Oct 16 2024 21:49:17 GMT-0500 (Central Dayl... | Sat Oct 11 2025 12:29:48 GMT-0500 (Central Dayl... | active | Area attack then mother heavy. Machine late dur... | Sat Dec 13 2025 03:14:12 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:12 GMT-0600 (Central Stan... |
| 4 | 21 | kristacastillo@example.org | Mary | Gay | Wed Jan 08 2025 20:53:10 GMT-0600 (Central Stan... | Wed Jun 11 2025 14:21:51 GMT-0500 (Central Dayl... | active | Speak father last mouth. Throw pattern thousand... | Sat Dec 13 2025 03:14:12 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:12 GMT-0600 (Central Stan... |
| 5 | 48 | hardinkaitlin@example.net | Oscar | Gilbert | Tue Dec 26 2023 00:28:29 GMT-0600 (Central Stan... | Sat Sep 27 2025 07:26:04 GMT-0500 (Central Dayl... | pending | Whether produce tree. | Sat Dec 13 2025 03:14:12 GMT-0600 (Central Stan... | Sat Dec 13 2025 03:14:12 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:39:14.606Z*