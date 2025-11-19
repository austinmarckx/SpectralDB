import logging
import unittest as ut
import numpy as np
from functools import partial
from spectraldb.utils.log import Log
from spectraldb.utils.io import process_element_abbreviation, load_element
from spectraldb.utils.types import TestTuple, TestInputs, TestOutputs, NamedWorkingSpace
from spectraldb.models.lindbloom import WORKING_SPACES_DICT, get_working_space, create_working_space

from warnings import filterwarnings
from typing import Optional, Callable

class TestColorspaces(ut.TestCase):
    """ Working space validation"""

    def setUp(self):
        filterwarnings("ignore",category=SyntaxWarning)
        Log.log("Setup", logging.DEBUG)
        self.res = []
        
    def tearDown(self):
        Log.log("Tear down", logging.DEBUG)

    def _create_working_spaces_conditions(self) -> list[TestTuple]:
        """ Get the test tuples """
        tests = [{"name":f"Test {name}", "inputs":{"kwargs":{"ws":name}}} for name in WORKING_SPACES_DICT]               
        return  list(map(TestTuple.make, tests))


    def test_create_working_spaces(self):
        tests = self._create_working_spaces_conditions()
        
        def _subtest(name:str, inputs:TestInputs, outputs:Optional[TestOutputs]=None, func:Optional[Callable]=None):
            args, kwargs = inputs.to_params()
            ws = kwargs.pop("ws")
            space = get_working_space(ws)
            r, g, b = space.primaries()
            
            if func is None:
                func = partial(create_working_space, name=ws, red=r, green=g, blue=b, ill=space.ill) 
            
            with self.subTest(name):
                outs = func(*args, **kwargs)
                self.assertTupleEqual(space.primaries(), outs.primaries())
                np.testing.assert_allclose(space.M, outs.M, atol=1e-5)
                np.testing.assert_allclose(space.M_inv, outs.M_inv, atol=1e-5)
                return f"[SUCCESS] {name}"
            return(f"[FAIL] {name}")

        subtest_lambda = lambda test_tuple: _subtest(**test_tuple._asdict())
        self.res = list(map(subtest_lambda, tests))
        print(f"Working Space Creation Result: {self.res}")
    
    


if __name__ == '__main__':
    ut.main()


