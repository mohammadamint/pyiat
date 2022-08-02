from plotly import graph_objects as go
import pandas as pd


class Plots:
    def __init__(self, model):
        self.model = model

    def final_scores_chart(self, type="bar", **kwargs):

        data = self.model.score
        fig = self._get_object(type)(data)

        fig.show()

    def detailed_scores_chart(self):
        data = self.model.dimensions_score
        fig = self._get_object("bar")(data)
        fig.show()

    def _get_object(self, type):

        plts = {"bar": self._bar, "radar": self._radar}

        if type.lower() not in plts:
            raise ValueError()

        return plts[type.lower()]

    def _bar(self, data: pd.DataFrame):

        fig = go.Figure()

        for col, vals in data.iteritems():
            fig.add_trace(go.Bar(x=vals.index, y=vals.values, name=col))

        return fig

    def _radar(self, data: pd.DataFrame):
        fig = go.Figure()

        for row, vals in data.iterrows():
            fig.add_trace(go.Scatterpolar(r=vals.values, theta=vals.index, name=row))

        return fig
