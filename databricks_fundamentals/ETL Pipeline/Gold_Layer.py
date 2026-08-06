# Databricks notebook source
# MAGIC %md
# MAGIC # Setup

# COMMAND ----------

from pyspark.sql import functions as F, SparkSession
spark = SparkSession.builder.appName("Gold Layer").getOrCreate()

# COMMAND ----------

transactions=spark.table('databricks_fundamentals.silver.transactions')
cards=spark.table('databricks_fundamentals.silver.cards')
users=spark.table('databricks_fundamentals.silver.users')

# COMMAND ----------

fraud_pie_chart=transactions.withColumn('Fraud_Label', F.when(F.col('Fraud_Label')==True,'Fraud').when(F.col('Fraud_Label')==False,'Not Fraud').otherwise('Unknown')).groupBy("Fraud_Label").agg(F.count('Fraud_Label').alias('Fraud_Count'))
fraud_pie_chart.write.mode('overwrite').saveAsTable('databricks_fundamentals.gold.fraud_pie_chart')
display(fraud_pie_chart)

# COMMAND ----------

transactions=transactions.filter(F.col('Fraud_Label').isNotNull())

# COMMAND ----------

# MAGIC %md
# MAGIC # Analysis

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question 1: 
# MAGIC Which day(s) of the week sees the highest number of fraudulent transactions?

# COMMAND ----------

fraud_days=transactions.filter(F.col("Fraud_Label")==True).withColumn('dayOfWeekInNumbers',F.dayofweek(F.col('date'))).withColumn('Day_of_the_Week', F.date_format('date','EEEE')).groupBy('dayOfWeekInNumbers','Day_of_the_Week').agg(F.count('Fraud_Label').alias('Fraudulent_Transactions')).orderBy('dayOfWeekInNumbers').drop('dayOfWeekInNumbers')
fraud_days.write.mode('overwrite').saveAsTable('databricks_fundamentals.gold.fraud_days')
display(fraud_days)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question 2:
# MAGIC What is the trend of the fraud rate (fraudulent transactions divided by total) over the past month?

# COMMAND ----------

year_month_df=transactions.withColumn('Year-Month',F.date_format(F.col('date'),'yyyy-MM'))
total_transactions=year_month_df.groupBy('Year-Month').agg(F.count('id').alias('total_transactions')).orderBy('Year-Month')
fraud_transactions=year_month_df.filter(F.col('Fraud_Label')==True).groupBy('Year-Month').agg(F.count('id').alias('fraud_transactions')).orderBy('Year-Month')
Monthly_rate=total_transactions.join(fraud_transactions, on='Year-Month', how='left').withColumn('fraud_transactions',F.when(F.col('fraud_transactions').isNull(),0).otherwise(F.col('fraud_transactions'))).withColumn('Monthly_Rate',F.col('fraud_transactions')/F.col('total_transactions')).orderBy("Year-Month")
Monthly_rate.write.mode('overwrite').saveAsTable('databricks_fundamentals.gold.Monthly_rate')
display(Monthly_rate)

# COMMAND ----------

lastMonth=Monthly_rate.agg(F.max(F.col('Year-Month')))
lastMonthFiltered=Monthly_rate.filter(F.col('Year-Month')==lastMonth.first()[0])
display(lastMonthFiltered)




# COMMAND ----------

# MAGIC %md
# MAGIC ### Question 3
# MAGIC Which users have the largest number of flagged (“is_fraud = true”) transactions?

# COMMAND ----------

users_fraud_count=transactions.join(users,users.id==transactions.client_id,how='inner').filter(F.col('Fraud_Label')==True).groupBy('client_id').agg(F.count('transactions.id').alias('user_fraudlant_transactions_count')).orderBy('user_fraudlant_transactions_count', ascending=False)
users_fraud_count.write.mode('overwrite').saveAsTable('databricks_fundamentals.gold.users_fraud_count')
display(users_fraud_count)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question 4: 
# MAGIC Are there any users showing a sharp rise in transaction amount compared to their weekly average?

# COMMAND ----------


user_spike_rise=transactions.withColumn('year-week',F.concat_ws("-",F.year(F.col('date')),F.weekofyear(F.col('date')))).filter(F.col('amount')>0).groupBy('client_id','year-week').agg(F.avg('amount').alias('weekly_avg'),F.max('amount').alias('largest_transaction')).withColumn("spike_ratio", F.col("largest_transaction") / F.col("weekly_avg")).filter(F.col("spike_ratio") >= 2).orderBy('client_id').dropDuplicates()
user_spike_rise.write.mode('overwrite').saveAsTable('databricks_fundamentals.gold.user_spike_rise')
display(user_spike_rise)     

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question 5:
# MAGIC Which merchant categories exhibit the highest fraud rate?

# COMMAND ----------

merchant_category_total=transactions.groupBy('mcc','mcc_description').agg(F.count('id').alias('merchant_total_transactions'))
merchant_category_fraud=transactions.filter(F.col('Fraud_Label')==True).groupBy('mcc').agg(F.count('id').alias('merchant_fraud_transactions'))
merchant_category_fraud_rate=merchant_category_total.join(merchant_category_fraud,on='mcc',how='left').withColumn('merchant_fraud_transactions',F.when(F.col('merchant_fraud_transactions').isNull(),0).otherwise(F.col('merchant_fraud_transactions'))).withColumn('rate',F.col('merchant_fraud_transactions')/F.col('merchant_total_transactions')).orderBy(F.desc('rate')).dropDuplicates()
merchant_category_fraud_rate.write.mode('overwrite').saveAsTable('databricks_fundamentals.gold.merchant_category_fraud_rate')
display(merchant_category_fraud_rate)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question 6:
# MAGIC Are there specific merchants with unusually high fraud volume?

# COMMAND ----------

mcc_count_fraud=transactions.filter(F.col('Fraud_Label')==True).groupBy('mcc').agg(F.count('id').alias('count_fraud')).join(transactions.select('mcc','mcc_description'),on='mcc',how='inner').dropDuplicates().orderBy(F.desc('count_fraud'))
mcc_count_fraud.write.mode('overwrite').saveAsTable('databricks_fundamentals.gold.category_count_fraud')
display(mcc_count_fraud)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question 7:
# MAGIC How does fraud distribution vary by time of day (morning vs night)?    
# MAGIC - Analysis is made with morning being 5am - 11:59am and night being 8pm - 4:59am

# COMMAND ----------

morning=transactions.filter((F.hour(F.col('date')).between(5,11)) &(F.col('Fraud_Label')==True)).agg(F.count('id').alias('morning_fraud')).withColumn('ref_id',F.lit(1))
night=transactions.filter((F.hour("date").isin(20, 21, 22, 23, 0, 1, 2, 3, 4)) &(F.col('Fraud_Label')==True)).agg(F.count('id').alias('night_fraud')).withColumn('ref_id',F.lit(1))
morn_vs_night=morning.join(night,on='ref_id',how='inner').drop('ref_id')
morn_vs_night.write.mode('overwrite').saveAsTable('databricks_fundamentals.gold.morn_vs_night')
display(morn_vs_night)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question 8:
# MAGIC What’s the average transaction amount for fraud vs non-fraud transactions?

# COMMAND ----------

fraud_avg=transactions.filter(F.col('Fraud_Label')==True).agg(F.avg('amount').alias('avg_fraud'))
nonfraud_avg=transactions.filter(F.col('Fraud_Label')==False).agg(F.avg('amount').alias('avg_nonfraud'))
print(f"Average Fraud amount: {fraud_avg.collect()[0][0]}")
print(f"Average Non-Fraud Amount: {nonfraud_avg.collect()[0][0]}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question 9:
# MAGIC Which merchant category has the highest total fraud amount?

# COMMAND ----------

mcc_amount_fraud=transactions.filter(F.col('Fraud_Label')==True).groupBy('mcc').agg(F.sum('amount').alias('amount_fraud')).join(transactions.select('mcc','mcc_description'),on='mcc',how='inner').dropDuplicates().orderBy(F.desc('amount_fraud'))
mcc_amount_fraud.write.mode('overwrite').saveAsTable('databricks_fundamentals.gold.mcc_amount_fraud')
display(mcc_amount_fraud)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question 10:
# MAGIC What are the total monetary losses due to fraud each day?

# COMMAND ----------

total_daily_losses=transactions.filter((F.col('Fraud_Label')==True)&(F.col('amount')>0)).groupBy(F.date_format('date','yyyy-MM-dd').alias('date')).agg(F.sum('amount').alias('amount_fraud')).orderBy(F.desc('amount_fraud'))
total_daily_losses.write.mode('overwrite').saveAsTable('databricks_fundamentals.gold.total_daily_losses')
display(total_daily_losses)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question 11:
# MAGIC How many unique users commit fraudulent transactions per week?

# COMMAND ----------

user_count=transactions.filter(F.col('Fraud_Label')==True).withColumn('Year-Week',F.concat_ws('-',F.year(F.col('date')),F.weekofyear(F.col('date')))).groupBy('Year-Week').agg(F.count('client_id').alias('user_count')).dropDuplicates().orderBy('user_count',ascending=False)
user_count.write.mode('overwrite').saveAsTable('databricks_fundamentals.gold.user_count')
display(user_count)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question 12:
# MAGIC Do fraud patterns show seasonal or monthly spikes?

# COMMAND ----------

seasons_months=transactions.filter(F.col('Fraud_Label')==True).withColumn('Month',F.month(F.col('date'))).withColumn('Season',F.when(F.col('Month').isin(12,1,2), 'Winter').when(F.col('Month').isin(3,4,5), 'Spring').when(F.col('Month').isin(6,7,8), 'Summer').otherwise('Fall')).withColumn('Month',F.when(F.col('Month')==1,'January').when(F.col('Month')==2,'February').when(F.col('Month')==3,'March').when(F.col('Month')==4,'April').when(F.col('Month')==5,'May').when(F.col('Month')==6,'June').when(F.col('Month')==7,'July').when(F.col('Month')==8,'August').when(F.col('Month')==9,'September').when(F.col('Month')==10,'October').when(F.col('Month')==11,'November').when(F.col('Month')==12,'December'))
seasons=seasons_months.groupBy('Season').agg(F.count('id').alias('fraud_count')).dropDuplicates()
months=seasons_months.groupBy('Month').agg(F.count('id').alias('fraud_count')).dropDuplicates().orderBy('Month')
months.write.mode('overwrite').saveAsTable('databricks_fundamentals.gold.months')
seasons.write.mode('overwrite').saveAsTable('databricks_fundamentals.gold.seasons')
display(seasons)
display(months)

                                                                            

# COMMAND ----------

# MAGIC %md
# MAGIC ### Question 13:
# MAGIC How has user behavior changed before versus after a fraudulent event?    
# MAGIC Lets look in terms of RFM model

# COMMAND ----------

from pyspark.sql.window import Window

window=Window.partitionBy('client_id')
first_fraud_date=F.min(F.when(F.col('Fraud_Label')==True, F.col('date'))).over(window)
user_RFM = transactions.join(users, transactions.client_id==users.id, how='inner').orderBy('client_id').withColumn('first_fraud_date', first_fraud_date).filter(F.col('Fraud_Label')==False).withColumn('period', F.when(F.col('date') < F.col('first_fraud_date'), 'before_fraud').when(F.col('date') > F.col('first_fraud_date'), 'after_fraud'))
user_RFM=user_RFM.groupBy('client_id','period').agg(F.count(F.col('transactions.id')).alias('Frequency'), F.sum('amount').alias('Monetary'), F.when(F.col('period')=='after_fraud', F.min('date')).when(F.col('period')=='before_fraud', F.max('date')).alias('Recency')).dropDuplicates().orderBy('client_id','period')
display(user_RFM)

# COMMAND ----------

before=user_RFM.filter(F.col('period')=='before_fraud').withColumnRenamed('Frequency','Frequency_before').withColumnRenamed('Monetary','Monetary_before').withColumnRenamed('Recency','Recency_before').drop('period')
after=user_RFM.filter(F.col('period')=='after_fraud').withColumnRenamed('Frequency','Frequency_after').withColumnRenamed('Monetary','Monetary_after').withColumnRenamed('Recency','Recency_after').drop('period')
user_behaviour=before.join(after,on='client_id',how='inner')
user_behaviour.write.mode('overwrite').saveAsTable('databricks_fundamentals.gold.user_behaviour')
display(user_behaviour)


# COMMAND ----------

# MAGIC %md
# MAGIC ### Question 14:
# MAGIC Are fraudulent transactions more common on high-value purchases compared to low-value purchases?

# COMMAND ----------

high_value=transactions.filter((F.col('amount')>300)&(F.col('Fraud_Label')==True)).agg(F.count('id').alias('high_value_fraud')).withColumn('ref_id',F.lit(1))
low_value=transactions.filter((F.col('amount')<=300)&(F.col('amount')>0)&(F.col('Fraud_Label')==True)).agg(F.count('id').alias('low_value_fraud')).withColumn('ref_id',F.lit(1))
low_vs_high=low_value.join(high_value,on='ref_id',how='inner').drop('ref_id')
display(low_vs_high)