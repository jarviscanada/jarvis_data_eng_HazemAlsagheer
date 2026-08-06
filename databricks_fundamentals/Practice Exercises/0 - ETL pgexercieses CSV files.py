# Databricks notebook source
# MAGIC %md
# MAGIC # Learning Objectives
# MAGIC
# MAGIC In this notebook, you will 
# MAGIC - learn the concept of ETL
# MAGIC - write ETL jobs for CSV files from `pgexercises` https://pgexercises.com/gettingstarted.html

# COMMAND ----------

# MAGIC %md
# MAGIC # What's ETL or ELT?
# MAGIC
# MAGIC ETL stands for Extract, Transform, Load. In the context of Spark, ETL refers to the process of extracting data from various sources, transforming it into a desired format or structure, and loading it into a target system, such as a data warehouse or a data lake.
# MAGIC
# MAGIC Here's a breakdown of each step in the ETL process:
# MAGIC
# MAGIC ## Extract
# MAGIC This step involves extracting data from multiple sources, such as databases, files (CSV, JSON, Parquet), APIs, or streaming data sources. Spark provides connectors and APIs to read data from a wide range of sources, allowing you to extract data in parallel and efficiently handle large datasets.
# MAGIC
# MAGIC ## Transform
# MAGIC In the transform step, the extracted data is processed and transformed according to specific business logic or requirements. This may involve cleaning the data, applying calculations or aggregations, performing data enrichment, filtering, joining datasets, or any other data manipulation operations. Spark provides a powerful set of transformation functions and SQL capabilities to perform these operations efficiently in a distributed and scalable manner.
# MAGIC
# MAGIC ## Load
# MAGIC Once the data has been transformed, it is loaded into a target system, such as a data warehouse, a data lake, or another storage system. Spark allows you to write the transformed data to various output formats and storage systems, including databases, distributed file systems (like Hadoop Distributed File System or Amazon S3), or columnar formats like Delta Lake or Apache Parquet. The data can be partitioned, sorted, or structured to optimize querying and analysis.
# MAGIC
# MAGIC Spark's distributed computing capabilities, scalability, and rich ecosystem of libraries make it a popular choice for ETL workflows. It can handle large-scale data processing, perform complex transformations, and efficiently load data into different target systems.
# MAGIC
# MAGIC By leveraging Spark for ETL, organizations can extract data from diverse sources, apply transformations to ensure data quality and consistency, and load the transformed data into a central repository for further analysis, reporting, or machine learning tasks.

# COMMAND ----------

# MAGIC %md
# MAGIC # Enable DBFS UI
# MAGIC
# MAGIC - Setting -> Admin Console -> search for dbfs
# MAGIC
# MAGIC <img src="https://raw.githubusercontent.com/jarviscanada/jarvis_data_eng_demo/feature/data/spark/notebook/spark_fundamentals/img/entable_dbfs.jpg" width="700">
# MAGIC
# MAGIC - Refresh the page and view DBFS files from UI
# MAGIC
# MAGIC <img src="https://raw.githubusercontent.com/jarviscanada/jarvis_data_eng_demo/feature/data/spark/notebook/spark_fundamentals/img/dbfs%20ui.png" width="700">

# COMMAND ----------

# MAGIC %md
# MAGIC ## Import `pgexercises` CSV files
# MAGIC
# MAGIC - The pgexercises CSV data files can be found [here](https://github.com/jarviscanada/jarvis_data_eng_demo/tree/feature/data/spark/data/pgexercises).
# MAGIC - The pgexercises schema can be found [here](https://pgexercises.com/gettingstarted.html) (for reference purposes).
# MAGIC - Upload the `bookings.csv`, `facilities.csv`, and `members.csv` files using Databricks UI (see screenshot)
# MAGIC - You can view the imported files from the DBFS UI.
# MAGIC
# MAGIC ![Upload Files](https://raw.githubusercontent.com/jarviscanada/jarvis_data_eng_demo/feature/data/spark/notebook/spark_fundamentals/img/upload%20file.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Interview Questions
# MAGIC
# MAGIC While completing the rest of the practice, try to answer the following questions:
# MAGIC
# MAGIC ## Concepts
# MAGIC - What is ETL? (Hint: Explain each step)    
# MAGIC     ETL stands for Extract, Transform, and Load, a process used to move data from source systems into a centralized data repository for analysis. During the Extract phase, data is collected from one or more sources such as databases, files, APIs, or cloud storage. In the Transform phase, the extracted data is cleaned, validated, standardized, and reshaped to meet business requirements, such as removing duplicates, correcting data types, joining datasets, or creating new calculated fields. Finally, during the Load phase, the transformed data is written into a destination system such as a data warehouse, data lake, or Delta table where it becomes available for reporting and analytics.    
# MAGIC
# MAGIC ## Databricks
# MAGIC - What is Databricks?
# MAGIC     Databricks is a cloud-based data analytics platform built on Apache Spark that provides a unified environment for data engineering, data science, machine learning, and business analytics. It implements the Lakehouse architecture, combining the flexibility and low-cost storage of a data lake with the reliability, governance, and performance of a data warehouse. Databricks supports multiple programming languages, collaborative notebooks, automated workflows, and scalable distributed computing, making it suitable for processing both structured and unstructured data.    
# MAGIC - What is a Notebook?
# MAGIC     A notebook is a web-based interactive document that combines executable code, visualizations, and documentation in a single environment. In Databricks, notebooks support multiple programming languages—including Python, SQL, Scala, and R—within the same notebook by using language magic commands such as %python and %sql. This allows users to develop, analyze, visualize, and document data pipelines collaboratively in one place.    
# MAGIC - What is DBFS?
# MAGIC     DBFS (Databricks File System) is an abstraction layer that provides a unified file system interface for accessing data stored in distributed cloud storage. Rather than storing data itself, DBFS exposes cloud storage such as Azure Data Lake Storage, Amazon S3, or Google Cloud Storage through familiar file paths that Spark and Databricks workloads can read from and write to. This allows users to interact with distributed storage as though it were a local file system while Databricks manages the underlying storage access.     
# MAGIC - What is a cluster? 
# MAGIC     A cluster is the compute engine used by Databricks to execute Spark applications. It consists of a single driver node, which coordinates the execution of the application, creates execution plans, schedules tasks, and manages Spark jobs, and one or more worker nodes that run executor processes responsible for performing the distributed computations. Databricks automatically provisions and manages these resources, allowing Spark to process large datasets efficiently across multiple machines.    
# MAGIC - Is Databricks a data lake or a data warehouse?
# MAGIC     Databricks is neither purely a data lake nor purely a data warehouse. Instead, it implements a Lakehouse architecture, which combines the scalability and flexibility of a data lake with the reliability, governance, ACID transactions, and performance optimizations traditionally associated with data warehouses. This enables organizations to store raw and structured data in one platform while supporting both large-scale data engineering and high-performance analytics.
# MAGIC ## Managed Table
# MAGIC - What is a managed table in Databricks?
# MAGIC     A managed table is a table whose metadata and underlying data files are both managed by Databricks through the Unity Catalog or Hive Metastore. When data is written using saveAsTable(), Databricks stores the data in its managed storage location and automatically maintains the table's metadata. If the managed table is dropped, Databricks deletes both the table metadata and the underlying data files.
# MAGIC - Can you explain how to create a managed table in Databricks?
# MAGIC     A managed table can be created by writing a DataFrame using the saveAsTable() method without specifying an external storage path. For example, df.write.mode("overwrite").saveAsTable("catalog.schema.sales") stores the DataFrame as a managed table within Unity Catalog. Databricks automatically determines where the data is physically stored and registers the table metadata so it can be queried using SQL or Spark.
# MAGIC - Can you compare a managed table with an RDBMS table? (Hint: Schema on read vs schema on write)
# MAGIC     Traditional relational database tables typically follow a schema-on-write approach, meaning data must conform to a predefined schema before it can be inserted. This provides strong consistency and validation during ingestion. In contrast, data lakes commonly follow schema-on-read, where raw data can be stored without enforcing a schema, and the structure is interpreted when the data is queried. Managed tables in Databricks—particularly Delta tables—behave much more like relational database tables because they enforce a schema when data is written while also providing ACID transactions, making them effectively schema-on-write despite residing within a Lakehouse architecture.
# MAGIC - What is the Hive metastore and how does it relate to managed tables in Databricks?
# MAGIC     The Hive Metastore is a centralized metadata repository that stores information about tables, such as their schemas, locations, partitions, and properties, rather than the data itself. Before Unity Catalog became the standard, Databricks used the Hive Metastore to organize and manage tables. When a managed table is created, the metastore records its metadata so Spark can locate and query it efficiently. Today, Unity Catalog largely replaces the Hive Metastore by providing centralized governance, security, and metadata management across multiple workspaces.
# MAGIC - How does a managed table differ from an unmanaged (external) table in Databricks? (Hint: Consider what happens to the data when the table is deleted)
# MAGIC     A managed table stores both its metadata and its data under Databricks' management. As a result, deleting the table also deletes the underlying data files. An external table, on the other hand, stores only its metadata in the catalog while the actual data remains in an external storage location specified by the user. Dropping an external table removes only the metadata, leaving the underlying data untouched.     
# MAGIC - How can you define a schema for a managed table?
# MAGIC     Rather than relying on schema inference, a schema can be explicitly defined using Spark's StructType and StructField classes before reading the data into a DataFrame. Spark then validates the incoming data against this schema, improving performance and ensuring consistent data types. Once the DataFrame has the desired schema, it can be written to a managed table using saveAsTable(), and the table will inherit that schema.    
# MAGIC
# MAGIC     schema= StructType([
# MAGIC         StructField('Col', DataType, Nullable?)
# MAGIC     ])
# MAGIC     df=spark.read.format('csv').schema(schema).load('filepath')
# MAGIC
# MAGIC ## Spark
# MAGIC `df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(file_location)`
# MAGIC - What does the option("inferSchema", "true") do? 
# MAGIC     The inferSchema option instructs Spark to examine the input data and automatically determine the appropriate data type for each column instead of treating every column as a string. This requires Spark to scan the dataset before loading it, introducing additional overhead. For production workloads, explicitly defining the schema is generally preferred because it improves performance, ensures consistency, and avoids incorrect type inference.
# MAGIC - What does the option("header", "true") do?
# MAGIC     The header option tells Spark to interpret the first row of a file as the column names rather than as a row of data. This allows the resulting DataFrame to use meaningful column names instead of automatically generated names such as _c0, _c1, and _c2.      
# MAGIC - How can you write data to a managed table?
# MAGIC     A DataFrame can be written to a managed table using the saveAsTable() method. If the table is a Delta table, Spark writes the data in Delta format while registering it in Unity Catalog or the Hive Metastore. Different write modes such as append, overwrite, ignore, or errorIfExists can be used depending on whether the existing table should be updated or replaced.     
# MAGIC - How can you read data from a managed table into a DataFrame?
# MAGIC     A managed table can be loaded directly into a Spark DataFrame using spark.table("catalog.schema.tableName") or by executing a SQL query such as spark.sql("SELECT * FROM catalog.schema.tableName"). Once loaded, the DataFrame can be transformed, analyzed, or written to another destination using Spark's DataFrame APIs.   

# COMMAND ----------

# MAGIC %md
# MAGIC # ETL `bookings.csv` file
# MAGIC
# MAGIC - **Extract**: Load data from CSV file into a DF
# MAGIC - **Transformation**: no transformation needed as we want to load data as it
# MAGIC - **Load**: Save the DF into a managed table (or Hive table); 
# MAGIC
# MAGIC # Managed Table
# MAGIC This is an important interview topic. Some people may refer to managed tables as Hive tables.
# MAGIC
# MAGIC https://docs.databricks.com/data-governance/unity-catalog/create-tables.html

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, TimestampType

file_location = "/Volumes/databricks_fundamentals/default/filestore/bookings.csv"

# What does `option("header", "true")` and `option("inferSchema", "true")` do?
df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(file_location)

# Why the df schema doesn't match the DDL data type? https://pgexercises.com/gettingstarted.html (hint: `option("inferSchema", "true")`)
df.printSchema()

# Here is the solution to define schema manually
# Define schema for the bookings table
schema = StructType([
    StructField("bookid", IntegerType(), False),
    StructField("facid", IntegerType(), False),
    StructField("memid", IntegerType(), False),
    StructField("starttime", TimestampType(), False),
    StructField("slots", IntegerType(), False)
])

# Read data from CSV file into DataFrame with predefined schema
df = spark.read.format("csv").option("header", "true").schema(schema).load(file_location)

# No 

# Drop the table if it already exists
spark.sql("DROP TABLE IF EXISTS databricks_fundamentals.default.bookings")

# Write data from DataFrame into managed table
df.write.saveAsTable("databricks_fundamentals.default.bookings")


# COMMAND ----------

# MAGIC %md
# MAGIC # Complete ETL Jobs
# MAGIC
# MAGIC - Complete ETL for `facilities.csv` and `members.csv`
# MAGIC - Tips
# MAGIC   - The Databricks community version will terminate the cluster after a few hours of inactivity. As a result, all managed tables will be deleted. You will need to rerun this notebook to perform the ETL on all files for the other exercises.
# MAGIC   - DBFS data will not be deleted when a custer become inactive/deleted

# COMMAND ----------

# Write a ETL job for `facilities.csv`
from pyspark.sql.types import StringType,DecimalType

file_location='/Volumes/databricks_fundamentals/default/filestore/facilities.csv'
schema=StructType([
    StructField('facid',IntegerType(),False),
    StructField('name',StringType(),False),
    StructField('membercost',DecimalType(), False),
    StructField('guestcost',DecimalType(), False),
    StructField('initialoutlay',DecimalType(), False),
    StructField('monthlymaintenance',DecimalType(),False)
])

df=spark.read.format('csv').option('header','true').schema(schema).load(file_location)

spark.sql('DROP TABLE IF EXISTS databricks_fundamentals.default.facilities')
df.write.saveAsTable('databricks_fundamentals.default.facilities')


# COMMAND ----------

# Write a ETL job Complete ETL for `members.csv`
from pyspark.sql.types import BooleanType, DateType
file_location='/Volumes/databricks_fundamentals/default/filestore/members.csv'
schema=StructType([
    StructField('memid',IntegerType(),False),
    StructField('surname',StringType(),False),
    StructField('firstname',StringType(),False),
    StructField('address', StringType(),False),
    StructField('zipcode', IntegerType(),False),
    StructField('telephone', StringType(),False),
    StructField('recommendedby', IntegerType(),False),
    StructField('joindate', TimestampType(), False)
])

df=spark.read.format('csv').option('header','true').schema(schema).load(file_location)

spark.sql('DROP TABLE IF EXISTS databricks_fundamentals.default.members')
df.write.saveAsTable('databricks_fundamentals.default.members')

# COMMAND ----------

# MAGIC %md
# MAGIC # Save your work to Git
# MAGIC
# MAGIC - Export the notebook to IPYTHON format, `notebook top menu bar -> File -> Export -> iphython`
# MAGIC - Upload to your Git repository, `your_repo/spark/notebooks/`
# MAGIC - Github can render ipython notebook https://github.com/josephcslater/JupyterExamples/blob/master/Calc_Review.ipynb