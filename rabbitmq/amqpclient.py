'''
@author: Fubai Zhong
'''
import logging
import time
from amqp import Connection, Message, AMQPError

logger = logging.getLogger('amqpclient')

class AMQPClient(object):
    """docstring for AMQPClient"""
    def __init__(self, host = 'localhost', userid = 'guest',
                    password = 'guest', virtual_host = '/', heartbeat = 0):
        super(AMQPClient, self).__init__()
        self.conn_params = {
            'host': host,
            'userid': userid,
            'password': password,
            'virtual_host': virtual_host,
            'heartbeat': heartbeat,
        }
        self.conn = None
        self.channel = None

    def _ensure(self):
        if self.conn:
            if self.conn.is_alive():
                return
            else:
                self.close()

        self.conn = Connection(**self.conn_params)

    def close(self):
        if not self.conn:
            return
        try:
            self.conn.close()
        except:
            pass
        self.conn = None

    def _queue(self, queue = None, exchange = None, exchange_type = 'direct', routing_key = None):
        self._ensure()

        channel = self.conn.channel()
        channel.queue_declare(queue = queue, durable = True, exclusive = False, auto_delete = False)
        channel.exchange_declare(exchange = exchange, type = exchange_type, durable = True, auto_delete = False)
        channel.queue_bind(queue = queue, exchange = exchange, routing_key = routing_key)

        return channel

    def queue(self, queue = None, exchange = None, exchange_type = 'direct', routing_key = None):
        channel = self._queue(queue, exchange, exchange_type, routing_key)
        return AMQPQueue(self, channel, queue, exchange, exchange_type, routing_key)

    def wait(self, timeout = None):
        self._ensure()
        self.conn.drain_events(timeout = timeout)

class AMQPQueue(object):
    """docstring for AMQPQueue"""
    def __init__(self, client, channel, queue, exchange, exchange_type, routing_key):
        super(AMQPQueue, self).__init__()
        self.channel = channel
        self.client = client
        self.queue = queue
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.routing_key = routing_key
        self.consumer_tag = None

    def reopen(self):
        self.channel = self.client._queue(queue = self.queue,
                                    exchange = self.exchange,
                                    exchange_type = self.exchange_type,
                                    routing_key = self.routing_key)

    def basic_cancel(self, retry = True):
        self.channel.basic_cancel(consumer_tag = self.consumer_tag)

    def basic_publish(self, body, properties = {}):
        properties['delivery_mode'] = 2
        msg = Message(body, **properties)
        self.channel.basic_publish(exchange = self.exchange, routing_key = self.routing_key, msg = msg)

    def basic_get(self, no_ack = False):
        return self.channel.basic_get(self.queue, no_ack = False)

    def basic_ack(self, msg):
        return self.channel.basic_ack(delivery_tag = msg.delivery_tag)

    def basic_consume(self, consumer_tag='', no_local=False,
        no_ack=False, exclusive=False, nowait=False,
        callback=None, on_cancel=None):
        if self.consumer_tag:
            self.basic_cancel()
        self.consumer_tag = self.channel.basic_consume(
                    queue = self.queue,
                    consumer_tag = consumer_tag,
                    no_local = no_local,
                    no_ack = no_ack,
                    exclusive = exclusive,
                    nowait = nowait,
                    callback = callback,
                    on_cancel = on_cancel,
                )

    def basic_qos(self, prefetch_size = 0, prefetch_count = 0, a_global = False):
        # not implemented.
        # self.channel.basic_qos(prefetch_size, prefetch_count, a_global)
        pass

    def wait(self, timeout = None):
        return self.client.wait(timeout = timeout)

if __name__ == "__main__":
    client = AMQPClient(host = '127.0.0.1')
    # client.basic_qos(prefetch_size = 1)

    begin = time.time() * 1000
    producer = client.queue('test_queue', 'test_exchange', 'direct', 'test_key')
    end = time.time() * 1000
    print '[perf] open_queue %dms' % ((end - begin))

    begin = time.time() * 1000

    for i in range(100):
        body = 'message %d' % (i)
        print 'publish: %s' % (body)
        producer.basic_publish(body)
        # time.sleep(1)
    end = time.time() * 1000
    print '[perf] publish %dms' % ((end - begin))

    consumer = client.queue('test_queue', 'test_exchange', 'direct', 'test_key')
    while True:
        msg = consumer.basic_get()
        if not msg:
            break
        print 'consume: %s' % (msg.body)
        consumer.basic_ack(msg)

    def consume_callback(msg):
        print 'consume: %s' % (msg.body)
        consumer.basic_ack(msg)
    consumer.basic_consume(callback = consume_callback)

    while True:
        consumer.wait()

    client.close()
