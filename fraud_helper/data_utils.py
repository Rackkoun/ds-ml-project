# file: data_utils.py

import pandas as pd
import numpy as np

# setup help methods
# convert date to datetime
def convert_to_pd_datetime(dfs:list[pd.DataFrame], col_name:str) -> None:
    for df in dfs:
        df[col_name] = pd.to_datetime(df[col_name], yearfirst=True)

# define a function to agg invoice by client id
def agg_invoice(invoice_df:pd.DataFrame, agg_feats: dict, agg_cond: str ="client_id"):
    agg_df = invoice_df.groupby(agg_cond).agg(agg_feats)
    # flatten the cols
    agg_df.columns = ["_".join(col).strip() for col in agg_df.columns]
    # reset the agg index
    agg_df.reset_index(inplace=True)
    return agg_df

def agg_invoice_add_counter_type(invoice_df:pd.DataFrame, agg_df: pd.DataFrame, agg_cond: str ="client_id"):
    tmp_invoice_copy_df = invoice_df.copy()
    tmp_invoice_copy_df["has_elec"] = (tmp_invoice_copy_df["counter_type"] == "ELEC").astype(int)
    tmp_invoice_copy_df["has_gaz"] = (tmp_invoice_copy_df["counter_type"] == "GAZ").astype(int)
    # agg
    agg_by_counter_type = tmp_invoice_copy_df.groupby(agg_cond).agg({
        "has_elec": ["sum", "mean"],
        "has_gaz": ["sum", "mean"],
        "counter_type": ["nunique"] # how many different types the client has
    })
    # flatten the cols
    agg_by_counter_type.columns = ["_".join(col).strip() for col in agg_by_counter_type.columns]
    # reset the agg index
    agg_by_counter_type.reset_index(inplace=True)
    # merge with the existing agg df
    agg_df = agg_df.merge(agg_by_counter_type, on=agg_cond, how="left")
    return agg_df

# create a copy of df
def make_a_copy(df: pd.DataFrame):
    return df.copy()