from pyiat.utils.constants import INDICATORS, EFFECT, POSITIVE, NEGATIVE
from pyiat.error_log.errors import InvalidInput, WrongFormat, MissingData
from pyiat.utils.constants import Constant
from pyiat.utils.tools import get_combination, geometric_mean,evaluation_guide
from pyiat.core.plots import Plots
import pandas as pd
import numpy as np
import copy
from typing import Dict, List, Union

OBJ_MAP = {"Impact": "capitals", "Capital": "dimensions", "Dimension": "indicators"}


class PairWised:
    """ The parent class for pairwised objects including:
        Dimension
        Capital
        Impact
    """

    def __init__(self, name, items, description=None):
        self.name = name
        self.description = description
        self.plots = Plots(self)
        self.set_items(items)

    def __len__(self):
        return len(self.pairwised_items)

    @property
    def id(self):
        """the id of pairwised object

        Returns
        -------
        str
            id of pairwised object equal to the name of object
        """
        if isinstance(self, Impact):
            return "Impact"
        elif isinstance(self, Dimension):
            return "Dimension"
        elif isinstance(self, Capital):
            return "Capital"

    @property
    def pairwised_items(self):
        """returns the pairwised info for each object

        Returns
        -------
        list
            list of pairwised items. For exmample Impact.pairwised_items returns a list of capitals
        """
        pairwised = OBJ_MAP[self.id]

        return getattr(self, pairwised)

    def get_weight_matrix(self):
        """returns the pd.Series for weight assignment

        Returns
        -------
        pd.Series
            A multiindex pd.Series for weight assignemnt of pariwised items
        """
        combination = get_combination(self.pairwised_items)

        return pd.Series(
            index=pd.MultiIndex.from_tuples(
                combination, names=["Reference Impact", "Compared Impact"]
            ),
            dtype=float,
        )

    def set_weight_matrix(self, matrix):
        """sets the weight matrix

        Parameters
        ----------
        matrix : pd.Series
            defines the weights of pairwised items

        Raises
        ------
        InvalidInput
            if nan exists in matrix
        WrongFormat
            if the index level/s of matrix is not correct
        """
        if matrix.hasnans:
            raise InvalidInput("nan values are not acceptable.")

        df = pd.DataFrame(
            data=np.eye(len(self)),
            index=self.pairwised_items,
            columns=self.pairwised_items,
        )

        # print(df)
        # if not df.index.equals(matrix.index):
        #     raise WrongFormat(
        #         f"matrix does not have the correct format. please use the get_weight_matrix function to get the correct format. Object -> {self}"
        #     )
        for raw, val in matrix.items():
            df.loc[raw[0], raw[1]] = val
            df.loc[raw[1], raw[0]] = 1 / val

        self.weight_matrix = df

    def calc_weight(self):
        """Calculates the normalized weights based on the given weight matrix

        Returns
        -------
        pd.Series
            the normilzed weights

        Raises
        ------
        MissingData
            if the weights are not still assigned.
        """
        if not hasattr(self, "weight_matrix"):
            raise MissingData(
                f"weights are not assigned for object '{self}'. set_weight_matrix function can be used for assinging the matrix."
            )

        geo_mean = geometric_mean(self.weight_matrix)

        return geo_mean / sum(geo_mean)

    def __repr__(self) -> str:
        return self.id + ":" + self.name

    def set_items(self, items, overwrite=False):
        """sets the pairwised items and their data

        Parameters
        ----------
        items : dict
            a dict of pairwised data:
                {name_of_item : object_of_item}

        overwrite : bool, optional
            if True, will overwrite the exisiting items, by default False

        Raises
        ------
        InvalidInput
            if the type of pairwised object does not match
        """
        if self.id == "Impact":
            _type = Capital
        elif self.id == "Capital":
            _type = Dimension
        elif self.id == "Dimension":
            _type = Indicator

        _name = OBJ_MAP[self.id]
        _pairwised = "_" + _name

        if any([not isinstance(item, _type) for item in items]):
            raise InvalidInput(f"only {_name.title()} object is acceptable.")

        for item in items:

            if item.name in self.pairwised_items and not overwrite:
                print(
                    f"{item.name} already exists and is not assigned. to assign duplicate items, use 'overwrite=True'."
                )
            else:
                getattr(self, _pairwised)[item.name] = item

    def __iter__(self):
        pairwised = "_" + OBJ_MAP[self.id]
        self.__it__ = copy.deepcopy(getattr(self, pairwised))
        self.__pairwised__ = pairwised
        return self

    def __next__(self):
        """generating an iterator over the scenarios"""
        if len(self.__it__):
            key = [*self.__it__][0]
            value = getattr(self,self.__pairwised__)[key]

            self.__it__.pop(key)

            return (key, value)

        else:
            raise StopIteration

    def copy(self):
        return copy.deepcopy(self)

class Indicator:
    """an object for buidling indicators
    """

    def __init__(self, name, type, unit, ex_ante, ex_post, description=None):
        """_summary_

        Parameters
        ----------
        name : str
            the name of indicator
        type : str
            "positive" or "negative"
        unit : str
            the unit of measure
        ex_ante : int
            the ex_ante situation rate from 0 to 5
        ex_post : int
            the ex_post situation rate from 0 to 5
        description : str, optional
            the description of the indicator, by default None
        """

        self.name = name
        self.type = type
        self.ex_ante = ex_ante
        self.ex_post = ex_post
        self.unit = unit
        self.description = description

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, var):
        if var not in INDICATORS.type:
            raise InvalidInput(f"Valid inputs for type are {INDICATORS.type}")
        self._type = var

    @property
    def ex_ante(self):
        return self._ex_ante

    @ex_ante.setter
    def ex_ante(self, var):
        if var not in INDICATORS.ex_ante:
            raise InvalidInput(f"Valid inputs for ex_ante are {INDICATORS.ex_ante}")
        self._ex_ante = var

    @property
    def ex_post(self):
        return self._ex_post

    @ex_post.setter
    def ex_post(self, var):
        if var not in INDICATORS.ex_post:
            raise InvalidInput(f"Valid inputs for ex_post are {INDICATORS.ex_post}")
        self._ex_post = var

    @property
    def effect(self):
        """translates the quantitative rates to qualitative rates

        Returns
        -------
        str
            conversion of quantitative changes into qualitative measures
        """
        difference = self.ex_post - self.ex_ante

        return EFFECT[self.type][difference]

    @property
    def normalized(self):
        """returns normalized data

        Returns
        -------
        Constant
            includes normalized ex_ante, ex_post and difference
        """
        _sum = self.ex_ante + self.ex_post

        if self.type == POSITIVE:
            ex_ante = self.ex_ante / _sum
            ex_post = self.ex_post / _sum

        else:
            ex_ante = self.ex_post / _sum
            ex_post = self.ex_ante / _sum

        return Constant(ex_ante=ex_ante, ex_post=ex_post, difference=ex_post - ex_ante)

    def __repr__(self) -> str:
        return "Indicator" + ":" + self.name

    def copy(self):
        return copy.deepcopy(self)

class Dimension(PairWised):
    """the main class for Dimensions
    """

    def __init__(
        self, name, indicators, description=None,
    ):
        """creates a dimension

        Parameters
        ----------
        name : str
            dimension name
        indicators : list
            list of indicator objects
        description : _type_, optional
            a description of dimension, by default None
        """
        self._indicators = {}
        super().__init__(name, indicators, description)

    def set_indicator(self, indicators, overwrite=False):
        """sets new indicators

        Parameters
        ----------
        indicators : list[Indicator]
            list of indicators
        overwrite : bool, optional
            if True will overwrite duplicate indicators, by default False
        """
        self.set_items(indicators, overwrite)

    @property
    def indicators(self):
        return [*self._indicators]

    @property
    def score(self):
        """calcuates and returns the final score of dimension

        Returns
        -------
        pd.DataFrame
            final score of dimension for all the indicators of the dimension
        """
        output = pd.DataFrame()
        for name, indicator in self:
            vals = indicator.normalized
            output.loc["ex_ante", name] = vals.ex_ante
            output.loc["ex_post", name] = vals.ex_post

        return output


class Capital(PairWised):
    """ creating a Capital
    """

    def __init__(self, name: str, dimensions: List[Dimension], description: str = None):
        """creates a Capital object

        Parameters
        ----------
        name : str
            the name of capital
        dimensions : list
            list of dimensions
        description : str, optional
            a description of the capital, by default None
        """
        self._dimensions = {}
        super().__init__(name, dimensions, description)

    @property
    def dimensions(self):
        return [*self._dimensions]

    def set_dimension(self, dimensions: List[Dimension], overwrite: bool = False):
        """sets the dimensions for the capital

        Parameters
        ----------
        dimensions : List[Dimenison]
            a list of dimensions to be assigned
        overwrite : bool, optional
            _description_, by default False
        """
        self.set_items(dimensions, overwrite)

    @property
    def score(self) -> pd.DataFrame:
        """returns the score of capital

        Returns
        -------
        pd.DataFrame
            the total score of the capital
        """
        output = pd.DataFrame(index=["ex_ante", "ex_post"], columns=[*self._dimensions])

        for name, dimension in self:
            score = dimension.score
            weight = dimension.calc_weight()
            output.loc[["ex_ante", "ex_post"], name] = score @ weight

        capital = output.sum(1).to_frame()
        capital.columns = [self.name]

        return capital

    @property
    def dimensions_score(self) -> pd.DataFrame:
        """returns the concated score of capital dimensions

        Returns
        -------
        pd.DataFrame
            the score of dimensions
        """
        return pd.concat({name: dimension.score for name, dimension in self}, axis=1)


class Impact(PairWised):
    """an Impact object"""

    def __init__(
        self, name: str, capitals: List[Capital], description: str = None,
    ):
        """creates an Impact

        Parameters
        ----------
        name : str
            Impact name
        capitals : List[Capital]
            list of capitals
        description : str, optional
            a description of the impact, by default None
        """
        self._capitals = {}
        super().__init__(name, capitals, description)

    @property
    def capitals(self):
        return [*self._capitals]

    def set_capital(self, capitals: List[Capital], overwrite: bool = False):
        """sets the capitals

        Parameters
        ----------
        capitals : List[Capital]
            a list of capitals
        overwrite : bool, optional
            if True, will overwrite the duplicate capitals, by default False
        """
        self.set_items(capitals, overwrite)

    @property
    def score(self) -> pd.DataFrame:
        """returns the impact score

        Returns
        -------
        pd.DataFrame
            the total score of the imapct
        """
        capital_scores = pd.concat([capital.score for _, capital in self], axis=1,)
        weights = self.calc_weight()
        _score = (capital_scores @ weights).to_frame()
        _score.columns = ["Impact"]
        return _score

    @property
    def summary(self) -> pd.DataFrame:
        """returns a summary of the whole project

        Returns
        -------
        pd.DataFrame
            a summary table of the prject
        """
        headers = [
            "Capital",
            "Dimension",
            "Indicator",
            "Type",
            "Ex_ante",
            "Ex_post",
            "Effect",
            "Normalized Ex_ante",
            "Normalized Ex_post",
            "Difference",
        ]
        vals = []
        for capital, capital_obj in self():
            for dimension, dimension_obj in capital_obj:
                for indicator, indicator_obj in dimension_obj:
                    normalized = indicator_obj.normalized
                    vals.append(
                        [
                            capital,
                            dimension,
                            indicator,
                            indicator_obj.type,
                            indicator_obj.ex_ante,
                            indicator_obj.ex_post,
                            indicator_obj.effect,
                            normalized.ex_ante,
                            normalized.ex_post,
                            normalized.difference,
                        ]
                    )

        df = pd.DataFrame(vals, columns=headers)
        return df.set_index(headers[0:3])


    @property
    def capitals_score(self) -> pd.DataFrame:
        """returns the concated capital scores of the project

        Returns
        -------
        pd.DataFrame
            concated capital scores
        """
        return pd.concat([capital.score for name, capital in self], axis=1)



    def weight_matrices_to_excel(self,path:Union[str,None]) -> Union[None,Dict]:
        """writes all the weight matrices into a series of excel files

        Parameters
        ----------
        path : Union[str,None]
            str of the file directory, if None, will return a dict similar to the structure of the files

        Returns
        -------
        Union[None,Dict]
            if str is passed to path, will save the excel files otherwise returns a dict
        """

        files = {
            "Impact":{},
            "Capital" : {},
            "Dimension": {},
        }


        files["Impact"]["impacts"] = self.get_weight_matrix()

        for capital_name,capital in self:
            files["Capital"][capital_name] = capital.get_weight_matrix()

            for dimension_name,dimension in capital:
                files["Dimension"][dimension_name] = dimension.get_weight_matrix()

        if path == None:
            return files

        for item,vals in files.items():
            guide = evaluation_guide(item)
            with pd.ExcelWriter(f'{path}/{item}.xlsx') as file:
                guide.to_excel(file,"Evaluation Guide")
                for sheet,df in vals.items():
                    df.to_excel(file,sheet)


    def parse_weight_matrices(self,io:Union[str,Dict]) -> None:
        """parses weight matrices from an excel file or a dictionary

        Parameters
        ----------
        io : Union[str,Dict]
            file path as a string or the files dictionary

        Raises
        ------
        InvalidInput
            if nans exists in the dataframes/excel sheets.
        """
        sample = self.weight_matrices_to_excel(path=None)

        if io == None:
            files = io

        else:
            files = sample.copy()

            for item,vals in files.items():
                for sheet,df in vals.items():
                    data = pd.read_excel(
                        f"{io}/{item}.xlsx",
                        sheet_name=sheet,
                        index_col=[0,1]
                        )

                    if data.isnull().any().sum():
                        raise InvalidInput(f"NaN values are not acceptable for weights. File -> '{io}/{item}.xlsx', sheet -> {sheet}.")

                    files[item][sheet] = data.iloc[:,0]

        self.set_weight_matrix(files["Impact"]["impacts"])

        for capital_name,capital in self:
            capital.set_weight_matrix(files["Capital"][capital_name])
            for dimension_name,dimension in capital:
                dimension.set_weight_matrix(files["Dimension"][dimension_name])




