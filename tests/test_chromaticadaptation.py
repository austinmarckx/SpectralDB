import logging
import unittest as ut
import numpy as np
from functools import partial
from spectraldb.utils.log import Log
from spectraldb.utils.io import process_element_abbreviation, load_element
from spectraldb.utils.types import TestTuple, TestInputs, TestOutputs, NamedWorkingSpace
from spectraldb.chromaticadaptation import get_adaptation, adaptation_matrix
from spectraldb.illuminant import get_illuminant

from warnings import filterwarnings
from typing import Optional, Callable

# Reference Adaptation matricies
ADAPTATION_TEST_CASES = {
    ("A", "B","xyz_scaling"): np.array([
            [0.9018844,  0.0000000,  0.0000000],
            [0.0000000,  1.0000000,  0.0000000],
            [0.0000000,  0.0000000,  2.3949136],
        ]),
    ("A", "B","bradford"): np.array([
            [0.8905163, -0.0829136,  0.2680945],
            [-0.0971524,  1.0754262, 0.0879463],
            [0.0538970, -0.0908558,  2.4838553],
        ]),
    ("A", "B","vonkries"): np.array([
            [ 0.9574884, -0.1643613,  0.2902356],
            [-0.0180539,  1.0185379,  0.0036373],
            [ 0.0000000,  0.0000000,  2.3949136],
        ]),   
    ("D65", "E","xyz_scaling"): np.array([
            [1.0521111,  0.0000000,  0.0000000],
            [0.0000000,  1.0000000,  0.0000000],
            [0.0000000,  0.0000000,  0.9184170],
        ]),
    ("D65", "E","bradford"): np.array([
            [ 1.0502616,  0.0270757, -0.0232523],
            [ 0.0390650,  0.9729502, -0.0092579],
            [-0.0024047,  0.0026446,  0.9180873],
        ]),
    ("D65", "E","vonkries"): np.array([
            [ 1.0161982,  0.0556310, -0.0197431],
            [ 0.0061107,  0.9955349, -0.0012334],
            [ 0.0000000,  0.0000000,  0.9184170],
        ]),
    ("F11", "C","xyz_scaling"): np.array([
            [0.9713952,  0.0000000,  0.0000000],
            [0.0000000,  1.0000000,  0.0000000],
            [0.0000000,  0.0000000,  1.8373271],
        ]),
    ("F11", "C","bradford"): np.array([
            [ 0.9166307, -0.0480575,  0.1606042],
            [-0.0557153,  1.0224336,  0.0525528],
            [ 0.0324715, -0.0548525,  1.8716217],
        ]),
    ("F11", "C","vonkries"): np.array([
            [ 0.9695340, -0.1108744,  0.1752191],
            [-0.0121788,  1.0107166,  0.0024542],
            [ 0.0000000,  0.0000000,  1.8373271],
        ]),
    ("D50", "D75","xyz_scaling"): np.array([
            [0.9849619,  0.0000000,  0.0000000],
            [0.0000000,  1.0000000,  0.0000000],
            [0.0000000,  0.0000000,  1.4861429],
        ]),
    ("D50", "D75","bradford"): np.array([
            [ 0.9369777, -0.0323563,  0.0952771],
            [-0.0389795,  1.0115975,  0.0314918],
            [ 0.0188243, -0.0315280,  1.5023535],
        ]),
    ("D50", "D75","vonkries"): np.array([
            [ 0.9778997, -0.0778744,  0.1026211],
            [-0.0085539,  1.0068249,  0.0017244],
            [ 0.0000000,  0.0000000,  1.4861429],
        ]),
    ("D55", "F2","xyz_scaling"): np.array([
                [ 1.0366213,  0.0000000,  0.0000000],
                [ 0.0000000,  1.0000000,  0.0000000],
                [ 0.0000000,  0.0000000,  0.7313481],
            ]),
    ("D55", "F2", "bradford"): np.array([
                [ 1.0591726,  0.0309362, -0.0569879],
                [ 0.0411624,  0.9788474, -0.0197857],
                [-0.0099371,  0.0158080,  0.7245114],
            ]),
    ("D55", "F2","vonkries"): np.array([
                [ 1.0199680,  0.0696350, -0.0582760],
                [ 0.0076489,  0.9941031, -0.0015429],
                [ 0.0000000,  0.0000000,  0.7313481],
            ]),
    ("E", "F7", "xyz_scaling"): np.array([
                [ 0.9504100,  0.0000000,  0.0000000],
                [ 0.0000000,  1.0000000,  0.0000000],
                [ 0.0000000,  0.0000000,  1.0874700],
            ]),
    ("E", "F7", "bradford"): np.array([
                [ 0.9533246, -0.0265304,  0.0236158],
                [-0.0381833,  1.0288601,  0.0093232],
                [ 0.0025528, -0.0029409,  1.0878581],
            ]),
    ("E", "F7", "vonkries"): np.array([
                [ 0.9844404, -0.0548332,  0.0208028],
                [-0.0060230,  1.0048074,  0.0012157],
                [ 0.0000000,  0.0000000,  1.0874700],
            ]),           
}

class TestChromaticAdaptation(ut.TestCase):
    """ Working space validation"""

    def setUp(self):
        filterwarnings("ignore",category=SyntaxWarning)
        Log.log("Setup", logging.DEBUG)
        self.res = []
        
    def tearDown(self):
        Log.log("Tear down", logging.DEBUG)

    def _chromatic_adaptation_conditions(self) -> list[TestTuple]:
        """ Get the test tuples """
        tests = [{"name":f"Test From {name[0]} To: {name[1]} using {name[2]}", "inputs":{"args":(name,)}} for name in ADAPTATION_TEST_CASES]               
        return  list(map(TestTuple.make, tests))

    def test_chromatic_adaptation(self):
        tests = self._chromatic_adaptation_conditions()
        
        def _subtest(name:str, inputs:TestInputs, outputs:Optional[TestOutputs]=None, func:Optional[Callable]=None):
            args, kwargs = inputs.to_params()
            source, dest, how = args[0]
            source_xyz = get_illuminant(source).to_CIE_XYZ()
            dest_xyz = get_illuminant(dest).to_CIE_XYZ()
            if func is None:
                func = partial(adaptation_matrix, src_ill=source, dest_ill=dest, adaptation=how) 
            
            with self.subTest(name):
                outs = func()
                np.testing.assert_allclose(outs, ADAPTATION_TEST_CASES[args[0]], atol=1e-5)
                np.testing.assert_allclose(dest_xyz.to_numpy(), outs @ source_xyz.to_numpy(), atol=1e-5)
                return f"[SUCCESS] {name}"
            return(f"[FAIL] {name}")

        subtest_lambda = lambda test_tuple: _subtest(**test_tuple._asdict())
        self.res = list(map(subtest_lambda, tests))
        print(f"Chromatic Adaptation Result: {self.res}")
    
    


if __name__ == '__main__':
    ut.main()


