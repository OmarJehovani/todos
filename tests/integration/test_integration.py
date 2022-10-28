import os
import sys
#import src.todos as todos
import pandas as pd
import pytest
import shutil
from src import todos 
from datetime import datetime
sys.path.append( os.path.abspath(os.path.dirname(__file__)+'/../..')) 

@pytest.fixture(scope="function")
def tmp_dir(tmpdir_factory):
    my_tmpdir = tmpdir_factory.mktemp("pytestdata")
    todos.PATH_TO_DATA = my_tmpdir
    yield my_tmpdir
    shutil.rmtree(str(my_tmpdir))

@pytest.fixture(scope="function")
def new_row():
    return {
        "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
        "task": "leer",
        "summary": "pytest",
        "status": "todo",
        "owner": "Omar",
    }

@pytest.fixture(scope="function")
def df_full(new_row):
    return pd.DataFrame([new_row], columns=["created", "task", "summary", "status", "owner"])

dict1 = {
     "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
        "task": "leer",
        "summary": "pytest",
        "status": "todo",
        "owner": "Omar",
}

dict2 = {
     "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
        "task": "leer",
        "summary": "unit tests",
        "status": "todo",
        "owner": "Omar",
}

def data_integration_test():
    return [
        (True, dict1, "list1", pd.DataFrame(columns=["created", "task", "summary", "status", "owner"])),
        (False, dict1, "list2", pd.DataFrame(columns=["created", "task", "summary", "status", "owner"]))
    ]

pytest.mark.parametrize('Bool, new_reg, name_ls, df', data_integration_test())
def test_add_to_list(Bool,new_reg, name_ls, df, df_full, tmp_dir):
    todos.create_list(name_ls)
    df_v1 = todos.load_list(name_ls)
    todos.create_list(name_ls)
    df_v2 = todos.load_list(name_ls)

    assert ((len(pd.concat([df_v1, df], axis=1).columns.unique())==5) and 
            (pd.concat([df_full, df_v2], axis=0).drop_duplicates().shape[0]==1)) == Bool

