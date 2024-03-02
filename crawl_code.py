import os
from TikTokApi import TikTokApi
import asyncio

# Define your ms_token, user_id and number of videos
ms_token = 'prkWCPUsYTgHWpM0kkx4lrcY0jVFwTreFuTKRn2M4vJNQW_iaADHQb16B4Y_AQKn_5pLmtSDjQn9NkM1_v2F7rIF0kYyQa1WByFeh0B-7EPDoAq3149SdE320xLA4-HK8B9SQxHUQHvCjNaCNw=='
user_id = 'lazadavietnam'
number_videos = 35


async def get_user_data(user_id):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)
        user = api.user(user_id)
        user_data = await user.info()
        # print(user_data)
        header_labels = "Create_time,Create_year,Create_month,Create_day,Create_hour,Likes,Comments,Saves,Views,Shares,Duration(sec),Video Height,Video Width\n"
        # Get the directory path of the Python file crawl_code
        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_directory, "tiktok_lzd_data.csv")  # Combine file name
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(header_labels)
            async for video in user.videos(count=number_videos):
                create_time = str(video.create_time)
                video_data = {
                    "Create_time": video.create_time,
                    "Create_year": create_time[0:4],
                    "Create_month": create_time[5:7],
                    "Create_day": create_time[8:10],
                    "Create_hour": create_time[11:13],
                    "Likes": video.stats["diggCount"],
                    "Comments": video.stats["commentCount"],
                    "Saves": video.stats["collectCount"],
                    "Views": video.stats["playCount"],
                    "Shares": video.stats["shareCount"],
                    "Duration(sec)": video.as_dict["video"]["duration"],
                    "Video Height": video.as_dict["video"]["height"],
                    "Video Width": video.as_dict["video"]["width"],
                }
                line = ",".join(str(video_data[key]) for key in header_labels.strip().split(","))
                file.write(line + "\n")
            print("Video data written to file.")

if __name__ == "__main__":
    asyncio.run(get_user_data(user_id))
