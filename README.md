#### Prerequisite 

•	Python IDE 
Kindly refer the link for the installation of PyCharm CE link   https://www.jetbrains.com/pycharm/download/other.html .
In case prefer to use the existing IDE- Kindly make sure the supporting version for python >3.7

•	Virtual Environment: To set up the VE in your workstation, refer this link https://sourabhbajaj.com/mac-setup/Python/virtualenv.html

•	Protobuf  & ProtoC : Protobuf is used to generate the message schema template, 
Refer this link for download and installation https://developers.google.com/protocol-buffers/docs/downloads

PROTOC_ZIP=protoc-3.14.0-osx-x86_64.zip curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v3.14.0/$PROTOC_ZIP
 sudo unzip -o $PROTOC_ZIP -d /usr/local bin/protoc 
  sudo unzip -o $PROTOC_ZIP -d /usr/local 'include/*' 
   rm -f $PROTOC_ZIP

 Can always use the below script to generate/update the message template script:     protoc -I=$SRC_DIR –python out=$DST_DIR $SRC_DIR/<MessageSchema>.proto 
•	Docker set up & installation 

#### Application Requirement Set up 
Pip install -r requirement.txt

#### Start the Kafka Cluster
docker-compose -f docker/docker-compose.yml up -d
 Create a Topic in the spark cluster and configure the topic name the producer and Consumer run script.

#### BUILD IMAGE:
sudo docker build -t {IMAGE}:{TAG} --target consumer/producer . -f docker/Dockerfile

#### How to run Producer & Consumer

PRODUCER:

docker run --network docker_default --name producer kafka-producer:v1.0 -b <BrokerName> -s <SchemaRegistry> -t <TopicName> -I <optional: InputFilename>

Eg: docker run --network docker_default --name producer kafka-producer:v1.0 -b 192.168.1.92:9092 -s http://192.168.1.92:8081 -t assignment


CONSUMER:
docker run --network docker_default --name producer kafka-producer:v1.0 -b <BrokerName> -s <SchemaRegistry> -t <TopicName> -g <>groupName>

Eg: docker run --network docker_default --name consumer kafka-consumer:v1.0 -b broker:9092 -s http://schema-registry:8081 -t assignment -g customerGroup

#### Stop the Kafka Cluster
docker-compose -f docker/docker-compose.yml down


![image](https://user-images.githubusercontent.com/37093793/132119987-134cf998-2c6b-484c-8ded-f95bb77d95a2.png)
