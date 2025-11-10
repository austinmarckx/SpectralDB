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
            {"name":"Test long", "inputs":{"args":("Helium",)}, "outputs":"He"},
            {"name":"Test caps", "inputs":{"args":("HELIUM",)}, "outputs":"He"},
            {"name":"Test lower", "inputs":{"args":("he",)}, "outputs":"He"},      
        ]        
        
        return  list(map(TestTuple.make, tests))


    def test_element_abbreviation(self):
        tests = self._element_abbreviation_conditions()
        print(f"Test list: {tests}")

        def _subtest(name:str, inputs:TestInputs, outputs:Optional[TestOutputs]=None, callable:Optional[Callable]=io.process_element_abbreviation):
            if callable is None:
                callable = lambda *args, **kwargs: f"Callable\n\tArgs: {args}\n\tKwargs: {kwargs}"

            print(f"Subtest: {name}")
            print(f"Inputs: {inputs}")
            args, kwargs = inputs.to_params()
            with self.subTest(name):
                outs = callable(*args, **kwargs)
                print(f"Outputs: {outs}")
                self.assertEqual(outs, outputs.outputs)
                print(f"[SUCCESS] {name}")
                return outputs

            print(f"[FAIL] {name}")

        subtest_lambda = lambda test_tuple: _subtest(**test_tuple._asdict())
        self.res = list(map(subtest_lambda, tests))

        logger.debug(f"result: {self.res}")
    


if __name__ == '__main__':
    ut.main()


