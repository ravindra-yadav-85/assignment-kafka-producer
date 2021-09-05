#### Project Overview
[![Build Status](https://jenkins.datasparkanalytics.com/buildStatus/icon?job=DS_algo)](https://jenkins.datasparkanalytics.com/job/DS_algo)

Create an application that acts as a Kafka producer and sends ‘transaction’ events using the schema below:
transaction: {
transaction_id: string,
account_number: string, transaction_reference: string, transaction_datetime: timestamp, amount: double,
}
The application will need to send at least 1000 transactions across 20 customers across a single topic.
Write a second application that acts as a Kafka consumer to subscribe to the topic and upon receipt of each message logs a tuple of (account_number, sum(amount)), i.e. the total value of the transactions made by the customer while the application has been running.

* Use a protobuf to serialize the messages.
* Create the producer and consumer in different languages, one in python and one in
scala, you can choose which language you want for each component
* Package the two different applications in docker containers and orchestrate the
container deployments using either docker-compose or a local kubernetes cluster

![image](https://user-images.githubusercontent.com/37093793/132120383-a2b985c4-14d5-4688-9760-2b2222ecb6b4.png)

#### Dependencies
```
* Python IDE
Kindly refer the link for the installation of PyCharm CE link   https://www.jetbrains.com/pycharm/download/other.html .
In case prefer to use the existing IDE- Kindly make sure the supporting version for python >3.7

* Virtual Environment: To set up the VE in your workstation, refer this link https://sourabhbajaj.com/mac-setup/Python/virtualenv.html

* Protobuf  & ProtoC : Protobuf is used to generate the message schema template, 
Refer this link for download and installation https://developers.google.com/protocol-buffers/docs/downloads

PROTOC_ZIP=protoc-3.14.0-osx-x86_64.zip curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v3.14.0/$PROTOC_ZIP
 sudo unzip -o $PROTOC_ZIP -d /usr/local bin/protoc 
  sudo unzip -o $PROTOC_ZIP -d /usr/local 'include/*' 
   rm -f $PROTOC_ZIP

 Can always use the below script to generate/update the message template script:     protoc -I=$SRC_DIR –python out=$DST_DIR $SRC_DIR/<MessageSchema>.proto 
* Docker set up & installation
```

#### Application Requirement Set up 
``` 
Pip install -r requirement.txt
``` 

#### Start the Kafka Cluster
```
docker-compose -f docker/docker-compose.yml up -d
```

#### BUILD IMAGE:
 ```
sudo docker build -t {IMAGE}:{TAG} --target consumer/producer . -f docker/Dockerfile

e.g. docker build -t kafka-producer:v1.0 --target producer . -f docker/Dockerfile
e.g. docker build -t kafka-consumer:v1.0 --target consumer . -f docker/Dockerfile
```

#### How to run Producer & Consumer
USING docker
```
PRODUCER:
docker run --network docker_default --name producer kafka-producer:v1.0 -b <BrokerName> -s <SchemaRegistry> -t <TopicName> -i <optional: InputFilename>

Eg: docker run --network docker_default --name producer kafka-producer:v1.0 -b broker:9092 -s http://schema-registry:8081-t assignment


CONSUMER:
docker run --network docker_default --name producer kafka-producer:v1.0 -b <BrokerName> -s <SchemaRegistry> -t <TopicName> -g <>groupName>

Eg: docker run --network docker_default --name consumer kafka-consumer:v1.0 -b broker:9092 -s http://schema-registry:8081 -t assignment -g customerGroup
```
 
USING docker-compose:
```    
1. Run the docker compose file [do not forgot to update the {IMAGE}:{TAG}]
 
 docker-compose -f docker/docker-compose-prod-cons.yml up -d

2. Follow the logs the see the messages consumed by consumer 
 
 docker-compose -f docker/docker-compose-prod-cons.yml logs --f

3. Stop the producer and consumer process 
 
 docker-compose -f docker/docker-compose-prod-cons.yml down

#### Stop the Kafka Cluster
docker-compose -f docker/docker-compose.yml down
``` 

#### Tradeoffs compared to alternative solutions
 ```
 Schema Registry Vs Custom SerDer
 1. Support Schema evolution
 2. Maintained versioned history of all schemas
 3. RESTful interface for storing and retrieving
 4. Serializers that plug into Kafka clients
 5. Schema Registry lives outside of and separately from your Kafka brokers and clients
 ```


#### Potential Improvements
 ```
 1. Producing the messages from actual source
 2. Setup the required partitions and creating multiple consumers to achive the throughput
 3. Store the aggregated o/p in datastore
 4. Multiple zookeeper setup for HA
 5. Multiple replication of messages
 ```


