def get_top_df(df, qty):
    df1 = df["club"].value_counts()
    others = df1[qty:].sum()
    df1 = df1[:qty]
    df1["Остальные"] = others
    return df1
