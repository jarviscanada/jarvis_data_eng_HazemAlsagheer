# Databricks notebook source
# MAGIC %md
# MAGIC # Learning Objectives
# MAGIC In this notebook, you will learn Spark Dataframe APIs.
# MAGIC
# MAGIC # Question List
# MAGIC
# MAGIC Solve the following questions using Spark Dataframe APIs
# MAGIC
# MAGIC ### Join
# MAGIC
# MAGIC 1. easy - https://pgexercises.com/questions/joins/simplejoin.html done
# MAGIC 2. easy - https://pgexercises.com/questions/joins/simplejoin2.html done
# MAGIC 3. easy - https://pgexercises.com/questions/joins/self2.html done
# MAGIC 4. medium - https://pgexercises.com/questions/joins/threejoin.html (three join) done
# MAGIC 5. medium - https://pgexercises.com/questions/joins/sub.html (subquery and join) done
# MAGIC
# MAGIC ### Aggregation
# MAGIC
# MAGIC 1. easy - https://pgexercises.com/questions/aggregates/count3.html Group by order by  done
# MAGIC 2. easy - https://pgexercises.com/questions/aggregates/fachours.html group by order by  done
# MAGIC 3. easy - https://pgexercises.com/questions/aggregates/fachoursbymonth.html group by with condition  done
# MAGIC 4. easy - https://pgexercises.com/questions/aggregates/fachoursbymonth2.html group by multi col done
# MAGIC 5. easy - https://pgexercises.com/questions/aggregates/members1.html count distinct  done
# MAGIC 6. med - https://pgexercises.com/questions/aggregates/nbooking.html group by multiple cols, join  done
# MAGIC
# MAGIC ### String & Date
# MAGIC
# MAGIC 1. easy - https://pgexercises.com/questions/string/concat.html format string done
# MAGIC 2. easy - https://pgexercises.com/questions/string/case.html WHERE + string function done
# MAGIC 3. easy - https://pgexercises.com/questions/string/reg.html WHERE + string function done
# MAGIC 4. easy - https://pgexercises.com/questions/string/substr.html group by, substr done
# MAGIC 5. easy - https://pgexercises.com/questions/date/series.html generate ts done
# MAGIC 6. easy - https://pgexercises.com/questions/date/bookingspermonth.html extract month from ts done

# COMMAND ----------

# MAGIC %md
# MAGIC ## Spark Session

# COMMAND ----------

# Write you solution here
# hint: you might need to re-run `0 - ETL pgexercises CSV files` notebook to init tables

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, rlike,count
spark=SparkSession.builder.appName('Notebook 2').getOrCreate()


# COMMAND ----------

# MAGIC %md
# MAGIC ## Table Setup

# COMMAND ----------

bookings=spark.table('databricks_fundamentals.default.bookings')
members=spark.table('databricks_fundamentals.default.members')
facilities=spark.table('databricks_fundamentals.default.facilities')

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question
# MAGIC
# MAGIC How can you produce a list of the start times for bookings by members named 'David Farrell'?
# MAGIC
# MAGIC https://pgexercises.com/questions/joins/simplejoin.html

# COMMAND ----------

df=bookings.join(members,on="memid",how="inner").filter((col("firstname")=='David') & (col("surname")=='Farrell')).select('starttime').show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question
# MAGIC How can you produce a list of the start times for bookings for tennis courts, for the date '2012-09-21'? Return a list of start time and facility name pairings, ordered by the time.   
# MAGIC https://pgexercises.com/questions/joins/simplejoin2.html

# COMMAND ----------

df=bookings.join(facilities, on='facid', how='inner').filter((col("starttime")>"2012-09-21") &(col('starttime')<'2012-09-22') & (col('facilities.name').rlike('Tennis Court*'))).sort(col("starttime")).withColumnRenamed('starttime', 'start').select(col('start'), col('facilities.name')).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question
# MAGIC How can you output a list of all members, including the individual who recommended them (if any)? Ensure that results are ordered by (surname, firstname).    
# MAGIC https://pgexercises.com/questions/joins/self2.html

# COMMAND ----------

r=members.alias('r')
df=members.alias('m').join(r, col('m.recommendedby')==col('r.memid'),how='left').select(
    col('m.firstname').alias('memfname'),
    col('m.surname').alias('memsname'),
    col('r.firstname').alias('recfname'),
    col('r.surname').alias('recsname')
).orderBy('memsname','memfname').show()


# COMMAND ----------

# MAGIC %md
# MAGIC ### Question
# MAGIC How can you produce a list of all members who have used a tennis court? Include in your output the name of the court, and the name of the member formatted as a single column. Ensure no duplicate data, and order by the member name followed by the facility name.    
# MAGIC https://pgexercises.com/questions/joins/threejoin.html

# COMMAND ----------

from pyspark.sql.functions import concat_ws
df=members.alias('m').join(bookings, on='memid', how='inner').join(facilities, on='facid', how='inner').filter(col('facilities.name').rlike('Tennis Court*')).withColumn('member', concat_ws(" ",col('m.firstname'), col('m.surname'))).select(col('member'), col('facilities.name').alias('facility')).dropDuplicates().orderBy('member').show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question
# MAGIC How can you output a list of all members, including the individual who recommended them (if any), without using any joins? Ensure that there are no duplicates in the list, and that each firstname + surname pairing is formatted as a column and ordered.    
# MAGIC
# MAGIC https://pgexercises.com/questions/joins/sub.html

# COMMAND ----------

r=members.alias('r').withColumn('recommender', concat_ws(" ",members.firstname,members.surname))
df=members.withColumn('member', concat_ws(" ", members.firstname, members.surname)).join(r,col('members.recommendedby')==col('r.memid'), how='left').select('member', 'recommender').orderBy('member').show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question
# MAGIC Produce a count of the number of recommendations each member has made. Order by member ID.   
# MAGIC https://pgexercises.com/questions/aggregates/count3.html

# COMMAND ----------

df=members.groupBy('recommendedby').agg(count('memid').alias('count')).orderBy('recommendedby').filter(col('recommendedby').isNotNull()).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question
# MAGIC Produce a list of the total number of slots booked per facility. For now, just produce an output table consisting of facility id and slots, sorted by facility id.    
# MAGIC
# MAGIC https://pgexercises.com/questions/aggregates/fachours.html

# COMMAND ----------

from pyspark.sql.functions import sum
df=bookings.groupby('facid').agg(sum("slots").alias('Total Slots')).sort('facid').show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question
# MAGIC Produce a list of the total number of slots booked per facility in the month of September 2012. Produce an output table consisting of facility id and slots, sorted by the number of slots.   
# MAGIC https://pgexercises.com/questions/aggregates/fachoursbymonth.html

# COMMAND ----------

df= bookings.filter((col('starttime')>='2012-09-01') & (col('starttime')<'2012-10-01')).groupBy('facid').agg(sum('slots').alias('Total Slots')).orderBy('Total Slots').show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question
# MAGIC Produce a list of the total number of slots booked per facility per month in the year of 2012. Produce an output table consisting of facility id and slots, sorted by the id and month.   
# MAGIC
# MAGIC https://pgexercises.com/questions/aggregates/fachoursbymonth2.html 

# COMMAND ----------

from pyspark.sql.functions import month
df=bookings.withColumn('month', month(col('starttime'))).filter((col('starttime')>='2012-01-01')&(col('starttime')<'2013-01-01')).groupBy('facid','month').agg(sum('slots').alias('Total Slots')).sort('facid','month').show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question
# MAGIC Find the total number of members (including guests) who have made at least one booking.  
# MAGIC https://pgexercises.com/questions/aggregates/members1.html

# COMMAND ----------

df=bookings.select(col('memid')).dropDuplicates().agg(count('memid').alias('count')).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question
# MAGIC Produce a list of each member name, id, and their first booking after September 1st 2012. Order by member ID.    
# MAGIC https://pgexercises.com/questions/aggregates/nbooking.html 

# COMMAND ----------

from pyspark.sql.window import Window
from pyspark.sql.functions import row_number
w=Window.partitionBy('bookings.memid').orderBy('bookings.starttime')
df=bookings.filter(col('starttime')>'2012-09-01').join(members,on='memid',how='inner').withColumn('rn', row_number().over(w)).filter(col('rn')==1).select('surname','firstname','memid', 'starttime').orderBy('memid').show()

# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question
# MAGIC Output the names of all members, formatted as 'Surname, Firstname'
# MAGIC https://pgexercises.com/questions/string/concat.html

# COMMAND ----------

df=members.withColumn('name', concat_ws(', ','surname','firstname')).select('name').show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question
# MAGIC Perform a case-insensitive search to find all facilities whose name begins with 'tennis'. Retrieve all columns.    
# MAGIC https://pgexercises.com/questions/string/case.html

# COMMAND ----------

from pyspark.sql.functions import ilike
df=facilities.filter(col('name').ilike('tennis%')).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question 
# MAGIC You've noticed that the club's member table has telephone numbers with very inconsistent formatting. You'd like to find all the telephone numbers that contain parentheses, returning the member ID and telephone number sorted by member ID.   
# MAGIC https://pgexercises.com/questions/string/reg.html

# COMMAND ----------

df=members.filter(col('telephone').rlike('^\(\d{3}\)')).select('memid','telephone').show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question
# MAGIC You'd like to produce a count of how many members you have whose surname starts with each letter of the alphabet. Sort by the letter, and don't worry about printing out a letter if the count is 0.   
# MAGIC https://pgexercises.com/questions/string/substr.html

# COMMAND ----------

from pyspark.sql.functions import substring
df= members.withColumn('Letter', substring('surname',0,1)).groupBy('Letter').agg(count('Letter').alias('Count')).orderBy('Letter')
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question
# MAGIC Produce a list of all the dates in October 2012. They can be output as a timestamp (with time set to midnight) or a date.   
# MAGIC https://pgexercises.com/questions/date/series.html

# COMMAND ----------

from pyspark.sql.functions import sequence, to_date, explode, lit,count

df=spark.range(1).select(explode(sequence(to_date(lit('2012-10-01')), to_date(lit('2012-10-31'))).alias('dates')))
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question
# MAGIC Return a count of bookings for each month, sorted by month    
# MAGIC https://pgexercises.com/questions/date/bookingspermonth.html

# COMMAND ----------

from pyspark.sql.functions import month, dayofmonth, col, date_format, concat, lit
df= bookings.withColumn('Month',date_format(col('starttime'),'yyyy-MM')).groupBy('Month').agg(count('bookid')).withColumn('Month',concat(col('Month'),lit('-01 00:00:00')))
display(df)