import os

def setup_notebook(lvl:int=1):
    """ Basically let notebooks access the module directory by changing the dir to `input` levels above current"""
    _this_path = os.path.dirname(__file__)
    target_path = os.path.sep.join(_this_path.split(os.path.sep)[:-lvl])
    if os.getcwd() != target_path:
        os.chdir(target_path)
    