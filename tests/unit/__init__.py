import inspect
import os


def data_file_path(filename: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), 'data', filename)
