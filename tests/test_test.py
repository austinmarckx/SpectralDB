import logging
logger = logging.getLogger()
import unittest as ut

from src.utils.defaults import UNITTEST_SETUP_STRING
from src.utils.types import TestTuple, TestInputs, TestOutputs

from warnings import filterwarnings
from typing import Optional, Callable

class TestTest(ut.TestCase):
    """ Placeholder for some reusable building blocks"""

    def setUp(self):
        self.logger = logging.getLogger()
        filterwarnings("ignore",category=SyntaxWarning)
        logger.info("setUp")
        self.res = []
        
    def tearDown(self):
        logger.info("tearDown")

    def _conditions(self) -> list[TestTuple]:
        """ Get the test tuples """
        tests = [
            {"name":"Test Args no outputs", "inputs":{"args":("Test Argument",)}},   
            {"name":"Test Args empty outputs", "inputs":{"args":("Test Argument",)}, "outputs":{}},   
            {"name":"Test Args with output message", "inputs":{"args":("Test Argument",)}, "outputs":{"message":"Test Argument"}},   
            {"name":"Test Kwargs no outputs", "inputs":{"kwargs":{"message":"Test kwargs"}}},   
        ]        
        
        return  list(map(TestTuple.make, tests))


    def test_conditions(self):
        tests = self._conditions()
        print(f"Test list: {tests}")

        def _subtest(name:str, inputs:TestInputs, outputs:Optional[TestOutputs]=None, callable:Optional[Callable]=None):
            if callable is None:
                callable = lambda *args, **kwargs: f"Callable\n\tArgs: {args}\n\tKwargs: {kwargs}"

            print(f"Subtest: {name}")
            print(f"Inputs: {inputs}")
            args, kwargs = inputs.to_params()
            with self.subTest(name):
                outs = callable(*args, **kwargs)
                print(f"Outputs: {outs}")
                
                print(f"[SUCCESS] {name}")
                return outputs

            print(f"[FAIL] {name}")

        subtest_lambda = lambda test_tuple: _subtest(**test_tuple._asdict())
        self.res = list(map(subtest_lambda, tests))

        logger.debug(f"result: {self.res}")
    

    def test_start_tests(self):
        print(UNITTEST_SETUP_STRING)

if __name__ == '__main__':
    ut.main()


