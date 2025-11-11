import logging
logger = logging.getLogger()
import unittest as ut

import src.utils.io as io
from src.utils.types import TestTuple, TestInputs, TestOutputs

from warnings import filterwarnings
from typing import Optional, Callable

class TestIO(ut.TestCase):
    """ I/O test cases"""

    def setUp(self):
        self.logger = logging.getLogger()
        filterwarnings("ignore",category=SyntaxWarning)
        logger.info("setUp")
        self.res = []
        
    def tearDown(self):
        logger.info("tearDown")

    def _element_abbreviation_conditions(self) -> list[TestTuple]:
        """ Get the test tuples """
        tests = [
            {"name":"Test expected", "inputs":{"args":("He",)}, "outputs":"He"},         
            {"name":"Test long", "inputs":{"args":("Lead",)}, "outputs":"Pb"},
            {"name":"Test caps", "inputs":{"args":("HE",)}, "outputs":"He"},
            {"name":"Test lower", "inputs":{"args":("he",)}, "outputs":"He"},      
        ]        
        
        return  list(map(TestTuple.make, tests))


    def test_element_abbreviation(self):
        tests = self._element_abbreviation_conditions()
        def _subtest(name:str, inputs:TestInputs, outputs:Optional[TestOutputs]=None, callable:Optional[Callable]=io.process_element_abbreviation):
            args, kwargs = inputs.to_params()
            with self.subTest(name):
                outs = callable(*args, **kwargs)
                self.assertEqual(outs, outputs.outputs)
                return f"[SUCCESS] {name}"
            return(f"[FAIL] {name}")

        subtest_lambda = lambda test_tuple: _subtest(**test_tuple._asdict())
        self.res = list(map(subtest_lambda, tests))
        print(f"Element Abbreviation Result: {self.res}")
    
    def _load_element_conditions(self) -> list[TestTuple]:
        """ Just checking running this doesn't throw error """
        tests = [
            {"name":"Test expected", "inputs":{"args":("He",)}},         
            {"name":"Test long", "inputs":{"args":("HE",)}},
            {"name":"Test lower", "inputs":{"args":("he",)}},      
        ]        
        
        return  list(map(TestTuple.make, tests))

    def test_load_element(self):
        tests = self._load_element_conditions()

        def _subtest(name:str, inputs:TestInputs, outputs:Optional[TestOutputs]=None, callable:Optional[Callable]=io.load_element):
            args, kwargs = inputs.to_params()
            with self.subTest(name):
                outs = callable(*args, **kwargs)
                # So long as not error, success
                return f"[SUCCESS] {name}"
            return(f"[FAIL] {name}")

        subtest_lambda = lambda test_tuple: _subtest(**test_tuple._asdict())
        self.res = list(map(subtest_lambda, tests))
        print(f"Load Element Result: {self.res}")



if __name__ == '__main__':
    ut.main()


