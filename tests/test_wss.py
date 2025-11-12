import logging
logger = logging.getLogger()
import unittest as ut

from spectraldb.models import wss as wss
from spectraldb.utils.types import TestTuple, TestInputs, TestOutputs
from spectraldb.utils.misc import nothing_burger

from warnings import filterwarnings
from typing import Optional, Callable

class TestWSS(ut.TestCase):
    """Test if all elements can be preprocessed"""

    def setUp(self):
        self.logger = logging.getLogger()
        filterwarnings("ignore",category=SyntaxWarning)
        logger.info("setUp")
        self.res = []
        
    def tearDown(self):
        logger.info("tearDown")

    def _wss_xyz_approx_1931_simple(self) -> list[TestTuple]:
        """ Get the test tuples """
        tests = [
            {"name":"1931 simple below visible", "inputs":{"args":(200,)}, "func":wss.simple_single_lobe_deg2},
            {"name":"1931 simple visible R", "inputs":{"args":(680.1,)}, "func":wss.simple_single_lobe_deg2},   
            {"name":"1931 simple visible G", "inputs":{"args":(455.6,)}, "func":wss.simple_single_lobe_deg2},   
            {"name":"1931 simple visible B", "inputs":{"args":(425.3,)}, "func":wss.simple_single_lobe_deg2},   
            {"name":"1931 simple above visible", "inputs":{"args":(2000,)}, "func":wss.simple_single_lobe_deg2},   
        ]     
        return  list(map(TestTuple.make, tests))

    def test_wss_xyz_approx_1931_simple(self):
        tests = self._wss_xyz_approx_1931_simple()
        def _subtest(name:str, inputs:TestInputs, outputs:Optional[TestOutputs]=None, func:Optional[Callable]=None):
            if func is None:
                func = nothing_burger
            args, kwargs = inputs.to_params()
            with self.subTest(name):
                outs = func(*args, **kwargs)
                # So long as not error, success
                return f"[SUCCESS] {name} {outs}"
            return(f"[FAIL] {name}")

        subtest_lambda = lambda test_tuple: _subtest(**test_tuple._asdict())
        self.res = list(map(subtest_lambda, tests))
        print(f"WSS Simple 1931 XYZ Approximation Result: {self.res}")


    def _wss_xyz_approx_1964_simple(self) -> list[TestTuple]:
        """ Get the test tuples """
        tests = [
            {"name":"1964 simple below visible", "inputs":{"args":(200,)}, "func":wss.simple_single_lobe_deg10},
            {"name":"1964 simple visible R", "inputs":{"args":(680.1,)}, "func":wss.simple_single_lobe_deg10},   
            {"name":"1964 simple visible G", "inputs":{"args":(455.6,)}, "func":wss.simple_single_lobe_deg10},   
            {"name":"1964 simple visible B", "inputs":{"args":(425.3,)}, "func":wss.simple_single_lobe_deg10},   
            {"name":"1964 simple above visible", "inputs":{"args":(2000,)}, "func":wss.simple_single_lobe_deg10},   
        ]     
        return  list(map(TestTuple.make, tests))

    def test_wss_xyz_approx_1964_simple(self):
        tests = self._wss_xyz_approx_1964_simple()
        def _subtest(name:str, inputs:TestInputs, outputs:Optional[TestOutputs]=None, func:Optional[Callable]=None):
            if func is None:
                func = nothing_burger
            args, kwargs = inputs.to_params()
            with self.subTest(name):
                outs = func(*args, **kwargs)
                # So long as not error, success
                return f"[SUCCESS] {name} {outs}"
            return(f"[FAIL] {name}")

        subtest_lambda = lambda test_tuple: _subtest(**test_tuple._asdict())
        self.res = list(map(subtest_lambda, tests))
        print(f"WSS Simple 1964 XYZ Approximation Result: {self.res}")


    def _wss_xyz_approx_1931_multi(self) -> list[TestTuple]:
        """ Get the test tuples """
        tests = [
            {"name":"1931 multi-lobe below visible", "inputs":{"args":(200,)}, "func":wss.multi_lobe_deg2},
            {"name":"1931 multi-lobe visible R", "inputs":{"args":(680.1,)}, "func":wss.multi_lobe_deg2},   
            {"name":"1931 multi-lobe visible G", "inputs":{"args":(455.6,)}, "func":wss.multi_lobe_deg2},   
            {"name":"1931 multi-lobe visible B", "inputs":{"args":(425.3,)}, "func":wss.multi_lobe_deg2},   
            {"name":"1931 multi-lobe above visible", "inputs":{"args":(2000,)}, "func":wss.multi_lobe_deg2},   
        ]     
        return  list(map(TestTuple.make, tests))

    def test_wss_xyz_approx_1931_multi(self):
        tests = self._wss_xyz_approx_1931_multi()
        def _subtest(name:str, inputs:TestInputs, outputs:Optional[TestOutputs]=None, func:Optional[Callable]=None):
            if func is None:
                func = nothing_burger
            args, kwargs = inputs.to_params()
            with self.subTest(name):
                outs = func(*args, **kwargs)
                # So long as not error, success
                return f"[SUCCESS] {name} {outs}"
            return(f"[FAIL] {name}")

        subtest_lambda = lambda test_tuple: _subtest(**test_tuple._asdict())
        self.res = list(map(subtest_lambda, tests))
        print(f"WSS Multi-lobe 1931 XYZ Approximation Result: {self.res}")

    
    def _wss_fit(self) -> list[TestTuple]:
        """ Get the test tuples """
        tests = [
            {"name":"1931 simple approx", "inputs":{"kwargs":{"lam":455, "how":"simple", "deg":"2"}}, "func":wss.WSS.fit},
            {"name":"1931 multi-lobe approx", "inputs":{"kwargs":{"lam":455, "how":"multi", "deg":"2"}}, "func":wss.WSS.fit},
            {"name":"1964 simple approx", "inputs":{"kwargs":{"lam":455, "how":"simple", "deg":"10"}}, "func":wss.WSS.fit},
        ]     
        return  list(map(TestTuple.make, tests))

    def test_wss_fit(self):
        tests = self._wss_fit()
        def _subtest(name:str, inputs:TestInputs, outputs:Optional[TestOutputs]=None, func:Optional[Callable]=None):
            if func is None:
                func = nothing_burger
            args, kwargs = inputs.to_params()
            with self.subTest(name):
                outs = func(*args, **kwargs)
                # So long as not error, success
                return f"[SUCCESS] {name} {outs}"
            return(f"[FAIL] {name}")

        subtest_lambda = lambda test_tuple: _subtest(**test_tuple._asdict())
        self.res = list(map(subtest_lambda, tests))
        print(f"WSS fit Approximation Result: {self.res}")




if __name__ == '__main__':
    ut.main()


