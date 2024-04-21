import os
from TikTokApi import TikTokApi
import asyncio
import time

# Define your ms_token, user_id and number of videos
ms_token = 'prkWCPUsYTgHWpM0kkx4lrcY0jVFwTreFuTKRn2M4vJNQW_iaADHQb16B4Y_AQKn_5pLmtSDjQn9NkM1_v2F7rIF0kYyQa1WByFeh0B-7EPDoAq3149SdE320xLA4-HK8B9SQxHUQHvCjNaCNw=='
user_id = 'lazadavietnam'

async def get_user_videos(username):
    start_time = time.time()  # Record the start time
    row_count = 0

    async with TikTokApi() as api:
        await api.create_sessions(headless=False, ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        user = api.user(username)
        user_data = await user.info()
        post_count = user_data["userInfo"]["stats"].get("videoCount")

        with open(f"user_videos_{username}.csv" , "w", encoding='utf-8') as f:
            header_labels = "Create_time,Create_year,Create_month,Create_day,Create_hour,Likes,Comments,Saves,Views,Shares,Duration(sec),Video Height,Video Width\n"
            f.write(header_labels)

            async for video in user.videos(count=post_count):
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
                row = f'{video_data["Create_time"]},"{video_data["Create_year"]}","{video_data["Create_month"]}","{video_data["Create_day"]}","{video_data["Create_hour"]}","{video_data["Likes"]}","{video_data["Comments"]}",{video_data["Saves"]},{video_data["Views"]},{video_data["Shares"]},{video_data["Duration(sec)"]},{video_data["Video Height"]},{video_data["Video Width"]}\n'
                f.write(row)
                print(video)
                row_count += 1

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds")
    print(f"Total rows: {row_count}")
    print(f"Rows per second: {row_count / elapsed_time}")

if __name__ == "__main__":
    asyncio.run(get_user_videos(user_id))
