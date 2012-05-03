import redis
import unittest

from redis.exceptions import ConnectionError

encode = lambda s: s.encode()

class PubSubTestCase(unittest.TestCase):
    def setUp(self):
        self.connection_pool = redis.ConnectionPool()
        self.client = redis.Redis(connection_pool=self.connection_pool)
        self.pubsub = self.client.pubsub()

    def tearDown(self):
        self.connection_pool.disconnect()

    def test_channel_subscribe(self):
        self.assertEquals(
            self.pubsub.subscribe('foo'),
            ['subscribe'.encode(), 'foo'.encode(), 1]
            )
        self.assertEquals(self.client.publish('foo', 'hello foo'), 1)
        self.assertEquals(
            next(self.pubsub.listen()),
            {
                'type': 'message'.encode(),
                'pattern': None,
                'channel': 'foo'.encode(),
                'data': 'hello foo'.encode()
            }
            )
        self.assertEquals(
            self.pubsub.unsubscribe('foo'),
            ['unsubscribe'.encode(), 'foo'.encode(), 0]
            )

    def test_pattern_subscribe(self):
        self.assertEquals(
            self.pubsub.psubscribe('fo*'),
            ['psubscribe'.encode(), 'fo*'.encode(), 1]
            )
        self.assertEquals(self.client.publish('foo', 'hello foo'), 1)
        self.assertEquals(
            next(self.pubsub.listen()),
            {
                'type': 'pmessage'.encode(),
                'pattern': 'fo*'.encode(),
                'channel': 'foo'.encode(),
                'data': 'hello foo'.encode()
            }
            )
        self.assertEquals(
            self.pubsub.punsubscribe('fo*'),
            ['punsubscribe'.encode(), 'fo*'.encode(), 0]
            )

class PubSubRedisDownTestCase(unittest.TestCase):
    def setUp(self):
        self.connection_pool = redis.ConnectionPool(port=6390)
        self.client = redis.Redis(connection_pool=self.connection_pool)
        self.pubsub = self.client.pubsub()

    def tearDown(self):
        self.connection_pool.disconnect()

    def test_channel_subscribe(self):
        got_exception = False
        try:
            self.pubsub.subscribe('foo')
        except ConnectionError:
            got_exception = True
        self.assertTrue(got_exception)
