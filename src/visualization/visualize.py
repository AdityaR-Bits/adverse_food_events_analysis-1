import plotly.express as px


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
