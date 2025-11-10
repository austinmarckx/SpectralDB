import logging
logger = logging.getLogger()
import unittest as ut
from utils.defaults import  UNITTEST_SETUP_STRING
from utils.types import TestTuple
from typing import List, Dict, Any, Optional

class TestTest(ut.TestCase):
    """ Placeholder for some reusable building blocks"""

    def setUp(self):
        self.logger = logging.getLogger()
        logger.info("setUp")
        self.res = []
        
    def tearDown(self):
        logger.info("tearDown")

    def _conditions(self) -> List[TestTuple]:
        """ Get the test tuples """
        tests = [
            {"name":"condition 1", "inputs":{"param":"Test", "args":(5,10), "ray_callable":"tune.randint"}, "outputs":None},   
        ]        
        tests = list(map(dict.values, tests))
        return  list(map(TestTuple._make, tests))


    def test_conditions(self):
        tests = self._conditions()
        logger.debug(f"Test list: {tests}")
        
        def _subtest(name:str, inputs:Dict, outputs:Optional[Any]=None, *args, **kwargs):
            logger.info(f"Subtest: {name}")
            logger.debug(f"Inputs: {inputs}")
            with self.subTest(name):
                curr = None
                logger.debug(f"[SUCCESS] {name}")
                return curr
            logger.debug(f"[FAIL] {name}")

        subtest_lambda = lambda test_tuple: _subtest(**test_tuple._asdict())
        self.res = list(map(subtest_lambda, tests))

        logger.debug(f"result: {self.res}")
    

    def test_start_tests(self):
        print(UNITTEST_SETUP_STRING)

if __name__ == '__main__':
    ut.main()


