import logging
logger = logging.getLogger()
import unittest as ut

import src.utils.preprocess as pp
from src.utils.defaults import ELEMENTS_R
from src.utils.types import TestTuple, TestInputs, TestOutputs

from warnings import filterwarnings
from typing import Optional, Callable

class TestPreprocess(ut.TestCase):
    """Test if all elements can be preprocessed"""

    def setUp(self):
        self.logger = logging.getLogger()
        filterwarnings("ignore",category=SyntaxWarning)
        logger.info("setUp")
        self.res = []
        
    def tearDown(self):
        logger.info("tearDown")

    def _preprocessing_conditions(self) -> list[TestTuple]:
        """ Get the test tuples """
        tests = [{"name":f"Test {el}", "inputs":{"args":(el,), "kwargs":{"trimmed":True}}} for el in ELEMENTS_R]        
        return  list(map(TestTuple.make, tests))

    def test_preprocessing(self):
        tests = self._preprocessing_conditions()
        def _subtest(name:str, inputs:TestInputs, outputs:Optional[TestOutputs]=None, func:Optional[Callable]=None):
            if func is None:
                func = pp.preprocess
            args, kwargs = inputs.to_params()
            with self.subTest(name):
                outs = func(*args, **kwargs)
                # So long as not error, success
                return f"[SUCCESS] {name}"
            return(f"[FAIL] {name}")

        subtest_lambda = lambda test_tuple: _subtest(**test_tuple._asdict())
        self.res = list(map(subtest_lambda, tests))
        print(f"Preprocessing Result: {self.res}")




if __name__ == '__main__':
    ut.main()


