import praw
import praw.models.subreddits
import urllib.request
import datetime
import itertools
import os

error_folder = './lib/errors/'
dict_file = './lib/dictionary.txt'
parent_folder = 'D:/Pictures/2017/Taxes/Lecture Notes/Homework'


def download_images(url, destination):
    # TODO use "os" module to check if filepaths are okay, and possibly create filepath constants above ^^^
    # TODO add file to limit redownloading of files
    try:
        # gfycat fucks with our urls, save as .webm files
        if "gfycat" in url:
            ext = ".webm"
            url = url.replace("gfycat.com", "giant.gfycat.com")
            url = url + ext
        else:
            ext = '.' + url.split('.')[-1]
            # fix imgur .gifv links
            if ext is ".gifv":
                ext = ".mp4"
                url = url.replace(".gifv", ".mp4")
        # append the file extension to the filepath
        destination = destination + ext
        if not os.path.exists(destination):
            # save image at url to destination if file doesn't already exist
            urllib.request.urlretrieve(url, destination)
            print("Saving " + url + " to " + destination)
        else:
            print("File " + destination + " already exists, skipping.")

    except Exception as e:
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        # colons are a no no for filenames
        filestamp = '{:%Y-%m-%d}'.format(datetime.datetime.now())
        file = error_folder + "dumpfile__" + filestamp + ".txt"
        with open(file, "a", encoding='utf-8') as f:
            f.write('Executed: {0:22} URL: {1:58} Error: {2:30}\n'.format(timestamp, url, str(e)))


def get_posts(subreddit, folder_name, retrieve_limit=50):
    reddit = praw.Reddit(client_id='', client_secret='',
                         user_agent='')
    # TODO: Add optional selector for new, top, etc?
    for submission in reddit.subreddit(subreddit).hot(limit=retrieve_limit):
        path = parent_folder + "/" + folder_name + "/" + submission.title
        download_images(submission.url, path)


def pairwise(iterable):
    # s -> (s0,s1), (s1,s2), (s2, s3), ...
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def remove_header(data):
    # Remove file header
    data = data.split("**", 2)
    data = data[2:]
    data = "".join(data)
    return data


def main():
    # Read file
    with open(dict_file) as f:
        data = f.read()
    # Remove header of dictionary file
    data = remove_header(data)
    # subreddits to list
    data = data.split("\n")
    data = " -> ".join(data)
    data = data.split(" -> ")

    # we had a leading \n from our header, remove it
    data = data[1:]

    # pass each subreddit and its respective folder to get_posts function
    for sub, folder in pairwise(data):
        get_posts(subreddit=sub, folder_name=folder)


if __name__ == '__main__':
    main()
