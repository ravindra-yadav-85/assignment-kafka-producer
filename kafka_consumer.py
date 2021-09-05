import argparse
# Protobuf generated class; resides at ./user_pb2.py
from proto import transaction_pb2
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
from confluent_kafka.serialization import StringDeserializer
from collections import defaultdict


def main(args):
    topic = args.topic

    protobuf_deserializer = ProtobufDeserializer(transaction_pb2.Transaction)
    string_deserializer = StringDeserializer('utf_8')

    consumer_conf = {'bootstrap.servers': args.bootstrap_servers,
                     'key.deserializer': string_deserializer,
                     'value.deserializer': protobuf_deserializer,
                     'group.id': args.group,
                     'auto.offset.reset': "earliest"}

    consumer = DeserializingConsumer(consumer_conf)
    consumer.subscribe([topic])
    account_dict = defaultdict(float)

    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(1.0)
            # print(msg)
            if msg is None:
                continue

            transaction = msg.value()
            if transaction is not None:
                # print("transaction record {}: account no: {}\n"
                #       "\tamount: {}\n"
                #       .format(msg.key(), transaction.account_number,
                #               transaction.amount))
                if transaction.account_number in account_dict:
                    addition = account_dict[transaction.account_number] + transaction.amount
                    account_dict[transaction.account_number] = addition
                else:
                    account_dict[transaction.account_number] = transaction.amount
                print("Account number: {} have sum of :{} amount\n" .format(transaction.account_number, account_dict[transaction.account_number]))

        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="DeserializingConsumer Example")
    parser.add_argument('-b', dest="bootstrap_servers", required=True,
                        help="Bootstrap broker(s) (host[:port])")
    parser.add_argument('-s', dest="schema_registry", required=True,
                        help="Schema Registry (http(s)://host[:port]")
    parser.add_argument('-t', dest="topic", default="example_serde_protobuf",
                        help="Topic name")
    parser.add_argument('-g', dest="group", default="example_serde_protobuf",
                        help="Consumer group")

    main(parser.parse_args())