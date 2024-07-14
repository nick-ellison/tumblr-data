import pytumblr
import csv
from bs4 import BeautifulSoup

# Your Tumblr API credentials
consumer_key = 'n43JLRiz4ghIyHClHkZ0z8Vk2P6kCw0ptD0j4E8DzlPh5QOnUd'
consumer_secret = 'G5ue0l7ysHlq2Z1c9awVMEZL8riRr0zT0EI7IGFxe3zQWQeEQE'
oauth_token = 'dlVxZrq8rAHJjkTRd6bupKCn0vu7qPPRWLGdUkqnCUpNpfpekJ'
oauth_secret = '0pnhY4EJYJB18dCI5RxByQftg5G9ciGz5eRlQc5qTthgZgWIju'

client = pytumblr.TumblrRestClient(
    consumer_key,
    consumer_secret,
    oauth_token,
    oauth_secret
)

# tags = ["qsmp", "caesar", "julius caesar", "omar rudberg", "edvin ryding", "unicorn", "mlp", "lgbtq", "oliver stark", "mixed media", "critical role"]
# tags = ["nude", "nsfw", "topless", "onlyfans", "nudes", "mature"]
tags = ["video", "videos", "tiktok", "tiktoks", "funny", "lol", "meme", "comedy", "haha", "animation", "anime"]
details_csv_file = "tumblr_posts_details.csv"
summary_csv_file = "tumblr_summary_analysis.csv"

def analyze_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    embedded_videos = len(soup.find_all('iframe', src=lambda x: 'youtube.com' in x or 'vimeo.com' in x))
    linked_videos = len([link for link in soup.find_all('a', href=True) if 'youtube.com' in link['href'] or 'vimeo.com' in link['href']])
    gifs = len(soup.find_all('img', src=lambda x: x.endswith('.gif')))
    return embedded_videos, linked_videos, gifs

# Process and write detailed post data
with open(details_csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Tag', 'Post ID', 'Post Type', 'Post Date', 'Post URL', 'Embedded Videos', 'Linked Videos', 'GIFs'])

    for tag in tags:
        response = client.tagged(tag, limit=50)  # Adjust limit as needed
        for post in response:
            if isinstance(post, dict):
                content = post.get('body', '') or post.get('caption', '')
                embedded_videos, linked_videos, gifs = analyze_content(content)
                writer.writerow([tag, post['id'], post['type'], post['date'], post['post_url'], embedded_videos, linked_videos, gifs])

# Collect summary data
summary_data = []

for tag in tags:
    response = client.tagged(tag, limit=50)
    total_posts = len(response)
    video_posts = sum(1 for post in response if post.get('type') == 'video')
    embedded_videos = linked_videos = gifs = 0
    
    for post in response:
        if isinstance(post, dict):
            content = post.get('body', '') or post.get('caption', '')
            ev, lv, g = analyze_content(content)
            embedded_videos += ev
            linked_videos += lv
            gifs += g
            
    summary_data.append([tag, total_posts, video_posts, embedded_videos, linked_videos, gifs])

# Write summary data to a separate CSV file
with open(summary_csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Tag', 'Total Posts', 'Video Posts', 'Embedded Videos', 'Linked Videos', 'GIFs'])
    writer.writerows(summary_data)

print(f"Details of posts written to {details_csv_file}")
print(f"Summary analysis written to {summary_csv_file}")
