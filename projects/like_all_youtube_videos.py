from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv
import time
import os
import pickle
import logging
import random
import tempfile
from pathlib import Path
logging.basicConfig(level=logging.INFO)
logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.ERROR)
from googleapiclient.errors import HttpError

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")
API_KEY = os.environ["YOUTUBE_API_KEY"]


class YouTube:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

        self.youtube_api = build("youtube", "v3", developerKey=self.api_key)
        self.youtube_auth = self.get_authenticated_service()

    def get_authenticated_service(self):
        creds = None
        token_file = BASE_DIR / "utility" / "token.pickle"

        # load saved credentials
        if os.path.exists(token_file):
            with open(token_file, "rb") as token:
                creds = pickle.load(token)

        # if not valid -> refresh or login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secret_374673107785-18mi68a9r8j3njvr00qgf14vbj58csg7.apps.googleusercontent.com.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)

            # save credentials
            with open(token_file, "wb") as token:
                pickle.dump(creds, token)

        logging.info("Authenticated YouTube API")
        return build("youtube", "v3", credentials=creds)

    def get_uploads_playlist(self, channel_id) -> str:
        res = self.youtube_api.channels().list(
            part="contentDetails",
            id=channel_id
        ).execute()

        pid = res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        logging.info(f"Upload playlist ID: {pid}")
        return pid

    def get_video_ids(self, playlist_id) -> list:
        video_ids = []
        next_page = None

        while True:
            res = self.youtube_api.playlistItems().list(
                part="contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page
            ).execute()

            for item in res["items"]:
                video_ids.append(item["contentDetails"]["videoId"])

            next_page = res.get("nextPageToken")
            if not next_page:
                break

        logging.info("Finished getting video ids")
        return video_ids

    def like(self, video_id, iteration) -> None:
        self.youtube_auth.videos().rate(
            id=video_id,
            rating="like"
        ).execute()

        logging.info(f"Liked video({str(iteration)}): {video_id}")

    def is_quota_error(self, e):
        return e.resp.status == 403 and "quotaExceeded" in str(e)


yt = YouTube(API_KEY)

channel_ids = [
    "UCkuZJIhMYCnOa0dnWeHuN2w",
    "UCMgapddJymOC6MBOiOqia1A"
]

# save already liked videos in a file to avoid repeatition
liked_file = BASE_DIR / "utility" / "liked_video.pkl"
if os.path.exists(liked_file):
    with open(liked_file, "rb") as f:
        liked = pickle.load(f)
else:
    liked = set()

try:
    quota_exceeded = False
    for channel_id in channel_ids:
        try:
            playlist = yt.get_uploads_playlist(channel_id)
        except HttpError as e:
            if yt.is_quota_error(e):
                logging.error("Quota exceeded while fetching playlist")
                quota_exceeded = True
                break
            else:
                raise

        try:
            videos = yt.get_video_ids(playlist)
        except HttpError as e:
            if yt.is_quota_error(e):
                logging.error("Quota exceeded while fetching videos")
                quota_exceeded = True
                break
            else:
                raise

        for i, vid in enumerate(videos, start=1):
            if vid in liked:
                logging.info(f"Already liked video({i}): {vid}")
                continue

            try:
                yt.like(vid, i)
                liked.add(vid)

            except HttpError as e:
                if e.resp.status == 403 and "quotaExceeded" in str(e):
                    logging.error("Quota exceeded while liking")
                    break
                else:
                    raise

            time.sleep(random.uniform(2,5))
        if quota_exceeded:
            break

except KeyboardInterrupt:
    logging.warning("Interrupted by user")
finally:
    # save the liked video id
    with tempfile.NamedTemporaryFile("wb",delete=False) as tmp:
        pickle.dump(liked, tmp)
        temp_name = tmp.name
    os.replace(temp_name, liked_file)
    logging.info(f"Progress saved. Exiting cleanly.")