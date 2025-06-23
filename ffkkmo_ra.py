import matplotlib.pyplot as plt
import numpy as np

sorter_names = [
    ("3-й юношеский разряд, мальчики", "Произвольная программа", 5.5),
    ("3-й юношеский разряд, девочки", "Произвольная программа", 5.5),
    ("2-й юношеский разряд, мальчики", "Произвольная программа", 9.5),
    ("2-й юношеский разряд, девочки", "Произвольная программа", 9.5),
    ("1-й юношеский разряд, мальчики", "Произвольная программа", 13),
    ("1-й юношеский разряд, девочки", "Произвольная программа", 13),
    ("3-й спортивный разряд, мальчики", "Произвольная программа", 16),
    ("3-й спортивный разряд, девочки", "Произвольная программа", 16),
    ("2-й спортивный разряд, мальчики", "Короткая программа", 13),
    ("2-й спортивный разряд, мальчики", "Произвольная программа", 20),
    ("2-й спортивный разряд, девочки", "Короткая программа", 13),
    ("2-й спортивный разряд, девочки", "Произвольная программа", 20),
    ("1-й спортивный разряд, мальчики", "Короткая программа", 19),
    ("1-й спортивный разряд, мальчики", "Произвольная программа", 30),
    ("1-й спортивный разряд, девочки", "Короткая программа", 19),
    ("1-й спортивный разряд, девочки", "Произвольная программа", 30),
    ("КМС, девушки", "Короткая программа", 30),
    ("КМС, девушки", "Произвольная программа", 49),
    ("КМС, юноши", "Короткая программа", 32),
    ("КМС, юноши", "Произвольная программа", 50),
    ("МС, девушки", "Короткая программа", 35),
    ("МС, девушки", "Произвольная программа", 53),
    ("МС, юноши", "Короткая программа", 38),
    ("МС, юноши", "Произвольная программа", 63),
]


def get_top_df(df, qty):
    df1 = df["club"].value_counts()
    others = df1[qty:].sum()
    df1 = df1[:qty]
    df1["Остальные"] = others
    return df1


def pie_of_winners(df, season, rank, limit, title):
    fig = (
        get_top_df(df[(df["season"] == season) & (df["rank"] <= rank)], limit)
        .plot.pie(
            autopct="%1.f%%",
            legend=False,
            wedgeprops={"edgecolor": "white", "linewidth": 2, "antialiased": True},
        )
        .get_figure()
    )
    plt.title(title, fontsize=16)
    plt.xlabel("", fontsize=18)
    plt.ylabel("", fontsize=18)
    return fig


def participants_for_club_in_season(
    df, season, club, limit, plot=True, sort_col="date", ascending=False
):
    data = (
        df[(df["season"] == season) & (df["club"] == club)]
        .groupby(["firstname", "lastname"])
        .count()
        .sort_values(by=sort_col, ascending=ascending)
        .head(limit)["date"]
    )
    if plot:
        ax = data.plot(kind="bar", figsize=(20, 5), grid=True)
        major_ticks = np.arange(0, max(data) + 1, 1)
        ax.set_yticks(major_ticks)
        plt.title(club, fontsize=32)
        plt.xlabel("Спортсмен", fontsize=16)
        plt.ylabel(f"Количество участий в сезоне {season}", fontsize=18)
        plt.xticks(fontsize=20, rotation=50, horizontalalignment="right")
    else:
        return data


def participants_for_club_in_year(
    df, year, club, limit, plot=True, sort_col="date", ascending=False
):
    data = (
        df[(df["year"] == year) & (df["club"] == club)]
        .groupby(["firstname", "lastname"])
        .count()
        .sort_values(by=sort_col, ascending=ascending)
        .head(limit)["date"]
    )
    if plot:
        ax = data.plot(kind="bar", figsize=(20, 5), grid=True)
        major_ticks = np.arange(0, max(data) + 1, 1)
        ax.set_yticks(major_ticks)
        plt.title(club, fontsize=32)
        plt.xlabel("Спортсмен", fontsize=16)
        plt.ylabel(f"Количество участий в {year} году", fontsize=18)
        plt.xticks(fontsize=20, rotation=50, horizontalalignment="right")
    else:
        return data


def plot_clubs_in_season(df, season, limit=50, club=None):
    df_clubs = (
        df[df["season"] == season]
        .groupby(["date", "firstname", "lastname"])
        .last()
        .groupby("club")
        .count()
        .sort_values(by="place", ascending=False)
        .reset_index()
        .head(limit)
    )
    ax = df_clubs.plot(x="club", y="place", kind="bar", figsize=(20, 5), grid=True)
    plt.title(f"Распределение количества участий школ в сезоне {2425}", fontsize=32)
    plt.xlabel("Школа", fontsize=18)
    plt.ylabel("Количество участий", fontsize=18)
    plt.xticks(fontsize=20, rotation=70, horizontalalignment="right")
    if club:
        idx = df_clubs[df_clubs["club"] == club].index
        for x in idx:
            ax.patches[x].set_facecolor("red")


def plot_clubs_in_year(df, year, limit):
    df[df["year"] == year].groupby(["date", "firstname", "lastname"]).last().groupby(
        "club"
    ).count().sort_values(by="place", ascending=False)["place"].head(limit).plot(
        kind="bar", figsize=(20, 5), grid=True
    )
    plt.title(f"Распределение количества участий школ в {year} году", fontsize=32)
    plt.xlabel("Школа", fontsize=18)
    plt.ylabel("Количество участий", fontsize=18)
    plt.xticks(fontsize=20, rotation=70, horizontalalignment="right")


def sportsmen_rating_in_season(
    df, season, category, firstname, lastname, middlename=None, limit=50
):
    if not middlename:
        df_tss = (
            df[(df["season"] == season) & (df["category"] == category)]
            .groupby(["date", "firstname", "lastname", "club"])
            .sum()
            .sort_values("tss", ascending=False)
            .reset_index()
        )
        idx = df_tss[
            (df_tss["firstname"] == firstname) & (df_tss["lastname"] == lastname)
        ].index
    else:
        df_tss = (
            df[(df["season"] == season) & (df["category"] == category)]
            .groupby(["date", "firstname", "middlename", "lastname"])
            .sum()
            .sort_values("tss", ascending=False)
            .reset_index()
        )
        idx = df_tss[
            (df_tss["firstname"] == firstname)
            & (df_tss["middlename"] == middlename)
            & (df_tss["lastname"] == lastname)
        ].index
    # Plotting
    df_tss["label"] = df_tss[["firstname", "lastname", "date"]].agg(" ".join, axis=1)
    ax = df_tss[:limit].plot(x="label", y="tss", kind="bar", figsize=(15, 5), grid=True)

    # Setting title and labels
    plt.title(f"{firstname} {lastname} в сезоне {season}", fontsize=32)
    plt.xlabel("Спортсмен", fontsize=18)
    plt.ylabel("Результат", fontsize=18)
    plt.xticks(fontsize=8, rotation=70, horizontalalignment="right")

    # Highlight sportsmen
    for x in idx:
        if len(ax.patches) > x:
            ax.patches[x].set_facecolor("red")

    display(df_tss.iloc[idx])


def club_rating_in_season(df, season, category, club, limit=50, ascending=False):
    df_tss = (
        df[(df["season"] == season) & (df["category"] == category)]
        .groupby(["date", "firstname", "lastname", "club"])
        .sum()
        .sort_values("tss", ascending=ascending)
        .reset_index()
    )
    idx = df_tss[df_tss["club"] == club].index
    # Plotting
    df_tss["label"] = df_tss[["firstname", "lastname", "date"]].agg(" ".join, axis=1)
    ax = df_tss[:limit].plot(x="label", y="tss", kind="bar", figsize=(15, 5), grid=True)
    # Setting title and labels
    plt.title(f"{club} в сезоне {season}", fontsize=32)
    plt.xlabel("Спортсмен", fontsize=18)
    plt.ylabel("Результат", fontsize=18)
    plt.xticks(fontsize=8, rotation=70, horizontalalignment="right")
    # Highlight club
    for x in idx:
        if len(ax.patches) > x:
            ax.patches[x].set_facecolor("red")

    display(df_tss.iloc[idx])


def get_df_of_club_in_year(df, club, year):
    return df[(df["year"] == year) & (df["club"] == club)].reset_index(drop=True)


def get_df_of_club_in_season(df, club, season):
    return df[(df["season"] == season) & (df["club"] == club)].reset_index(drop=True)


def participants_of_club_in_season(df, club, season):
    data = (
        get_df_of_club_in_season(df, club, season)
        .groupby(["date", "firstname", "lastname"])
        .last()
        .reset_index()
        .groupby(["firstname", "lastname"])
        .count()
        .sort_values(by=["date", "lastname"], ascending=False)["club"]
    )
    ax = data.plot(kind="bar", figsize=(20, 10), grid=True)
    major_ticks = np.arange(0, max(data) + 1, 1)
    ax.set_yticks(major_ticks)
    plt.title(f"Количество участий спортсменов в сезоне {season}", fontsize=32)
    plt.xlabel("Спортсмен", fontsize=16)
    plt.ylabel(f"", fontsize=18)
    plt.xticks(fontsize=10, rotation=50, horizontalalignment="right")
