import plotly.express as px
import pandas as pd


def brandsVsOutcomesPlot(
    baseDf,
    category,
    title,
    relv_outcomes=[
        "Death",
        "Life Threatening",
        "Hospitalization",
        "Disability",
        "Patient Visited ER",
    ],
):
    """ This function plots histogram for the brand names for each category colored with respect to all outcomes.

    Args:
        base_df (pd.DataFrame): Base dataframe with all data.
        category (str): Category for which brands have to be plotted.
        title (str): Title of plot
        relv_outcomes (list, optional): Relevant serious outcomes which are considered. Defaults to [ "Death", "Life Threatening", "Hospitalization", "Disability", "Patient Visited ER", ].
    """

    assert isinstance(
        baseDf, pd.DataFrame
    ), "Check whether baseDf is Pandas Dataframe or not."
    assert isinstance(category, str), "Check whether category is string or not."
    assert isinstance(title, str), "Check whether title is string or not."
    assert isinstance(
        relv_outcomes, list
    ), "Check whether relv_outcomes is list or not."
    assert len(relv_outcomes) > 1, "Atleast 1 relevant outcome must be selected"

    df = baseDf[
        (baseDf["category"] == category) & (baseDf["product"] != "EXEMPTION 4")
    ].copy()
    df.dropna(inplace=True)

    topBrandsGroup = (
        df.groupby(["brand"])["report_id"].count().sort_values(ascending=False)
    )

    relv_brands = list(topBrandsGroup.reset_index()["brand"].values[:10])
    relv_df = df[df["outcomes"].isin(relv_outcomes)]
    relv_df = relv_df[relv_df["brand"].isin(relv_brands)]

    relv_df = relv_df.rename(columns={"outcomes": "Outcomes"})

    plotBarHistogram(relv_df, title=title, x="brand", color="Outcomes")

    df = df[df["outcomes"].isin(relv_outcomes)]
    g_top = df.groupby(["brand"])["report_id"].count().sort_values(ascending=False)
    top_brands_df = g_top.reset_index()[:10].rename(columns={"report_id": "#events"})

    fig_pie = px.pie(
        top_brands_df,
        values="#events",
        names="brand",
        title=title,
        height=800,
        width=1200,
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    fig_pie.show()


def plotBarHistogram(
    df, title, x="brand", color="Outcomes", barmode="stack", logscale=False
):
    """This function plots bar histogram for columnn in dataframe with color as another column.

    Args:
        df (pd.DataFrame): input pandas dataframe
        title (str): title of bar plot
        x (str, optional): x-axis column name. Defaults to "brand".
        color (str, optional): column name for color. Defaults to "Outcomes".
        barmode (str, optional): bar mode-stack or group . Defaults to "stack".
        logscale (bool, optional): whether y-axis (count) has to be log-scaled or not. Defaults to False.
    """

    assert isinstance(df, pd.DataFrame), "Check whether df is Pandas Dataframe or not."
    assert isinstance(color, str), "Check whether color is string or not."
    assert isinstance(title, str), "Check whether title is string or not."
    assert isinstance(barmode, str), "Check whether title is string or not."
    assert isinstance(logscale, bool), "Check whether logscale is bool or not."

    fig = px.histogram(
        df,
        x=x,
        color=color,
        barmode=barmode,
        title=title,
        height=800,
        width=1200,
        log_y=logscale,
    )

    fig.update_layout(uniformtext_minsize=24, uniformtext_mode="hide")
    fig.update_layout(
        legend=dict(font=dict(family="Arial", size=20, color="black")),
        legend_title=dict(font=dict(family="Arial", size=20, color="#424242")),
    )
    fig.update_layout(
        xaxis_title="Top 10 Brands",
        yaxis_title="Number  of  Adverse  Events",
        font=dict(family="Arial", size=14, color="#424242"),
    )

    fig.show()
