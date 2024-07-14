import pytumblr
import csv
from bs4 import BeautifulSoup

# Replace these with your own credentials
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

# Function to analyze the content for embedded vs linked videos
def analyze_video_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    embedded_videos = soup.find_all('iframe', src=True)
    linked_videos = 0
    video_platforms = ['youtube.com', 'vimeo.com']

    for link in soup.find_all('a', href=True):
        if any(platform in link['href'] for platform in video_platforms):
            linked_videos += 1

    return len(embedded_videos), linked_videos

# Amend the CSV file writing as per your original structure
with open("tumblr_video_content_analysis.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Tag', 'Post ID', 'Post Type', 'Post Date', 'Post URL', 'Embedded Videos', 'Linked Videos'])

    for tag in tags:
        print(f"\nAnalyzing posts for tag: #{tag}")
        response = client.tagged(tag, limit=50)

        for post in response:
            content = post.get('body', '') or post.get('caption', '')
            embedded_videos, linked_videos = analyze_video_content(content)
            
            # Your CSV writing logic here
            writer.writerow([tag, post.get('id'), post.get('type'), post.get('date'), post.get('post_url'), embedded_videos, linked_videos])

        # Console output or further analysis as needed
