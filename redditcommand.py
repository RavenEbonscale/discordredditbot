import praw
import concurrent.futures
import re


img_exts= re.compile("\/*.(jpg|jpeg|png|gif|mp4|gifv)$")


def urlsthing(submision):
    sub_url = submision.url
    isMatch = len(img_exts.findall(sub_url)) > 0
    if sub_url.startswith('https://gfycat.com/') or sub_url.startswith('https://redgifs.com/'):
        if sub_url.startswith('https://gfycat.com/'):
            reurl =sub_url.replace('https://gfycat.com/', 'https://giant.gfycat.com/')
            newurl = f'{reurl}.gif'
            print(newurl)
            return newurl
        else:
            try:
                newurl = submision.preview['reddit_video_preview']['fallback_url']
                return newurl
            except :
                    pass
    else:
        if isMatch:
            return sub_url

async def geturls(submissions):
    urls= []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for url in executor.map(urlsthing,submissions):
            urls.append(url)
    return urls