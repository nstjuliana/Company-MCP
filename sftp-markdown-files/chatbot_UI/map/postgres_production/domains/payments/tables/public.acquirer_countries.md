# acquirer_countries

**Database:** postgres_production
**Schema:** public
**Description:** The `acquirer_countries` table stores a registry of country codes where payment acquirers operate, with each country identified by a two-letter country code (such as "GB" for Great Britain) serving as the primary key and including a creation timestamp. This table appears to function as a reference or lookup table for supported acquirer countries within a payment processing system. The table currently has no foreign key relationships, suggesting it serves as a standalone reference entity that may be used by other payment-related tables in the broader data model.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| country_code | character varying | NO | Stores two-letter country identifiers representing the countries where acquiring entities are located or operate. Based on the sample values, this includes major European markets (Great Britain, Netherlands, Italy, France) and the United States. |
| created_at | timestamp without time zone | YES | Records the date and time when each acquirer country record was initially added to the system. All sample entries show the same timestamp, suggesting they were created during a batch data loading process. |

## Primary Key

`country_code`

## Indexes

- `acquirer_countries_pkey`: CREATE UNIQUE INDEX acquirer_countries_pkey ON public.acquirer_countries USING btree (country_code)

## Sample Data

| country_code | created_at |
| --- | --- |
| GB | Tue Dec 09 2025 21:38:08 GMT-0600 (Central Stan... |
| US | Tue Dec 09 2025 21:38:08 GMT-0600 (Central Stan... |
| NL | Tue Dec 09 2025 21:38:08 GMT-0600 (Central Stan... |
| IT | Tue Dec 09 2025 21:38:08 GMT-0600 (Central Stan... |
| FR | Tue Dec 09 2025 21:38:08 GMT-0600 (Central Stan... |

*Generated at: 2025-12-11T22:51:35.587Z*