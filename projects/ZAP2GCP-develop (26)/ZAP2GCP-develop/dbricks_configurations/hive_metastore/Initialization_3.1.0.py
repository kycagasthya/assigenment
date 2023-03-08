# Databricks notebook source
# MAGIC %md
# MAGIC ### The steps below are to be done one-time to initialise a new database with hive metastore schema version 3.1.0 ###
# MAGIC ##### execute the notebook cell by cell, and use a new cluster that can be deleted after the execution #####

# COMMAND ----------

# MAGIC %md
# MAGIC - Check that connectivity to MySQL database server is open

# COMMAND ----------

# MAGIC %sh
# MAGIC nc -vz 10.176.11.88 3306

# COMMAND ----------

# MAGIC %md
# MAGIC - Download Hadoop 3.1.0 and Hive 3.1.0 libraries. As cluster does not have internet connectivity, then the files are uploaded to bucket and downloaded from there
# MAGIC 
# MAGIC  - https://archive.apache.org/dist/hadoop/common/hadoop-3.1.0/hadoop-3.1.0.tar.gz
# MAGIC  - https://archive.apache.org/dist/hive/hive-3.1.0/apache-hive-3.1.0-bin.tar.gz

# COMMAND ----------

gcs_hadoop_tar = "gs://databricks-1235921161438059/1235921161438059/mnt/metastore-initialization/hadoop-3.1.0.tar.gz" 
gcs_hive_tar = "gs://databricks-1235921161438059/1235921161438059/mnt/metastore-initialization/apache-hive-3.1.0-bin.tar.gz"

dbutils.fs.rm("file:/tmp/hive-3.1.0")
dbutils.fs.mkdirs("file:/tmp/hive-3.1.0")
dbutils.fs.cp(gcs_hadoop_tar,"file:/tmp/hive-3.1.0/")
dbutils.fs.cp(gcs_hive_tar,"file:/tmp/hive-3.1.0/")

# COMMAND ----------

# MAGIC %md
# MAGIC - unzip the tar files

# COMMAND ----------

# MAGIC %sh 
# MAGIC tar -xvzf /tmp/hive-3.1.0/hadoop-3.1.0.tar.gz --directory /tmp/hive-3.1.0
# MAGIC tar -xvzf /tmp/hive-3.1.0/apache-hive-3.1.0-bin.tar.gz --directory /tmp/hive-3.1.0

# COMMAND ----------

dbutils.fs.ls("file:/tmp/hive-3.1.0/")

# COMMAND ----------

# MAGIC %md
# MAGIC - Remove sqlline and upload mysql connector
# MAGIC  - https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-8.0.27.tar.gz

# COMMAND ----------

# MAGIC %sh
# MAGIC rm -f /tmp/hive-3.1.0/apache-hive-3.1.0-bin/lib/sqlline-1.3.0.jar

# COMMAND ----------

gcs_mysql_tar = "gs://databricks-1235921161438059/1235921161438059/mnt/metastore-initialization/mysql-connector-java-8.0.27.tar.gz"

dbutils.fs.cp(gcs_mysql_tar,"file:/tmp/hive-3.1.0/apache-hive-3.1.0-bin/lib/")

# COMMAND ----------

# MAGIC %sh
# MAGIC tar -xvzf /tmp/hive-3.1.0/apache-hive-3.1.0-bin/lib/mysql-connector-java-8.0.27.tar.gz --directory /tmp/hive-3.1.0/apache-hive-3.1.0-bin/lib/
# MAGIC cp /tmp/hive-3.1.0/apache-hive-3.1.0-bin/lib/mysql-connector-java-8.0.27/mysql-connector-java-8.0.27.jar /tmp/hive-3.1.0/apache-hive-3.1.0-bin/lib/

# COMMAND ----------

# MAGIC %md
# MAGIC - Upload the hive-site.xml file containing connection details of the mysql database to be initialized
# MAGIC ##### !!! handle the hive-site.xml with care as it will contain the credentials for the database !!! #####
# MAGIC 
# MAGIC (Template has been provided here - gs://databricks-1235921161438059/1235921161438059/mnt/metastore-initialization/hive-site-template.xml)

# COMMAND ----------

dbutils.fs.cp("gs://databricks-1235921161438059/1235921161438059/mnt/metastore-initialization/hive-site.xml",
             "file:/tmp/hive-3.1.0/apache-hive-3.1.0-bin/conf/")

# COMMAND ----------

# MAGIC %md 
# MAGIC - Run the schema initialization tool

# COMMAND ----------

# MAGIC %sh
# MAGIC ls /usr/lib/jvm/

# COMMAND ----------

# MAGIC %md
# MAGIC Path variable changes are effective within a cell so set them and run the schematool

# COMMAND ----------

# MAGIC %sh
# MAGIC export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
# MAGIC export PATH=$JAVA_HOME/bin:$PATH
# MAGIC 
# MAGIC export HADOOP_HOME=/tmp/hive-3.1.0/hadoop-3.1.0
# MAGIC export PATH=$HADOOP_HOME/bin:$PATH
# MAGIC 
# MAGIC export HIVE_HOME=/tmp/hive-3.1.0/apache-hive-3.1.0-bin
# MAGIC export PATH=$HIVE_HOME/bin:$PATH
# MAGIC 
# MAGIC /tmp/hive-3.1.0/apache-hive-3.1.0-bin/bin/schematool -initSchema -dbType mysql

# COMMAND ----------

# MAGIC %md
# MAGIC ### Create an Init script to use with clusters so clusters can connect to mysql hive metastore ### 

# COMMAND ----------

# MAGIC %md
# MAGIC We need to host jars required for metastore 3.1.0 in a bucket and import them onto cluster during start
# MAGIC 
# MAGIC We will use the jars downloaded in the steps above

# COMMAND ----------

# MAGIC %sh
# MAGIC cp -r /tmp/hive-3.1.0/apache-hive-3.1.0-bin/lib/. /dbfs/mnt/metastore-initialization/cluster-jars/
# MAGIC cp -r /tmp/hive-3.1.0/hadoop-3.1.0/share/hadoop/common/lib/. /dbfs/mnt/metastore-initialization/cluster-jars/
# MAGIC cp /tmp/hive-3.1.0/apache-hive-3.1.0-bin/lib/mysql-connector-java-8.0.27/mysql-connector-java-8.0.27.jar /dbfs/mnt/metastore-initialization/cluster-jars/

# COMMAND ----------

# MAGIC %md
# MAGIC To enable clusters to connect to the metastore, update the spark config for the cluster - the below can be part of Cluster policy

# COMMAND ----------

spark.sql.hive.metastore.version 3.1.0
spark.hadoop.javax.jdo.option.ConnectionUserName {{secrets/hive-metastore-dev/username}}
spark.hadoop.javax.jdo.option.ConnectionPassword {{secrets/hive-metastore-dev/password}}
spark.hadoop.javax.jdo.option.ConnectionURL jdbc:mysql://10.176.11.88:3306/zap_dbx_dev
spark.hadoop.javax.jdo.option.ConnectionDriverName com.mysql.jdbc.Driver
spark.sql.hive.metastore.jars /hive_jars/cluster-jars/*

# COMMAND ----------

# MAGIC %md
# MAGIC Create init file with step to copy jars and also to set the spark config

# COMMAND ----------

contents = """#!/bin/sh

sleep 10s
mkdir /hive_jars
cp -r /dbfs/mnt/metastore-initialization/cluster-jars /hive_jars
"""

dbutils.fs.put(
    file = "dbfs:/mnt/metastore-initialization/ext_hive_metastore.sh",
    contents = contents,
    overwrite = True
)

# COMMAND ----------


