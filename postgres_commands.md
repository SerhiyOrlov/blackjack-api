### Show the list of all databse tabels 

SELECT tablename

FROM pg_tables

WHERE schemaname = 'public';  -- Replace 'public' with your schema name

### Show all values from a table

SELECT * FROM table_name