### Show the list of all databse tabels 

SELECT tablename

FROM pg_tables

WHERE schemaname = 'public';  -- Replace 'public' with your schema name

### Show the all values from a table

SELECT * FROM table_name

### Delete the value from a table

DELETE FROM table_name WHERE column_name = value;
