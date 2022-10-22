import src.todos as todos
import pandas as pd
import pytest
import shutil
from datetime import datetime

# @pytest.fixture()
# def three_cards(cards_db):
#     i = cards_db.add_card(Card("foo"))
#     j = cards_db.add_card(Card("bar"))
#     k = cards_db.add_card(Card("baz"))
#     return (i, j, k)  # ids for the cards

@pytest.fixture(scope="function")
def tmp_dir(tmpdir_factory):
    my_tmpdir = tmpdir_factory.mktemp("pytestdata")
    todos.PATH_TO_DATA = my_tmpdir
    yield my_tmpdir
    shutil.rmtree(str(my_tmpdir))


@pytest.fixture(scope="session")
def df_empty():
    return pd.DataFrame(columns=["created", "task", "summary", "status", "owner"])


@pytest.fixture(scope="session")
def df_full(new_row):
    return pd.DataFrame(
        [new_row], columns=["created", "task", "summary", "status", "owner"]
    )


@pytest.fixture(scope="function")
def df_full_stored(tmp_dir, df_full):
    df_full.to_csv(f"{tmp_dir}/todos.csv")
    return df_full


@pytest.fixture(scope="function")
def df_empty_stored(tmp_dir, df_empty):
    df_empty.to_csv(f"{tmp_dir}/todos.csv")
    return df_empty


@pytest.fixture(scope="session")
def new_row():
    return {
        "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
        "task": "cocinar",
        "summary": "Cocinar algo rico",
        "status": "todo",
        "owner": "Andre",
    }


def test_get_list_path():
    """
    función para testear 
    """
    assert todos.get_list_path("todos") == todos.PATH_TO_DATA + "todos.csv"


def test_get_filename():
    assert todos.get_list_filename("data") == "data.csv"


def test_create_list(tmp_dir, df_empty):
    todos.create_list("todos")
    df1 = todos.load_list("todos")
    pd.testing.assert_frame_equal(df1, df_empty)


def test_store_list(tmp_dir, df_empty):
    todos.store_list(df_empty, "todos")
    df2 = todos.load_list("todos")
    pd.testing.assert_frame_equal(df_empty, df2)


def test_check_list_exists_fail(tmp_dir):
    assert todos.check_list_exists("todos") == False


def test_check_list_exists(df_empty_stored):
    assert todos.check_list_exists("todos") == True


def test_load_list(df_empty_stored, tmp_dir):
    df = todos.load_list("todos")
    pd.testing.assert_frame_equal(df_empty_stored, df)


def test_add_to_list(new_row, df_full, tmp_dir):
    todos.add_to_list("todos", new_row)
    df1 = todos.load_list("todos")
    pd.testing.assert_frame_equal(df1, df_full)


def test_update_list(df_full_stored):
    df_full_stored.loc[0, "owner"] = "Ivan"
    todos.update_task_in_list("todos", 0, "owner", "Ivan")
    df = todos.load_list("todos")
    pd.testing.assert_frame_equal(df, df_full_stored)
