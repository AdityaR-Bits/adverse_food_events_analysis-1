import plotly.express as px
from collections import defaultdict
import pandas as pd
import plotly.graph_objects as go

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

def symptom_counter(file_name: str, variable: int = 0):
    """This function will return a dictionary containing counts of each symptom present in data file under a given condition, 
    dictated by variable

    Args:
        file_name (str): The CSV file on which function will execute
        cosmetic (int): 0 -> all categories, all products
                        1 -> only for cosmetics as a categorie
                        2 -> only for quorn as a product

    Returns:
        (dictionary): A dictionary with keys as symptoms and values as total count
    """
    
    assert isinstance(file_name, str) and len(file_name)>0 , "file_name is either empty or not a string"
    assert isinstance(variable, int) and 0<=variable<=2, "variable is not an integer in the range [0,2]"
    dic=defaultdict(int)
    data=pd.read_csv(file_name)
    if variable==1: data=data.drop(data.index[(data['category']!='Cosmetics')])
    elif variable==2: data=data.drop(data.index[(data['brand']!='QUORN')])
    for dat in data["medra_preferred_terms"]:
        if dat== '' or pd.isnull(dat): continue
        lis=dat.split(",")
        for i in lis:
            i=i.strip()
            dic[i]+=1
    if variable==1:
        del dic["DEATH"] #Since this is probably an error made by doctors, it should be an outcome not a symptom
        del dic["INJURY"] #Since this is probably an error made by doctors, it should be an outcome not a symptom
    return dic

def top_symptoms(dic,title):
    """Find and plot top symptoms in the dictionary based on count

    Args:
        dic (dict): Dictionary containing text-count pair

    Returns:
        [dictionary]: Top 5 symptoms with their count
    """
    assert isinstance(dic,dict) and len(dic)>0, "dic is not a nonempty dictionary"
    labels = []
    sizes = []
    counts=0
    top5=sorted(dic, key=dic.get, reverse=True)[:5]
    others=sorted(dic, key=dic.get, reverse=True)[5:]
    for i in others:counts+=dic[i]
    for i in top5:
        labels.append(i)
        sizes.append(dic[i])
    labels.append("OTHER")
    sizes.append(counts)
    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=.3)])
    fig.update_layout(
        title=title,
        template=None,
        title_x=0.5,
        width=1000, 
        height=900,
        margin=dict(l=20, r=20, t=50, b=20),
        legend = dict(font = dict(size = 25, color = "black"))
        )
    fig.show()
    return top5

def top_vitamins_symptom_distribution(file_name):
    """This function will plot a histogram for Reported Cases vs Products, where Products are the top vitamin products causing the
    top 5 symptoms

    Args:
        file_name (str): Name of the file used
    """
    assert isinstance(file_name,str) and len(file_name)>0, "file_name is either empty or a non string"
    fig = go.Figure()
    symptom_list=['DIARRHOEA', 'VOMITING', 'NAUSEA', 'ABDOMINAL PAIN']
    data=pd.read_csv(file_name)
    data["category"]=data["category"].str.strip()
    grouped_desc=data.groupby("category")
    add_on_list=[]
    for symp in symptom_list:
        grouped_desc_vit=grouped_desc.get_group('Vit/Min/Prot/Unconv Diet(Human/Animal)')
        grouped_desc_vit["medra_preferred_terms"]=grouped_desc_vit["medra_preferred_terms"].str.split(",")
        grouped_desc_vit= grouped_desc_vit.explode("medra_preferred_terms").drop_duplicates()
        grouped_desc_vit["medra_preferred_terms"]=grouped_desc_vit["medra_preferred_terms"].str.strip()
        grouped_desc_vit2=grouped_desc_vit.groupby("medra_preferred_terms")
        grouped_desc_vit=grouped_desc_vit2.get_group(symp)
        list_of_counts=grouped_desc_vit["brand"].value_counts()
        list_of_counts=list_of_counts.reset_index()
        i = list_of_counts[list_of_counts["index"]== 'EXEMPTION 4'].index
        list_of_counts=list_of_counts.drop(i)
        prods=list(list_of_counts["index"])[:5]
        quants=list(list_of_counts["brand"])[:5]
        lis_symp=[symp]*5
        zipped=zip(prods,quants,lis_symp)
        for lis in zipped:
            add_on_list.append(list(lis))
        
    df=pd.DataFrame(list(add_on_list),columns=['Products','Reported Cases','Symptom'])
    fig = px.histogram(df, x="Products", y="Reported Cases", color="Symptom",title="Top Vitamin Products Causing Symptoms ")
    fig.update_layout(
        barmode="stack",
        bargap=0.1)
    fig.show()


