from kafka import KafkaConsumer

# 创建Kafka消费者
consumer = KafkaConsumer(
    'weather-data',
    bootstrap_servers=['master:9092'],
    auto_offset_reset='earliest',  # 从最早的offset开始读取
    group_id='my-group'  # 消费者组ID
)

# 读取并打印消息
for message in consumer:
    print(message.value.decode('utf-8'))
