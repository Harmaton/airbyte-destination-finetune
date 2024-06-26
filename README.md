# Project Overview

This project involves migrating data from a MySQL database to a PostgreSQL database. During the migration process, additional columns were added to the schema by Airbyte. These columns are `_airbyte_raw_id`, `_airbyte_extracted_at`, and `_airbyte_meta`.

## Problem Description

After transferring data from MySQL to PostgreSQL, the schema in the PostgreSQL database included additional columns introduced by Airbyte. Specifically, the following columns were added to each table:

- `_airbyte_raw_id`: A unique identifier for the row in the context of the Airbyte sync.
- `_airbyte_extracted_at`: A timestamp indicating when the data was extracted by Airbyte.
- `_airbyte_meta`: A JSONB column containing metadata about the row.

These additional columns were affecting the original frontend logic of the application. The frontend was not designed to handle these extra columns, leading to unexpected behavior and potential bugs.

## Solution

To resolve this issue, I created a Python script that connects to the PostgreSQL database and removes the `_airbyte_raw_id`, `_airbyte_extracted_at`, and `_airbyte_meta` columns from all tables. This ensures that the database schema matches the original schema from the MySQL database, allowing the frontend to function correctly.

## Recommendation

If you need to retain the original columns as in your source database while using Airbyte, it is recommended to remove these additional columns after the migration process. This will help maintain the integrity of your frontend logic and ensure that your application functions as expected.
