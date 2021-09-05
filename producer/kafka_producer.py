import argparse
from uuid import uuid4
from proto import transaction_pb2
# import proto.transaction_pb2 as transaction_pb2
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from google.protobuf.timestamp_pb2 import Timestamp
import csv


def delivery_report(err, msg):
    if err is not None:
        print("Delivery failed for Transaction record {}: {}".format(msg.key(), err))
        return
    print('Transaction record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


def main(args):
    topic = args.topic
    file = args.filename

    schema_registry_conf = {'url': args.schema_registry}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    protobuf_serializer = ProtobufSerializer(transaction_pb2.Transaction,
                                             schema_registry_client)

    producer_conf = {'bootstrap.servers': args.bootstrap_servers,
                     'key.serializer': StringSerializer('utf_8'),
                     'value.serializer': protobuf_serializer}

    producer = SerializingProducer(producer_conf)

    print("Producing transaction records to topic {}. ^C to exit.".format(topic))
    while True:
        # Serve on_delivery callbacks from previous calls to produce()
        producer.poll(0.0)
        try:
            with open(file) as file:
                reader = csv.DictReader(file, delimiter=",")
                for row in reader:
                    timestamp = Timestamp()
                    timestamp.GetCurrentTime()
                    transaction = transaction_pb2.Transaction(transaction_id=str(uuid4()),
                                                              account_number=row["account_no"],
                                                              transaction_reference=row["transaction_details"],
                                                              transaction_datetime=timestamp,
                                                              amount=float(row["amount"]))
                    producer.produce(topic=topic, key=str(uuid4()), value=transaction, on_delivery=delivery_report)
        except KeyboardInterrupt:
            break
        except ValueError:
            print("Invalid input, discarding record...")
            continue

    print("\nFlushing records...")
    producer.flush()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="SerializingProducer Example")
    parser.add_argument('-b', dest="bootstrap_servers", required=True,
                        help="Bootstrap broker(s) (host[:port])")
    parser.add_argument('-s', dest="schema_registry", required=True,
                        help="Schema Registry (http(s)://host[:port]")
    parser.add_argument('-t', dest="topic", default="example_serde_protobuf",
                        help="Topic name")
    parser.add_argument('-f', dest="filename", default="../input/bank_data.csv",
                        help="Topic name")

    main(parser.parse_args())