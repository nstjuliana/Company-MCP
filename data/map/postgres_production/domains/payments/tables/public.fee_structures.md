# fee_structures

**Database:** postgres_production
**Schema:** public
**Description:** This table stores fee structure configurations for payment processing, with each record containing a unique fee_id and detailed fee parameters stored as JSON in the fee_data column including card scheme types, rates, fixed amounts, and merchant category codes. The table appears to be a standalone reference table for payment fee calculations, as it has no foreign key relationships with other tables. Based on the sample data, it serves as a configuration store for different payment processing fee structures that can be applied based on various criteria like card scheme (e.g., "TransactPlus"), merchant category codes, and transaction characteristics.

**Row Count:** 1,000

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| fee_id | integer | NO | A unique identifier that automatically assigns sequential numbers to distinguish each fee structure record. Based on the sample values, this appears to be the primary means of referencing individual fee configurations within the system. |
| fee_data | jsonb | YES | Purpose unclear from available data. Contains structured configuration or parameter information related to fee calculations, but the specific content and business meaning cannot be determined from the object references shown. |
| created_at | timestamp without time zone | YES | Records the timestamp when each fee structure record was initially inserted into the database. Automatically captures the creation time for audit trail and chronological tracking purposes. |

## Primary Key

`fee_id`

## Indexes

- `fee_structures_pkey`: CREATE UNIQUE INDEX fee_structures_pkey ON public.fee_structures USING btree (fee_id)

## Sample Data

| fee_id | fee_data | created_at |
| --- | --- | --- |
| 1 | [object Object] | Tue Dec 09 2025 21:38:09 GMT-0600 (Central Stan... |
| 2 | [object Object] | Tue Dec 09 2025 21:38:09 GMT-0600 (Central Stan... |
| 3 | [object Object] | Tue Dec 09 2025 21:38:09 GMT-0600 (Central Stan... |
| 4 | [object Object] | Tue Dec 09 2025 21:38:09 GMT-0600 (Central Stan... |
| 5 | [object Object] | Tue Dec 09 2025 21:38:09 GMT-0600 (Central Stan... |

*Generated at: 2025-12-11T22:51:36.013Z*