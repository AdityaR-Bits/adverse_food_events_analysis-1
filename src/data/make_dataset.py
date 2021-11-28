# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import pandas as pd
import re
import string
from nltk.corpus import stopwords


def brand_preprocess(row, trim_len=2):

    regex = re.compile("[%s]" % re.escape(string.punctuation))
    x = regex.sub("", row["product"])

    stop = stopwords.words("english")
    n_x = [_.upper() for _ in x.lower().split(" ") if _ not in stop]

    if len(n_x) == 0:
        return ""
    if row["category"] in [
        "Nuts/Edible Seed",
        "Vit/Min/Prot/Unconv Diet(Human/Animal)",
    ]:
        return " ".join(n_x) if len(n_x) < trim_len else " ".join(n_x[:trim_len])
    return n_x[0]

def age_preprocess(row):
    '''This function converts age reports to a single unit : year(s)
       since Data has age reported in multiple units like month(s),day(s)'''
    assert isinstance(row,pd.Series)

    age_conv = {}
    age_conv["month(s)"] = 1/12
    age_conv["year(s)"] = 1
    age_conv["day(s)"] = 1/365
    age_conv["Decade(s)"] = 10
    age_conv["week(s)"] = 1/52

    unit = row["age_units"]
    return row["patient_age"] * round(age_conv[unit],4)

@click.command()
@click.argument("input_dirpath", type=click.Path(exists=True))
@click.argument("output_dirpath", type=click.Path())
def main(
    input_dirpath="../../data/raw/", output_dirpath="../../data/processed",
):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    outPath = Path(output_dirpath)
    inPath = Path(input_dirpath)

    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")

    aggReports = None

    def strip_str(x):
        if isinstance(x, str):
            x = x.strip()
        return x

    for p in list(inPath.glob("*.csv")):

        curr_df = pd.read_csv(p, encoding="unicode_escape")

        column_map = {x: x.lower().replace(" ", "_") for x in curr_df.columns}
        curr_df = curr_df.rename(columns=column_map)
        curr_df = curr_df.rename(
            columns={"meddra_preferred_terms": "medra_preferred_terms"}
        )
        curr_df = curr_df.applymap(strip_str)

        aggReports = curr_df if aggReports is None else pd.concat([aggReports, curr_df])

    aggReports = aggReports.rename(columns={"description": "category"})
    aggReports.reset_index(drop=True, inplace=True)

    aggReports.to_csv(outPath / "clean_data.csv")

    logger.info("making outcomes exploded data set from clean data")

    # Create exploded outcome-wise cleaned data
    aggReports.outcomes = aggReports.outcomes.apply(
        lambda x: [y.strip() for y in x.split(",") if y != []]
    )

    expl_aggReports = aggReports.explode("outcomes")
    expl_aggReports = expl_aggReports[["report_id", "product", "category", "outcomes"]]
    expl_aggReports = expl_aggReports.reset_index(drop=True)

    expl_aggReports.to_csv(outPath / "exploded_out.csv")

    logger.info("making data with clean product column from processed data")
    # Create brand-enriched clean data.
    aggReports = aggReports[aggReports["product"].notna()]
    aggReports["brand"] = aggReports.apply(brand_preprocess, axis=1)
    aggReports.to_csv(outPath / "clean_brand_data.csv")

    logger.info("converting age to a common unit year(s)")
    # Create age cleaned data
    
    age_aggReports = aggReports[aggReports["patient_age"].notna()]
    age_aggReports["patient_age"] = age_aggReports.apply(age_preprocess,axis=1)
    age_aggReports.loc[:,"age_units"] = "year(s)"
    age_aggReports.to_csv(outPath / "clean_age_data.csv")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
