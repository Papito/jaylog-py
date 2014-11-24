import unittest
import json
import logging
import datetime
from string import Template
from jaylog import LogAdapter

class TestLogger(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.logger = LogAdapter(None)

    def test_arbitrary_constants(self):
        logger = LogAdapter(None, pid=12345, app='APP NAME')
        res = json.loads(logger._get_log_stmt(logging.INFO, None))
        
        self.assertEquals(res['pid'], 12345)
        self.assertEquals(res['app'], 'APP NAME')

    def test_simple_log_statement(self):
        stmt = 'simple log statement'
        res = json.loads(self.logger._get_log_stmt(logging.DEBUG, stmt))

        self.assertEquals(res['msg'], stmt)
    
    def test_with_string_formatting(self):
        stmt = 'simple log statement with variable $var'
        data = {'var': 1}
        res = json.loads(self.logger._get_log_stmt(logging.DEBUG, stmt, **data))

        self.assertEquals(res['msg'], Template(stmt).substitute(data))
        
    def test_tags(self):
        res = self.logger._get_log_stmt(logging.DEBUG, '', 'TAG1', 'TAG2')
        res = json.loads(res)

        self.assertEquals(len(res['tags']), 2)
        
    def test_custom_adapter(self):
        datetime_handler = lambda obj: (obj.isoformat() 
            if isinstance(obj, datetime.datetime) 
            or isinstance(obj, datetime.date) 
            else None)
            
        class CustomAdapter(LogAdapter):
            def to_json(self, data):
                return json.dumps(data, default=datetime_handler)

        logger = CustomAdapter(None)

        res = logger._get_log_stmt(
            logging.DEBUG, '$created', created = datetime.datetime.now()
        )
        res = json.loads(res)
        self.assertNotEquals(res[logger.LEVEL], 'ERROR')
        
    def test_core_fields(self):
        logger = LogAdapter(None)
        logger.MESSAGE = 'm'
        logger.LEVEL = 'l'
        logger.WITHOUT = 'w'
        res = logger._get_log_stmt(logging.DEBUG, '', w=[logger.LOCATION])
        res = json.loads(res)
        self.assertTrue(logger.MESSAGE in res)
        self.assertTrue(logger.LEVEL in res)
        self.assertFalse(logger.LOCATION in res)
        self.assertFalse(logger.WITHOUT in res)