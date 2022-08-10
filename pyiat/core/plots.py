from plotly import graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from math import ceil
from pyiat.error_log.errors import NotImplementable
from pyiat.utils.tools import generate_plot_grid

DETAILED_SCORES = {
    "Impact" : "capitals_score",
    "Capital": "dimensions_score",
    "Dimension": None
}

class Plots:
    def __init__(self, model):
        self.model = model

    def final_scores_chart(self,**kwargs):

        data = self.model.score
        fig = self._get_object("bar")(data)

        fig.show()

    def detailed_scores_chart(self,kind,**kwargs):

        if self.model.id == "Dimension":
            raise NotImplementable("detailed score chart is not implementable for Dimension object.")

        data = getattr(self.model,DETAILED_SCORES[self.model.id])

        fig = self._get_object(kind)(data)
        fig.show()

    def _get_object(self, type):

        plts = {"bar": self._bar, "radar": self._radar}

        if type.lower() not in plts:
            raise ValueError()

        return plts[type.lower()]

    def _bar(self, data: pd.DataFrame,output:str="fig",size_identifier=None):

        if isinstance(data.columns,pd.MultiIndex):
            sub_figures_id = data.columns.unique(0)

            rows,cols,iterator = generate_plot_grid(
                size = len(sub_figures_id),
                size_identifier = size_identifier if size_identifier != None else ("cols",2)
            )

            fig = make_subplots(cols=cols,rows=rows)

            for position,sub_figure_id in enumerate(sub_figures_id):
                _data = data[sub_figure_id]

                for chart in self._bar(data = _data, output="traces"):
                    fig.add_trace(
                        chart ,
                        row = iterator[position][0],
                        col = iterator[position][1]
                    )

        else:
            fig = go.Figure()
            fig.add_traces
            traces = []
            for col, vals in data.iteritems():
                traces.append(go.Bar(x=vals.index, y=vals.values, name=col))
                fig.add_trace(traces[-1])

            if output == "traces":
                return traces

        fig.update_layout(tiltle = self._titile)
        return fig


    def _radar(self, data: pd.DataFrame):

        fig = go.Figure()
        for row, vals in data.iterrows():
            r = vals.values.tolist()
            theta = vals.index.tolist()
            # closing the radar lines by adding the first point to the last data
            r.append(r[0])
            theta.append(theta[0])
            fig.add_trace(go.Scatterpolar(r=r, theta=theta, name=row))

        fig.update_layout(title = self._titile)
        return fig

    @property
    def _titile(self):

        title = f"<b>{self.model.id} : {self.model.name}</b><br>"
        if self.model.description is not None:
            title += self.model.description

        return title

