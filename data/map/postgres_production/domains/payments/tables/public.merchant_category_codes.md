# merchant_category_codes

**Database:** postgres_production
**Schema:** public
**Description:** This table stores a reference catalog of Merchant Category Codes (MCCs) used to classify different types of businesses and merchants, with each record containing a unique 4-digit MCC code, its corresponding category description, and creation timestamp. The table serves as a standalone lookup/reference table with no foreign key relationships, indicating it functions as a master data source for MCC classifications that would typically be referenced by transaction or merchant-related tables elsewhere in the system. Based on the sample data showing code "1520" for "General Contractors - Residential and Commercial," this appears to follow standard industry MCC classification schemes used in payment processing and financial systems.

**Row Count:** 769

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| mcc_code | character varying | NO | Four-digit numeric codes that classify different types of merchant businesses or industries, with sample values representing various commercial sectors such as construction (1700s range) and publishing/printing (2700s range). These standardized codes are used to categorize merchants for payment processing and transaction classification purposes. |
| category_description | text | YES | Contains detailed textual descriptions of business categories and industries, primarily focused on construction trades, contractors, and publishing services that merchants operate within. |
| created_at | timestamp without time zone | YES | Records when each merchant category code entry was initially added to the system. Based on the sample data showing identical timestamps, this appears to track bulk data creation events. |

## Primary Key

`mcc_code`

## Indexes

- `merchant_category_codes_pkey`: CREATE UNIQUE INDEX merchant_category_codes_pkey ON public.merchant_category_codes USING btree (mcc_code)

## Sample Data

| mcc_code | category_description | created_at |
| --- | --- | --- |
| 1520 | General Contractors - Residential and Commercial | Tue Dec 09 2025 21:38:07 GMT-0600 (Central Stan... |
| 1711 | Heating, Plumbing, and Air Conditioning Contrac... | Tue Dec 09 2025 21:38:07 GMT-0600 (Central Stan... |
| 1731 | Electrical Contractors | Tue Dec 09 2025 21:38:07 GMT-0600 (Central Stan... |
| 1740 | Masonry, Stonework, Tile-Setting, Plastering, a... | Tue Dec 09 2025 21:38:07 GMT-0600 (Central Stan... |
| 1750 | Carpentry Contractors | Tue Dec 09 2025 21:38:07 GMT-0600 (Central Stan... |

*Generated at: 2025-12-11T22:51:37.124Z*