import json
import os
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import typer
from googleapiclient.discovery import build

if TYPE_CHECKING:
    from googleapiclient._apis.youtube.v3.resources import YouTubeResource


YT_URL = "https://www.googleapis.com/youtube/v3/videos"
WATCH_HISTORY_FILE_PATH = "./watch-history.json"


def main(
    youtube_api_key: str, watch_history_file_path: str = WATCH_HISTORY_FILE_PATH
) -> None:
    """Given a YT v3 API key and a watch history JSON filepath, creates analysis graphs under outputs folder

    Args:
        youtube_api_key (str): YouTube api key from https://console.cloud.google.com/apis/dashboard
        watch_history_file_path (str, optional): Path to watch history downloaded from Google Takeout as JSON. Defaults to ./watch-history.json.
    """
    print("Analysis Started!")
    print("Connecting to YouTube.")
    service: YouTubeResource = build("youtube", "v3", developerKey=youtube_api_key)
    videos_collection = service.videos()
    video_categories_collection = service.videoCategories()

    if not os.path.exists("./outputs"):
        os.mkdir("./outputs")

    print("Loading watch history.")
    with open(WATCH_HISTORY_FILE_PATH, encoding="utf-8") as watch_history_file:
        watch_history = json.load(watch_history_file)

    watched_urls = {}
    for watched in watch_history:
        url = watched.get("titleUrl", None)
        title = watched.get("title", None)[8:]
        if url:
            watched_urls[title] = url

    unique_watched_urls = list(set(watched_urls.values()))
    unique_watched_ids = [url[32:] for url in unique_watched_urls]

    print("Getting video information from YouTube.")
    watched_video_snippets = []
    for i in range(0, len(unique_watched_ids), 50):
        video_collection_request = videos_collection.list(
            part="snippet", id=unique_watched_ids[i : i + 50]  # noqa: E203
        )
        snippets_response = video_collection_request.execute()
        snippets = [item["snippet"] for item in snippets_response["items"]]
        watched_video_snippets += snippets

    unique_category_ids = list(
        {snippet["categoryId"] for snippet in watched_video_snippets}
    )
    video_categories_request = video_categories_collection.list(
        part="snippet", id=unique_category_ids
    )
    video_categories_response = video_categories_request.execute()
    video_category_id_to_title = {
        item["id"]: item["snippet"]["title"]
        for item in video_categories_response["items"]
    }
    print("Saving video snippets and watch history information to outputs folder.")
    df_snippets = pd.DataFrame(watched_video_snippets)
    df_watch_history = pd.DataFrame(watch_history)
    df_watch_history.to_csv("outputs/watch_history.csv")
    df_snippets.to_csv("outputs/snippets.csv")
    df_watch_history.title = df_watch_history.title.apply(lambda title: title[8:])  # type: ignore
    df_merged = df_watch_history.merge(df_snippets, on="title", how="left")
    df_merged["categoryTitle"] = df_merged["categoryId"].apply(
        lambda id: video_category_id_to_title.get(id, "NaN")
    )
    df_merged.drop(
        [
            "subtitles",
            "products",
            "activityControls",
            "header",
            "thumbnails",
            "liveBroadcastContent",
        ],
        axis=1,
    )
    df_merged.to_csv("outputs/full_history.csv")
    df_merged["time"] = pd.to_datetime(df_merged["time"])  # type: ignore
    df_merged["dayWatched"] = pd.to_datetime(  # type: ignore
        df_merged["time"].apply(lambda time: str(time)[:10])
    )
    df_merged.set_index("title")
    df_category_to_day = df_merged.filter(items=["dayWatched", "categoryTitle"])
    ctdf = (
        df_category_to_day.reset_index()
        .groupby(["dayWatched", "categoryTitle"], as_index=False)
        .count()
        # rename isn't strictly necessary here, it's just for readability
        .rename(columns={"index": "count"})
    )
    pivotted = ctdf.pivot_table("count", "dayWatched", "categoryTitle")  # type: ignore
    df_pivotted_by_month = pivotted.resample("M").sum()
    percentages = df_pivotted_by_month.div(df_pivotted_by_month.sum(axis=1), axis=0)

    print("Drawing a few example graphs to output folder.")
    plt.style.use("dark_background")  # type: ignore
    vals = np.linspace(0, 1, 22)
    np.random.shuffle(vals)
    cmap = plt.cm.colors.ListedColormap(plt.cm.gnuplot(vals))  # type: ignore
    ax = percentages.plot.area(fontsize=12, figsize=(20, 10), cmap=cmap)
    ax.set_xlabel("Date")
    ax.set_ylabel("Percentage of Video Watched")
    ax.set_title("My YouTube Interest by Month")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles[::-1],
        labels[::-1],
        fontsize=11,
        loc="upper left",
        bbox_to_anchor=(1.0, 1.0),
    )
    ax.get_figure().savefig(os.path.join("outputs", "percentages_per_month.png"))

    ax = df_pivotted_by_month.plot.area(fontsize=13, figsize=(20, 10))
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of videos watched")
    ax.set_title("My YouTube Interest by Month")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], fontsize=11, loc="upper left")
    ax.get_figure().savefig(os.path.join("outputs", "numbers_per_month.png"))
    service.close()

    print(
        "Done! Go check out your analysis in the outputs folder!"
        "You can also run some on your own using the csv files."
        "Thanks for using youtube-history-analysis"
    )


if __name__ == "__main__":
    typer.run(main)
