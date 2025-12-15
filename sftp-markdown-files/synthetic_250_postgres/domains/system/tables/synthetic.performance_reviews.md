# performance_reviews

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.performance_reviews` table is designed to store evaluations of employee performance, identifiable by the primary key `review_id`. This table is intended to interact with other unidentified tables through foreign key relationships, potentially linking employee details or departmental data. Despite its current lack of row data and column details, its primary function seems to organize and reference performance-related metrics within the broader database schema.

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| review_id | integer | NO | Represents the unique identifier assigned to each record in the employee performance reviews table. |
| employee_id | integer | NO | This column represents unique identifiers assigned to employees whose performance reviews are recorded in the database. The purpose of this column is to link each performance review to the specific employee it evaluates. |
| reviewer_id | integer | NO | This column uniquely identifies individuals responsible for conducting performance reviews. Purpose unclear from available data beyond serving as an identifier. |
| review_period_start | date | YES | This column indicates the starting date of the period covered in an employee's performance review. It is used to specify when the evaluation timeframe begins. |
| review_period_end | date | YES | This column indicates the concluding date of an evaluated period for an employee's performance review. Purpose unclear from available data. |
| review_date | date | YES | This column represents the date on which an individual's performance review was conducted. Purpose unclear from available data. |
| overall_rating | numeric | YES | Purpose unclear from available data. |
| goals_met_percentage | integer | YES | This column likely represents the percentage of goals achieved by an individual or team during a performance evaluation period. Purpose unclear from available data due to lack of sample values. |
| comments | text | YES | Purpose unclear from available data. |
| status | character varying | YES | This column likely indicates the progress or approval stage of performance reviews, with the initial status being 'draft'. Note that further specifics about the stages are not available. |
| created_at | timestamp without time zone | YES | The column records the date and time when a new entry is added to the performance reviews table, capturing when the performance review was created. The purpose of tracking this information in the context of performance reviews may involve monitoring the timeliness and recency of evaluations. |
| updated_at | timestamp without time zone | YES | This column records the date and time when a performance review entry was last modified, allowing for tracking updates to employee evaluations. If no updates have occurred, it captures the initial creation timestamp. |

## Primary Key

`review_id`

## Foreign Keys

- `employee_id` → `synthetic.employees.employee_id`
- `reviewer_id` → `synthetic.employees.employee_id`

## Indexes

- `performance_reviews_pkey`: CREATE UNIQUE INDEX performance_reviews_pkey ON synthetic.performance_reviews USING btree (review_id)

*Generated at: 2025-12-14T23:39:23.622Z*