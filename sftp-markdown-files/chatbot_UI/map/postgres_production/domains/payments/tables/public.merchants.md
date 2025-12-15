# merchants

**Database:** postgres_production
**Schema:** public
**Description:** This table represents merchant entities in the system, storing basic information about businesses or service providers that likely process transactions or offer services. Each merchant is uniquely identified by a merchant_id (as evidenced by "Crossfit_Hanna" in the sample data) and includes a timestamp tracking when the merchant record was created. The table appears to serve as a foundational entity in the data model, though it currently has no established relationships with other tables in the database.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| merchant_id | character varying | NO | Unique identifier for business establishments including restaurants, fitness centers, bookstores, golf clubs, and other retail merchants. Based on the sample data, appears to use business names formatted with underscores replacing spaces. |
| created_at | timestamp without time zone | YES | Records the date and time when a merchant record was first created in the system. Automatically captures the timestamp of merchant registration or onboarding. |

## Primary Key

`merchant_id`

## Indexes

- `merchants_pkey`: CREATE UNIQUE INDEX merchants_pkey ON public.merchants USING btree (merchant_id)

## Sample Data

| merchant_id | created_at |
| --- | --- |
| Crossfit_Hanna | Tue Dec 09 2025 21:38:08 GMT-0600 (Central Stan... |
| Martinis_Fine_Steakhouse | Tue Dec 09 2025 21:38:08 GMT-0600 (Central Stan... |
| Belles_cookbook_store | Tue Dec 09 2025 21:38:08 GMT-0600 (Central Stan... |
| Golfclub_Baron_Friso | Tue Dec 09 2025 21:38:08 GMT-0600 (Central Stan... |
| Rafa_AI | Tue Dec 09 2025 21:38:08 GMT-0600 (Central Stan... |

*Generated at: 2025-12-11T22:51:34.981Z*