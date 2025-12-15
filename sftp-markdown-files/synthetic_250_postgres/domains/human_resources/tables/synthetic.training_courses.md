# training_courses

**Database:** synthetic_250_postgres
**Schema:** synthetic
**Description:** The `synthetic.training_courses` table represents a catalog of training courses, including their key attributes such as course name, code, description, category, duration, and cost. This table does not participate in any foreign key relationships, indicating that it functions independently in the data model, possibly acting as a reference for other unlisted entities. Each course entry is identified by a unique `course_id` and contains metadata about the course's creation and updates.

**Row Count:** 100

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| course_id | integer | NO | This column uniquely identifies each training course within the system. It uses sequential integers to assign a distinct identifier to each course record. |
| course_name | character varying | NO | This column contains descriptive phrases that likely represent titles or themes of various training courses. The exact purpose of each entry is unclear from the available data. |
| course_code | character varying | YES | This column appears to contain unique identifiers or codes for training courses, used to distinguish one course from another. Purpose unclear from available data. |
| description | text | YES | This column contains brief, fragmented textual descriptions associated with training courses, reflecting various concepts or themes potentially related to course content or objectives. Purpose unclear from available data. |
| category | character varying | YES | This column appears to categorize training courses with descriptive summaries or themes, although the exact purpose and structure of these descriptions are unclear based on the sample values. |
| duration_hours | numeric | YES | This column represents the duration of training courses measured in hours, suggesting variability in course lengths. Courses can have diverse durations ranging from under 100 hours to nearly 1,000 hours, reflecting different training intensities or comprehensive coverage. |
| is_mandatory | boolean | YES | Indicates whether a training course is required for participants, with true signifying mandatory courses. Most courses appear to be optional, as reflected by the predominance of false values. |
| provider | character varying | YES | Purpose unclear from available data. |
| cost | numeric | YES | This column represents the financial amount associated with training courses offered by the organization. The values indicate varying costs, suggesting that different courses or categories may have different pricing structures. |
| created_at | timestamp without time zone | YES | This column records the date and time when a training course entry was created in the system. The timestamp is typically set to the current date and time at the moment of entry creation, but it may be null. |
| updated_at | timestamp without time zone | YES | Indicates the most recent date and time when a record in the training courses table was updated. Purpose unclear from available data. |

## Primary Key

`course_id`

## Indexes

- `training_courses_course_code_key`: CREATE UNIQUE INDEX training_courses_course_code_key ON synthetic.training_courses USING btree (course_code)
- `training_courses_pkey`: CREATE UNIQUE INDEX training_courses_pkey ON synthetic.training_courses USING btree (course_id)

## Sample Data

| course_id | course_name | course_code | description | category | duration_hours | is_mandatory | provider | cost | created_at | updated_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Me off nature individual run summer month. Pare... | JTEVGICBBS | Car term truth toward. Camera recent drop fall ... | Explain main difference college. Writer send un... | 278.60 | true | Interview know call law truth respond try. Know... | 96692.22 | Sat Dec 13 2025 02:54:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:00 GMT-0600 (Central Stan... |
| 2 | Religious fire under item. Fish success produce... | SGOHWWSACU | Break let five box recent relate. Style tell ov... | No follow push in. Interesting end area magazin... | 279.12 | false | Really Mrs former article light. At player thir... | 67983.86 | Sat Dec 13 2025 02:54:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:00 GMT-0600 (Central Stan... |
| 3 | Follow time appear. Southern international line... | RCPRPEZCST | Personal wife statement tell until. Place make ... | That capital information suffer. Kitchen report... | 843.66 | false | Study prove assume stay may rock. Common and pa... | 93929.79 | Sat Dec 13 2025 02:54:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:00 GMT-0600 (Central Stan... |
| 4 | Study politics top course sense. Financial here... | PZRYSNVSGJ | Message decision design end. Military piece lit... | Nor probably top follow bit grow. City little f... | 115.34 | false | Over lot husband always upon doctor. Blue inter... | 17938.92 | Sat Dec 13 2025 02:54:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:00 GMT-0600 (Central Stan... |
| 5 | A challenge third feeling ball door data. Right... | GANMWZEPOI | Analysis few behavior himself conference. Expec... | Behind risk plan issue ever will ready. Try tou... | 962.53 | false | Mention rise front PM few husband. Wear either ... | 3921.89 | Sat Dec 13 2025 02:54:00 GMT-0600 (Central Stan... | Sat Dec 13 2025 02:54:00 GMT-0600 (Central Stan... |

*Generated at: 2025-12-14T23:41:11.173Z*