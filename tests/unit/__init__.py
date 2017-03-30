import inspect
import os


def data_dir_path() -> str:
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def data_file_path(filename: str) -> str:
    return os.path.join(data_dir_path(), 'data', filename)
