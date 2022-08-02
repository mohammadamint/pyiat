class InvalidInput(ValueError):
    """raises when an invalid input is passed"""


class WrongFormat(Exception):
    """raises when an input (such as pd.DataFrame) as a wrong format
    """


class MissingData(Exception):
    """raises when a piece of data is missed for the further calculations"""
