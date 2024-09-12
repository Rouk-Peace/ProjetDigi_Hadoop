cp /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar .
./start-hadoop.sh
start-hbase.sh
./hbase_drop.sh
./hbase_create.sh
hbase-daemon.sh start thrift
hdfs dfs -mkdir -p input
hdfs dfs -rm input/dataw_fro03.csv
hdfs dfs -put dataw_fro03.csv input
hdfs dfs -rm -r outputprojet
hadoop jar hadoop-streaming-2.7.2.jar -file mapper.py -mapper "python3 mapper_projet.py" -file reducer.py -reducer "python3 reducer_projet.py" -input input/dataw_fro03 -output outputprojet
