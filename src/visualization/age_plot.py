import plotly.express as px
from collections import defaultdict
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd


def age_dist_plot(
    baseDf,
    category,
    relv_outcomes=[
        "Death",
        "Life Threatening",
        "Hospitalization",
        "Disability",
        "Patient Visited ER",
    ],
):
    """Plots a KDE plot for age distribution of reports across top outcomes for a given category

    Args:
        baseDf ([type]): [description]
        category (string): Which category of products to plot age distribution for
        relv_outcomes (list, optional):Defaults to [ "Death", "Life Threatening", "Hospitalization", "Disability", "Patient Visited ER", ].
    """
    assert isinstance(
        baseDf, pd.DataFrame
    ), "Check whether baseDf is Pandas Dataframe or not."
    assert isinstance(category, str), "Check whether category is string or not."
    assert isinstance(
        relv_outcomes, list
    ), "Check whether relv_outcomes is list or not."
    assert len(relv_outcomes) > 1, "Atleast 1 relevant outcome must be selected"

    outcome_age_dist = []

    for outcome in relv_outcomes:
        out_grp = (
            baseDf.groupby("category")
            .get_group(category)
            .groupby("outcomes")
            .get_group(outcome)
        )
        outcome_age_dist.append(out_grp["patient_age"])

    fig1 = ff.create_distplot(
        outcome_age_dist,
        relv_outcomes,
        bin_size=5,
        show_hist=False,
        histnorm="probability",
        curve_type="kde",
    )
    fig1.update_layout(
        xaxis_title="Patient Age",
        yaxis_title="Probability Density",
        font=dict(family="Courier New, monospace", size=16, color="black",),
    )
    fig1.show()
