---------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------
																		STEPS FOR PREDICTIVE MAINTENANCE FOR BATCH MODE PART
---------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------

1. Start Zookeeper Server

zkServer.sh start /usr/local/zookeeper/config/zookeeper.properties


2. Start Kafka Server

kafka-server-start.sh /usr/local/kafka/config/server.properties


3. Create a kafka topic

kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic <topic-name>


4. You can check that your topic is created ot not using the following command

kafka-topics.sh --list --zookeeper localhost:2181


5. Start a Kafka Producer to produce live data for that

kafka-console-producer.sh --broker-list localhost:9092 --topic sensor


6. Start Hadoop and its services


7. Configure flume agent for HDFS to get data from Kafka

Configuration file: kafka.config

#	Flume	config	to	listen	to	Kakfa	topic	and	write	to	HDFS.
flume1.sources	=	kafka-source-1
flume1.channels	=	hdfs-channel-1
flume1.sinks	=	hdfs-sink-1
#	For	each	source,	channel,	and	sink,	set
#	standard	properties.
flume1.sources.kafka-source-1.type	=	org.apache.flume.source.kafka.KafkaSource
flume1.sources.kafka-source-1.zookeeperConnect	=	localhost:2181
flume1.sources.kafka-source-1.topic	=	sensor
flume1.sources.kafka-source-1.batchSize	=	100
flume1.sources.kafka-source-1.channels	=	hdfs-channel-1
flume1.channels.hdfs-channel-1.type	=	memory
flume1.sinks.hdfs-sink-1.channel	=	hdfs-channel-1
flume1.sinks.hdfs-sink-1.type	=	hdfs
flume1.sinks.hdfs-sink-1.hdfs.writeFormat	=	Text
flume1.sinks.hdfs-sink-1.hdfs.fileType	=	DataStream
flume1.sinks.hdfs-sink-1.hdfs.filePrefix	=	sensor
flume1.sinks.hdfs-sink-1.hdfs.useLocalTimeStamp	=	true
flume1.sinks.hdfs-sink-1.hdfs.path	=	/flume_data/%{topic}-data/%y-%m-%d
flume1.sinks.hdfs-sink-1.hdfs.rollCount=100
flume1.sinks.hdfs-sink-1.hdfs.rollSize=0
#	Other	properties	are	specific	to	each	type	of
#	source,	channel,	or	sink.	In	this	case,	we
#	specify	the	capacity	of	the	memory	channel.
flume1.channels.hdfs-channel-1.capacity	=	10000


8. Create the designated directory in HDFS


9. Start the flume agent services

flume-ng agent --conf conf --conf-file /home/mayank/flume/kafka.conf --name flume1 -Dflume.root.logger=INFO,console


10. Open the HDFS web interface and check that file or data is going into the HDFS or not.


11. Built the pig script that will take the data stored in hdfs and remove all intermediate blank line between two records.
Name of pig script : dataCleansing.pig


12. Make a shel script that will trigger your pig script to an execution on a daily basis.
Name of shell script : daily_scheduler.sh


13. Now your data is cleansed and stored in hdfs see new folder configuration pig and shell script.


14. Write a hive script named as SensorSchema.hql that will make an external table on the newly cleansed data.
Run this as : hive -f SensorSchema.hpl


15. Open hive terminal and check that table is created or not.


16. Do batch analytics on this table. 

<--------------------------------------------------------------------------------------------------------------------------->

SUCCESSFULL............

<--------------------------------------------------------------------------------------------------------------------------->
