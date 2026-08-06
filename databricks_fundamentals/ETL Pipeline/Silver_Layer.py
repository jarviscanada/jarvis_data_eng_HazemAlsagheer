# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, date_format, to_timestamp,col, round, when,isnan
from pyspark.sql.types import StructType,MapType, StructField, StringType
spark=SparkSession.builder.appName("Silver Layer").getOrCreate()

# COMMAND ----------

# MAGIC %md
# MAGIC # Table SetUp

# COMMAND ----------

transactions=spark.table('databricks_fundamentals.bronze.transactions_data')
cards=spark.table('databricks_fundamentals.bronze.cards_data')
users=spark.table('databricks_fundamentals.bronze.users_data')

# COMMAND ----------


mcc_df = spark.read.option("multiLine", "true").json(
    "/Volumes/databricks_fundamentals/bronze/volume/mcc_codes.json"
)

mcc_dict = mcc_df.collect()[0].asDict()
mcc=spark.createDataFrame(mcc_dict.items(),['mcc_code','mcc_description'])
mcc.write.mode("overwrite").saveAsTable("databricks_fundamentals.silver.mcc_codes")

# COMMAND ----------

schema=StructType([
    StructField('target', MapType(StringType(), StringType(), True))
])
train_df = spark.read.schema(schema).json("/Volumes/databricks_fundamentals/bronze/volume/train_fraud_labels.json")

train_fraud_label=train_df.select(explode('target').alias('Id','Fraud_Label'))
train_fraud_label.write.mode('overwrite').saveAsTable('databricks_fundamentals.silver.train_fraud_labels')

# COMMAND ----------

# MAGIC %md
# MAGIC # Data Cleaning

# COMMAND ----------

# MAGIC %md
# MAGIC ## Transactions Data

# COMMAND ----------

complete_transactions=transactions.join(mcc,transactions.mcc==mcc.mcc_code,how='inner').drop(mcc.mcc_code).join(train_fraud_label,transactions.id==train_fraud_label.Id,how='left').drop(train_fraud_label.Id)
display(complete_transactions)

# COMMAND ----------

cnt=[complete_transactions.filter(col(c).isNull()).count() for c in complete_transactions.columns]
null_df=spark.createDataFrame([cnt],complete_transactions.columns)
display(null_df)

# COMMAND ----------

complete_transactions.count()

# COMMAND ----------

merstateNull=complete_transactions.filter(col("merchant_state").isNull())
uniqueValues= [row[0] for row in merstateNull.select(col('merchant_city')).distinct().collect()]
nullcount=merstateNull.filter(col('zip').isNull()).count()
display(f"merstateNullCount: {merstateNull.count()}, zipNullcount:{nullcount}, Merchant cities when zip and state are null: {uniqueValues}")

# COMMAND ----------

modified_transactions=complete_transactions.withColumn('date',to_timestamp('date','yyyy-MM-dd HH:mm:ss')).withColumn('amount', round(col("amount"),2)).withColumn('Fraud_Label',when(col('Fraud_Label')=='Yes',True).when(col('Fraud_Label')=='No',False).otherwise(None)).dropDuplicates()
modified_transactions.write.mode('overwrite').saveAsTable('databricks_fundamentals.silver.transactions')


# COMMAND ----------

# MAGIC %md
# MAGIC ## Cards Data

# COMMAND ----------

cnt=[cards.filter(col(c).isNull()).count() for c in cards.columns]
null_df=spark.createDataFrame([cnt],cards.columns)
display(null_df)

# COMMAND ----------

modified_cards=cards.withColumn('credit_limit',round(col('credit_limit'),2))\
    .withColumn('has_chip', when(col('has_chip')=='YES', True).when(col('has_chip')=='NO',False).otherwise(None)).\
    withColumn('card_on_dark_web',when(col('card_on_dark_web')=='Yes',True).when(col('card_on_dark_web')=='No',False).otherwise(None)).dropDuplicates()
modified_cards.write.mode('overwrite').saveAsTable('databricks_fundamentals.silver.cards')

# COMMAND ----------

# MAGIC %md
# MAGIC ## Users Data

# COMMAND ----------

cnt=[users.filter(col(c).isNull()).count() for c in users.columns]
null_df=spark.createDataFrame([cnt],users.columns)
display(null_df)

# COMMAND ----------

modified_users=users.withColumn('per_capita_income',round(col('per_capita_income'),2)).\
    withColumn('yearly_income',round(col('yearly_income'),2)).\
    withColumn('total_debt',round(col('total_debt'),2)).\
    dropDuplicates()


modified_users.write.mode('overwrite').saveAsTable('databricks_fundamentals.silver.users')


# COMMAND ----------

display(train_fraud_label)

# COMMAND ----------

display(mcc)

# COMMAND ----------

