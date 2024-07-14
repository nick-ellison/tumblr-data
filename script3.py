import pytumblr
import csv
from bs4 import BeautifulSoup

# Your Tumblr API credentials
consumer_key = 'n43JLRiz4ghIyHClHkZ0z8Vk2P6kCw0ptD0j4E8DzlPh5QOnUd'
consumer_secret = 'G5ue0l7ysHlq2Z1c9awVMEZL8riRr0zT0EI7IGFxe3zQWQeEQE'
oauth_token = '6jadkNS0z1zjqNdxtoWYWl8yIYcbV6Z0zmfVti2SBTIv7dJxtS'
oauth_secret = 'z7AmEAUU2P31ePMVqXFKloPSpwWA866cYoYeu6ktBt3gX2PIUK'

client = pytumblr.TumblrRestClient(
    consumer_key,
    consumer_secret,
    oauth_token,
    oauth_secret
)

tags = ["qsmp", "caesar", "julius caesar", "omar rudberg", "edvin ryding", "unicorn", "mlp", "lgbtq", "oliver stark", "mixed media", "critical role"]
csv_file = "tumblr_video_content_analysis.csv"

def analyze_video_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    embedded_videos_count = len(soup.find_all('iframe', src=True))
    linked_videos_count = len([link for link in soup.find_all('a', href=True) if 'youtube.com' in link['href'] or 'vimeo.com' in link['href']])
    return embedded_videos_count, linked_videos_count

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Tag', 'Post ID', 'Post Type', 'Post Date', 'Post URL', 'Content Snippet', 'Embedded Videos', 'Linked Videos'])

    for tag in tags:
        print(f"Analyzing posts for tag: #{tag}")
        try:
            response = client.tagged(tag, limit=50)
            for post in response:
                if isinstance(post, dict):  # Ensure 'post' is a dictionary
                    content = post.get('body', '') or post.get('caption', '')
                    embedded_videos, linked_videos = analyze_video_content(content)
                    writer.writerow([
                        tag, post.get('id'), post.get('type'), post.get('date'), post.get('post_url'), content[:100], embedded_videos, linked_videos
                    ])
                else:
                    print(f"Unexpected data format: {post}")
        except Exception as e:
            print(f"Error fetching or processing posts for tag #{tag}: {e}")

print(f"Analysis completed and stored in {csv_file}")
