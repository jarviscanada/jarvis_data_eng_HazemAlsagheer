# Databricks notebook source
# MAGIC %md
# MAGIC # Learning Objectives
# MAGIC
# MAGIC In this notebook, you will craft sophisticated ETL jobs that interface with a variety of common data sources, such as 
# MAGIC - REST APIs (HTTP endpoints)
# MAGIC - RDBMS
# MAGIC - Hive tables (managed tables)
# MAGIC - Various file formats (csv, json, parquet, etc.)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC # Interview Questions
# MAGIC
# MAGIC As you progress through the practice, attempt to answer the following questions:
# MAGIC
# MAGIC ## Columnar File
# MAGIC - **What is a columnar file format and what advantages does it offer?**       
# MAGIC     A columnar file format stores data by columns rather than by rows, meaning all values from the same column are stored together on disk. This organization is ideal for analytical workloads because Spark often only needs a subset of the columns in a dataset. Instead of scanning the entire file, Spark reads only the required columns, reducing disk I/O and improving query performance. Columnar formats also compress data more efficiently since values within a column are typically similar in type and distribution. A common example of a columnar file format used with Spark is Parquet.
# MAGIC          
# MAGIC - **Why is Parquet frequently used with Spark and how does it function?**     
# MAGIC     Parquet is frequently used with Spark because it is a distributed, columnar storage format optimized for large-scale analytics. It stores data in row groups, with each column stored separately within those groups, along with metadata and statistics such as minimum and maximum values. Spark uses this metadata to perform optimizations like column pruning and predicate pushdown, allowing it to skip unnecessary columns and data blocks during queries. Combined with its efficient compression, Parquet significantly reduces storage requirements and speeds up analytical workloads, making it one of the default file formats for Spark-based data processing.
# MAGIC          
# MAGIC - **How do you read/write data from/to a Parquet file using a DataFrame?**      
# MAGIC     Parquet files can be read into a Spark DataFrame using spark.read.parquet(path) or spark.read.format("parquet").load(path). Once the data has been processed, it can be written back using df.write.parquet(path) or df.write.format("parquet").save(path), optionally specifying a write mode such as overwrite or append. Since Parquet preserves the schema and data types, it integrates seamlessly with Spark DataFrames     
# MAGIC                 
# MAGIC ## Partitions
# MAGIC - **How do you save data to a file system by partitions? (Hint: Provide the code)**      
# MAGIC     Spark allows data to be physically partitioned when writing files by using the partitionBy() method. For example, df.write.partitionBy("country").parquet("/data/sales") stores the data in separate folders for each country. Instead of one large dataset, Spark creates a directory structure where each partition contains only the records for a specific partition value, making the data more efficient to query.
# MAGIC          
# MAGIC - **How and why can partitions reduce query execution time? (Hint: Give an example)**    
# MAGIC     Partitioning reduces query execution time through partition pruning. When a dataset is partitioned on a column that is commonly used for filtering, Spark can skip entire partitions that are not relevant to the query. For example, if sales data is partitioned by country and a query requests only Canadian sales, Spark reads only the country=Canada partition instead of scanning data for every country. This significantly reduces disk I/O, network traffic, and the amount of data Spark needs to process. However, partitioning should be done on columns with relatively low cardinality, such as dates or countries, because partitioning on highly unique columns can create too many small files and hurt performance.
# MAGIC          
# MAGIC               
# MAGIC ## JDBC and RDBMS
# MAGIC - **How do you load data from an RDBMS into Spark? (Hint: Discuss the steps and JDBC)**     
# MAGIC     Spark loads data from relational databases using JDBC (Java Database Connectivity). A JDBC connection requires the database URL, the table name or SQL query to read, user credentials, and the appropriate JDBC driver. Spark then establishes a connection to the database, retrieves the requested data, and loads it into a DataFrame for distributed processing. For large tables, Spark can also read the data in parallel by partitioning the JDBC read across multiple connections, improving performance when importing large datasets. 
# MAGIC       
# MAGIC            
# MAGIC ## REST API and HTTP Requests
# MAGIC - **How can Spark be used to fetch data from a REST API? (Hint: Discuss making API requests)**     
# MAGIC     Spark does not directly connect to REST APIs like it does with JDBC databases. Instead, an HTTP client such as Python's requests library is typically used to send HTTP requests and retrieve the API's JSON response. The returned JSON is then converted into a Python data structure, such as a list of dictionaries, and loaded into a Spark DataFrame using spark.createDataFrame(). Once the data is in a DataFrame, Spark can perform distributed transformations and analysis. For large APIs, it is common to first save the API responses to cloud storage or a data lake and then have Spark read the JSON files in parallel for better scalability.

# COMMAND ----------

from pyspark.sql import SparkSession
spark=SparkSession.builder.appName('Notebook3').getOrCreate()

# COMMAND ----------

# MAGIC %md
# MAGIC ## ETL Job One: Parquet file
# MAGIC ### Extract
# MAGIC Extract data from the managed tables (e.g. `bookings_csv`, `members_csv`, and `facilities_csv`)
# MAGIC
# MAGIC ### Transform
# MAGIC Data transformation requirements https://pgexercises.com/questions/aggregates/fachoursbymonth.html
# MAGIC
# MAGIC ### Load
# MAGIC Load data into a parquet file
# MAGIC
# MAGIC ### What is Parquet? 
# MAGIC
# MAGIC Columnar files are an important technique for optimizing Spark queries. Additionally, they are often tested in interviews.
# MAGIC - https://www.youtube.com/watch?v=KLFadWdomyI
# MAGIC - https://www.databricks.com/glossary/what-is-parquet

# COMMAND ----------

# Write your solution here
df=spark.table('databricks_fundamentals.default.bookings')
transformed_df=df.filter("starttime>='2012-09-01' and starttime<'2012-10-01'").groupBy('facid').sum('slots').withColumnRenamed("sum(slots)","Total Slots").orderBy(asc('sum(slots)'))
transformed_df.write.parquet("/Volumes/databricks_fundamentals/default/filestore/transformedData.parquet")

# COMMAND ----------

# MAGIC %md
# MAGIC ## ETL Job Two: Partitions
# MAGIC
# MAGIC ### Extract
# MAGIC Extract data from the managed tables (e.g. `bookings_csv`, `members_csv`, and `facilities_csv`)
# MAGIC
# MAGIC ### Transform
# MAGIC Transform the data https://pgexercises.com/questions/joins/threejoin.html
# MAGIC
# MAGIC ### Load
# MAGIC Partition the result data by facility column and then save to `threejoin_delta` managed table. Additionally, they are often tested in interviews.
# MAGIC
# MAGIC hint: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameWriter.partitionBy.html
# MAGIC
# MAGIC What are paritions? 
# MAGIC
# MAGIC Partitions are an important technique to optimize Spark queries
# MAGIC - https://www.youtube.com/watch?v=hvF7tY2-L3U&t=268s

# COMMAND ----------

# MAGIC %md
# MAGIC ### Table Setup

# COMMAND ----------

# Write your solution here
bookings=spark.table('databricks_fundamentals.default.bookings')
facilities=spark.table('databricks_fundamentals.default.facilities')
members=spark.table('databricks_fundamentals.default.members')


# COMMAND ----------

# MAGIC %md
# MAGIC ### Implementation

# COMMAND ----------

from pyspark.sql.functions import rlike, concat_ws, col

df=members.withColumn('member', concat_ws(' ', col('members.firstname'), col('members.surname'))).join(bookings,on='memid',how='inner').join(facilities, on='facid', how='inner').filter(col('facilities.name').ilike('tennis court%')).select(col('member'),col('facilities.name').alias("facility")).dropDuplicates().orderBy('member')
df.write.partitionBy('facility').saveAsTable('databricks_fundamentals.default.threejoin_delta')

# COMMAND ----------

# MAGIC %md
# MAGIC ## ETL Job Three: HTTP Requests
# MAGIC
# MAGIC ### Extract
# MAGIC Extract daily stock price data price from the following companies, Google, Apple, Microsoft, and Tesla. 
# MAGIC
# MAGIC Data Source
# MAGIC - API: https://rapidapi.com/alphavantage/api/alpha-vantage
# MAGIC - Endpoint: GET `TIME_SERIES_DAILY`
# MAGIC
# MAGIC Sample HTTP request
# MAGIC
# MAGIC ```
# MAGIC curl --request GET \
# MAGIC 	--url 'https://alpha-vantage.p.rapidapi.com/query?function=TIME_SERIES_DAILY&symbol=TSLA&outputsize=compact&datatype=json' \
# MAGIC 	--header 'X-RapidAPI-Host: alpha-vantage.p.rapidapi.com' \
# MAGIC 	--header 'X-RapidAPI-Key: [YOUR_KEY]'
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC Sample Python HTTP request
# MAGIC
# MAGIC ```
# MAGIC import requests
# MAGIC
# MAGIC url = "https://alpha-vantage.p.rapidapi.com/query"
# MAGIC
# MAGIC querystring = {
# MAGIC     "function":"TIME_SERIES_DAILY",
# MAGIC     "symbol":"IBM",
# MAGIC     "datatype":"json",
# MAGIC     "outputsize":"compact"
# MAGIC }
# MAGIC
# MAGIC headers = {
# MAGIC     "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com",
# MAGIC     "X-RapidAPI-Key": "[YOUR_KEY]"
# MAGIC }
# MAGIC
# MAGIC response = requests.get(url, headers=headers, params=querystring)
# MAGIC
# MAGIC data = response.json()
# MAGIC
# MAGIC # Now 'data' contains the daily time series data for "IBM"
# MAGIC ```
# MAGIC
# MAGIC ### Transform
# MAGIC Find **weekly** max closing price for each company.
# MAGIC
# MAGIC hints: 
# MAGIC   - Use a `for-loop` to get stock data for each company
# MAGIC   - Use the spark `union` operation to concat all data into one DF
# MAGIC   - create a new `week` column from the data column
# MAGIC   - use `group by` to calcualte max closing price
# MAGIC
# MAGIC ### Load
# MAGIC - Partition `DF` by company
# MAGIC - Load the DF in to a managed table called, `max_closing_price_weekly`

# COMMAND ----------

import requests

url = "https://alpha-vantage.p.rapidapi.com/query"

companies=['GOOGL','MSFT','APPL','TSLA']
records=[]
for company in companies:
    querystring = {
        "function":"TIME_SERIES_DAILY",
        "symbol":company,
        "datatype":"json",
        "outputsize":"compact"
    }

    headers = {
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com",
        "X-RapidAPI-Key": "71c41207famsh019cff6b17dc635p1a04a0jsn300173d7c58c"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)

        data = response.json()
    
        for date, values in data['Time Series (Daily)'].items():
            record=[company]
            record.append(date)
            record.append(float(values['1. open']))
            record.append(float(values['2. high']))
            record.append(float(values['3. low']))
            record.append(float(values['4. close']))
            record.append(float(values['5. volume']))
            records.append(record)
    except Exception as err:
        print(err)




# COMMAND ----------

from pyspark.sql.functions import col, weekofyear, max
df=spark.createDataFrame(records,schema=['symbol','date','open','high','low','close','volume']).withColumn('Week',weekofyear(col('date'))).groupBy('week').agg(max('close').alias('Maximum Close Price')).show()






# COMMAND ----------

# MAGIC %md
# MAGIC ## ETL Job Four: RDBMS
# MAGIC
# MAGIC
# MAGIC ### Extract
# MAGIC Extract RNA data from a public PostgreSQL database.
# MAGIC
# MAGIC - https://rnacentral.org/help/public-database
# MAGIC - Extract 100 RNA records from the `rna` table (hint: use `limit` in your sql)
# MAGIC - hint: use `spark.read.jdbc` https://docs.databricks.com/external-data/jdbc.html
# MAGIC
# MAGIC ### Transform
# MAGIC We want to load the data as it so there is no transformation required.
# MAGIC
# MAGIC
# MAGIC ### Load
# MAGIC Load the DF in to a managed table called, `rna_100_records`

# COMMAND ----------

# Write your solution here
rna_table = (spark.read
  .format("jdbc")
  .option("url", "jdbc:postgresql://hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs")
  .option("dbtable", "rna")
  .option("user", "reader")
  .option("password", "NWDMCE5xdipIjRrp").option('driver','org.postgresql.Driver')
  .load()
)


# COMMAND ----------

rna_table.limit(100).write.saveAsTable('databricks_fundamentals.default.rna_100_records')

# COMMAND ----------

