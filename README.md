# Wallinator
Python program for Windows to download and change wallpaper after specified interval

Uses Google Custom Search API to download images that the user has specified in config.txt and then changes wallpaper.
Read config.txt for more information

Users need to create their own Google custom search API key and CS key(Custom search engine key). (Refer https://developers.google.com/custom-search) 


**Features**:
* Changes wallpapers after fixed intervals choosing from exisiting downloaded images or newly downloaded ones.
* Uses Google image search to download images corresponding to user search query.
* Allow time restriction to fetch recent results.
* Choose from different image sizes and number of images to download for a certain query.

**Dependencies**
* Python 3.5-3.8
* Google API python client: __pip install google-api-python-client__ 
  
