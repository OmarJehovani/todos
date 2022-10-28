import os
import sys
import src.todos as todos
import pandas as pd
import pytest
import shutil
from datetime import datetime
sys.path.append( os.path.abspath(os.path.dirname(__file__)+'/../..')) 

@pytest.fixture(scope="function")
def tmp_dir(tmpdir_factory):
    my_tmpdir = tmpdir_factory.mktemp("pytestdata")
    todos.PATH_TO_DATA = my_tmpdir
    yield my_tmpdir
    shutil.rmtree(str(my_tmpdir))

def data_to_dfs():
    """
    Test to convert data to a DataFrame
    Returns:
        boolean and df name: True if the DataFrame was created according to the structure, False otherwise
    """
    return [(True, pd.DataFrame(columns=["created", "task", "summary", "status", "owner"])),
            (False, pd.DataFrame(columns=["created_time", "task_todo", "summary", "status", "owner"])),
            (False, pd.DataFrame(columns=["created", "task_todo", "summary", "status", "proprietary"])),
            (False, pd.DataFrame(columns=["time_created", "task_to", "summary_all", "status_all", "proprietary"]))
            ]

@pytest.mark.parametrize('Bool, df', data_to_dfs())
def test_create_list(tmp_dir, Bool, df):
    """_summary_

    Args:
        tmp_dir (str): temporary directory
        Bool (bool): true or false
        df (str): name of the dataframe
    """
    todos.create_list("todos")
    df1 = todos.load_list("todos")
    assert (len(pd.concat([df1, df], axis=1).columns.unique())==5)==Bool
