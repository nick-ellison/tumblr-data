from requests_oauthlib import OAuth1Session

# Replace these with your app's consumer key and consumer secret
consumer_key = 'n43JLRiz4ghIyHClHkZ0z8Vk2P6kCw0ptD0j4E8DzlPh5QOnUd'
consumer_secret = 'G5ue0l7ysHlq2Z1c9awVMEZL8riRr0zT0EI7IGFxe3zQWQeEQE'

# Start the session
tumblr = OAuth1Session(consumer_key, client_secret=consumer_secret)

# Get a request token
request_token_url = 'https://www.tumblr.com/oauth/request_token'
fetch_response = tumblr.fetch_request_token(request_token_url)

# Get authorization URL
base_authorization_url = 'https://www.tumblr.com/oauth/authorize'
authorization_url = tumblr.authorization_url(base_authorization_url)

print('Please go here and authorize:', authorization_url)

# The user will authorize and be redirected back with a verifier
# You need to extract that verifier from the callback URL and proceed to get the access token
