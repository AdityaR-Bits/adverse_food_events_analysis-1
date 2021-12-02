import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import plot
import pandas as pd
import numpy as np


def brands_vs_outcomes_plot(
        base_df,
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
    """[summary]

    Args:
        base_df ([type]): [description]
        category ([type]): [description]
        title ([type]): [description]
        relv_outcomes (list, optional): [description]. Defaults to [ "Death", "Life Threatening", "Hospitalization", "Disability", "Patient Visited ER", ].
    """

    df = base_df[
        (base_df["category"] == category) & (base_df["product"] != "EXEMPTION 4")
        ].copy()
    df.dropna(inplace=True)

    g = df.groupby(["brand"])["report_id"].count().sort_values(ascending=False)

    relv_brands = list(g.reset_index()["brand"].values[:10])
    relv_df = df[df["outcomes"].isin(relv_outcomes)]
    relv_df = relv_df[relv_df["brand"].isin(relv_brands)]

    relv_df = relv_df.rename(columns={"outcomes": "Outcomes"})

    plot_bar_histogram(relv_df, title=title, x="brand", color="Outcomes")

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


def plot_bar_histogram(
        df, title, x="brand", color="Outcomes", barmode="stack", logscale=False
):
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


def plot_time_trend(df, title, x_col="date", y_col="counts"):
    """

    Args:
        df: input dataframe
        title: title of the graph
        x_col: x-axis column name
        y_col: y-axis column name

    Returns: the plotly figure for time series plot

    """
    assert isinstance(df, pd.DataFrame)
    assert isinstance(title, str)
    assert isinstance(x_col, str)
    assert isinstance(y_col, str)
    year_month = pd.DataFrame(df['time_stamp'].groupby(df.time_stamp.dt.to_period("M")).agg('count').items(),
                              columns=["date", "counts"]).sort_values(by=["date"])
    year_month["date"] = year_month["date"].apply(lambda x: x.to_timestamp())
    fig = px.line(year_month, x=x_col, y=y_col, title=title)
    fig.show()


def plot_pie_subplots_yearly(group, title, column_name, dropping=False, d_threshold=1 / 50):
    """

    Args:
        d_threshold:
        group: input pandas groupby object
        title: title of the plot
        column_name: the column name of the data of interests
        col_num: number of columns
        row_num: number of rows
        dropping: if the data needs to group data with respect to d_threshold to "Others"
        d_threshold: dropping threshold

    Returns: a subplot of pie charts

    """
    assert isinstance(group, pd.core.groupby.generic.DataFrameGroupBy)
    assert isinstance(title, str)
    assert isinstance(column_name, str)
    assert isinstance(dropping, bool)
    assert isinstance(d_threshold, float) and 0 < d_threshold < 1

    specs = np.full((6, 3), {"type": "pie"}).tolist()
    fig = make_subplots(rows=6, cols=3, start_cell="top-left", specs=specs, vertical_spacing=0.01,
                        horizontal_spacing=0.01)
    row = 1
    col = 1
    for i in range(2004, 2021):
        year_category = pd.DataFrame(group.get_group(i)[column_name].
                                     value_counts().items(), columns=[column_name, "counts"]).sort_values(by=['counts'])
        total = year_category["counts"].sum()
        if dropping:
            year_category.loc[year_category['counts'] < total / 50, column_name] = 'Other'
        fig.add_trace(go.Pie(values=year_category["counts"], labels=year_category[column_name], textinfo='none'
                             , title="%d" % i), row=row, col=col)
        if col == 3:
            col = 1
            row += 1
        else:
            col += 1
    fig.layout.update(title=title,
                      height=1000, width=1000, hovermode='closest')
    fig.show()


def plot_scatters(group, group_names, title, fil=False, filter_list=None, plot_now=False):
    """

    Args:
        group: input pandas groupby object
        group_names: the name of groups of interest
        filter: if some groups needs to be dropped
        filter_list: the list of groups that needs to be dropped
        file_path: the path for saving images
        title: title of the graph

    Returns: a time series plot

    """
    assert isinstance(group, pd.core.groupby.generic.DataFrameGroupBy)
    assert isinstance(group_names, list) and all(isinstance(x, str) for x in group_names)
    assert isinstance(fil, bool)
    assert isinstance(filter_list, list) or filter_list is None
    assert isinstance(plot_now, bool)
    assert isinstance(title, str)
    fig = go.Figure()
    for i in range(len(group_names)):
        if fil and group_names[i] in filter_list:
            continue
        outcome = group.get_group(group_names[i])
        outcome_df = pd.DataFrame(outcome["time_stamp"].groupby(outcome.time_stamp.dt.to_period("M")).
                                  agg('count').items(), columns=["date", "counts"]).sort_values(by=["date"])
        outcome_df["date"] = outcome_df["date"].apply(lambda x: x.to_timestamp())
        fig.add_trace(go.Scatter(
            x=outcome_df["date"],
            y=outcome_df["counts"],
            mode="lines",
            name=group_names[i]
        ))
    fig.update_traces(hoverinfo='text+name', mode='lines')
    fig.update_layout(title_text=title)
    fig.update_layout(legend=dict(font=dict(family="Times", size=15, color="black")))
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Count",
        font=dict(
            family="Times",
            size=15,
            color="#7f7f7f"
        ))
    if plot_now:
        fig.show()
    else:
        return fig


def get_quorn_pie(exploded_df):
    """

    Args:
        exploded_df: the exploded_dataframe

    Returns: the pie chart for quorn

    """
    assert isinstance(exploded_df, pd.DataFrame)
    exploded_df = exploded_df.rename(columns={'product': 'products'})
    quorn = exploded_df[exploded_df.products.str.contains("QUORN") == True]
    fig = go.Figure()
    outcome_quorn = quorn.groupby("outcomes")
    count = list(outcome_quorn["outcomes"].agg("count").sort_values(ascending=False))
    outcomes = list(outcome_quorn["outcomes"].agg("count").sort_values(ascending=False).index)
    fig.add_trace(go.Pie(values=count, labels=outcomes, textinfo='none', title="outcome from QUORN"))
    fig.show()

def get_quorn_bar(exploded_df):
    """

    Args:
        exploded_df: the exploded_dataframe

    Returns:the bar chart of quorn outcomes

    """
    assert isinstance(exploded_df, pd.DataFrame)
    quorn = exploded_df[exploded_df.products.str.contains("QUORN") == True]
    k = quorn[["outcomes", "year"]]
    fig = px.histogram(
        k,
        x="year",
        color="outcomes",
        title='Outcome histogram for Quorn'
    )
    fig.show()

def plot_normalized_scatters(groups,group_names):
    """

    Args:
        df: input dataframe
        groups: groups that want to plot and normalized

    Returns:a normalized scatter over time

    """
    assert isinstance(groups, list)
    assert all(isinstance(x,pd.DataFrame) for x in groups)
    assert isinstance(group_names, list) and all(isinstance(x, str) for x in group_names)
    fig = go.Figure()
    for i in range(len(group_names)):
        cat = groups[i]
        max_num = max(cat["time_stamp"].groupby(cat.time_stamp.dt.to_period("M")).agg('count'))
        category_df = pd.DataFrame((cat["time_stamp"].groupby(cat.time_stamp.dt.to_period("M")).
                                    agg('count') / max_num).items(), columns=["date", "counts"]).sort_values(
            by=["date"])
        category_df["date"] = category_df["date"].apply(lambda x: x.to_timestamp())
        fig.add_trace(go.Scatter(x=category_df["date"], y=category_df["counts"], mode="lines", name=group_names[i]))
    fig.update_traces(hoverinfo='text+name', mode='lines')
    fig.update_layout(title_text="Normalized categories over time")
    fig.update_layout(legend=dict(font=dict(family="Times", size=15, color="black")))
    fig.update_layout(
        xaxis_title="Date",
        font=dict(
            family="Times",
            size=15,
            color="#7f7f7f"
        ))
    fig.show()

