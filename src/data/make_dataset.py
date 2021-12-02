# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from numpy import NaN
import pandas as pd
import re
import string
from nltk.corpus import stopwords


def brand_preprocess(row, trim_len=2):
    """ This function creates a brand name column by parsing out the product column of data. It trims the words based on trim length param to choose appropriate brand name.

    Args:
        row ([pd.Series]): Dataframe row
        trim_len (int, optional): Length by which product name has to be trimmed. Defaults to 2.

    Returns:
        [str]: brand name corresponding to a product.
    """
    # Remove punctuations from product name
    regexPunctuation = re.compile("[%s]" % re.escape(string.punctuation))
    cleanProduct = regexPunctuation.sub("", row["product"])

    nameList = [
        _.upper()
        for _ in cleanProduct.lower().split(" ")
        if _ not in stopwords.words("english")
    ]

    if len(nameList) == 0:
        return ""

    # for certain categories use trim length to select brand name.
    if row["category"] in [
        "Nuts/Edible Seed",
        "Vit/Min/Prot/Unconv Diet(Human/Animal)",
    ]:
        return (
            " ".join(nameList)
            if len(nameList) < trim_len
            else " ".join(nameList[:trim_len])
        )
    return nameList[0]


def age_preprocess(row):
    """This function converts age reports to a single unit : year(s)
    since Data has age reported in multiple units like month(s),day(s)

    Args:
        row ([pd.Series]): A row of the entire Dataframe

    Returns:
        [float]: value of patient_age converted to years unit 
    """

    assert isinstance(row, pd.Series)

    age_conv = {
        "month(s)": 1 / 12,
        "year(s)": 1,
        "day(s)": 1 / 365,
        "Decade(s)": 10,
        "week(s)": 1 / 52,
    }

    unit = row["age_units"]
    if unit == NaN:
        return -1
    else:
        return row["patient_age"] * round(age_conv[unit], 4)


def strip_str(x):
    if isinstance(x, str):
        x = x.strip()
    return x


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
    logger.info("Creating clean unified data from raw files")

    aggReports = None

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
    aggReports["caers_created_date"] = pd.to_datetime(aggReports.caers_created_date)
    aggReports.reset_index(drop=True, inplace=True)
    aggReports.to_csv(outPath / "clean_data.csv")

    logger.info("Processing and enriching data")

    # Create brand-enriched column.
    logger.info("Making brand name column from clean data")
    aggReports = aggReports[aggReports["product"].notna()]
    aggReports["brand"] = aggReports.apply(brand_preprocess, axis=1)

    # Pre-processing Age column.
    logger.info("converting age to a common unit year(s)")
    aggReports["patient_age"] = aggReports.apply(age_preprocess, axis=1)
    aggReports = aggReports.drop(columns=["age_units"])

    aggReports.to_csv(outPath / "processed_data.csv")

    # Create exploded outcome-wise cleaned data.
    logger.info("making outcomes exploded data set from clean brand-name data")
    aggReports.outcomes = aggReports.outcomes.apply(
        lambda x: [y.strip() for y in x.split(",") if y != []]
    )
    expl_aggReports = aggReports.explode("outcomes")
    expl_aggReports = expl_aggReports.reset_index(drop=True)
    expl_aggReports.to_csv(outPath / "exploded_data.csv")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
