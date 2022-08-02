from dash import Dash, dcc, Output, Input, html
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX])

title = dcc.Markdown(children="# Impact Evaluation App")
name_output = dcc.Markdown(children=" ", id="n_out")
name_input = dbc.Input(value="John Doe", id="n_in")


def build_banner():
    return html.Div(
        style={"display": "inline"},
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text", children=[html.H1("Impact Evaluation Dashboard"),],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Img(
                        src=app.get_asset_url("logo.svg"),
                        style={"width": "10%", "height": "10%"},
                    )
                ],
            ),
        ],
    )


def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="Project Definition",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Weighting",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab1",
                        label="Results",
                        value="tab3",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )


def build_tab_1():
    return


app.layout = html.Div(
    id="main_app_container",
    style={"margin-left": "2px"},
    children=[
        build_banner(),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
    ],
)


# #dbc.Container([title,name_input,name_output])

# @app.callback(
#     Output(component_id="n_out",component_property="children"),
#     Input(component_id="n_in",component_property="value")
# )
# def update_title(user_input):
#     return user_input

if __name__ == "__main__":
    app.run_server(port=8051)
