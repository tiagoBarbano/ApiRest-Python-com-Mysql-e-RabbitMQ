import pika

def emit_user_profile_update(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel    = connection.channel()
    exchange_name = 'teste'
    routing_key   = 'teste1'

    channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)

    channel.basic_publish(exchange=exchange_name,
                          routing_key=routing_key,
                          body=message,
                          properties=pika.BasicProperties(delivery_mode = 2,))

    print("%r sent to exchange %r with data: %r" % (routing_key, exchange_name, message))
    connection.close()