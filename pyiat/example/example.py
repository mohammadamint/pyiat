
import os
from pyiat.utils.io import excel_parser

path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
    )
)
def load_example():

    project = excel_parser(
        filepath= f"{path}/Project.xlsx",
        impact_name = "Utopia"
    )

    project.impact.parse_weight_matrices("files")

    return project
