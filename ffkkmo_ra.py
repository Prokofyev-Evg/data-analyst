import matplotlib.pyplot as plt
import numpy as np


def get_top_df(df, qty):
    df1 = df["club"].value_counts()
    others = df1[qty:].sum()
    df1 = df1[:qty]
    df1["Остальные"] = others
    return df1


def pie_of_winners(df, season, rank, limit, title):
    get_top_df(df[(df["season"] == season) & (df["rank"] <= rank)], limit).plot.pie(
        autopct="%1.f%%",
        legend=False,
        wedgeprops={"edgecolor": "white", "linewidth": 2, "antialiased": True},
    )
    plt.title(title, fontsize=16)
    plt.xlabel("", fontsize=18)
    plt.ylabel("", fontsize=18)


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


def plot_clubs_in_season(df, season, limit):
    df[df["season"] == season].groupby(
        ["date", "firstname", "lastname"]
    ).last().groupby("club").count().sort_values(by="place", ascending=False)[
        "place"
    ].head(
        50
    ).plot(
        kind="bar", figsize=(20, 5), grid=True
    )
    plt.title(f"Распределение количества участий школ в сезоне {2425}", fontsize=32)
    plt.xlabel("Школа", fontsize=18)
    plt.ylabel("Количество участий", fontsize=18)
    plt.xticks(fontsize=20, rotation=70, horizontalalignment="right")


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
