import duckdb

con = duckdb.connect()
df = con.execute("DESCRIBE SELECT * FROM 'dpwh_projects_raw.parquet'")
print(df.fetchdf())