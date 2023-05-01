import os
import time
import shutil
import random

from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from ConstText import searchTags, captions, generateTags
from instagrapi.types import Media, DirectThread, DirectMessage, DirectMedia
from pathlib import Path

# TODO get memes in more ways then hashtag
# TODO story posts
# TODO post from DM's
# TODO post from Thug Shaker Central

CREDS_PATH = Path("CREDENTIALS.txt")
with open(CREDS_PATH, 'r') as f:
    USERNAME, PASSWORD = f.read().split()

cl = Client()
SESSION_PATH = Path("session.json")

# LOGIN
login_via_session = False
login_via_creds = False

if os.path.getsize(SESSION_PATH) == 0:
    print("Creating new session")
    cl.login(USERNAME, PASSWORD)
    time.sleep(1)
    cl.dump_settings(SESSION_PATH)
    cl.get_timeline_feed()
    print("Logged in via credentials")
    login_via_creds = True

else:
    print("There is a session")
    try:
        session = cl.load_settings(SESSION_PATH)
        cl.set_settings(session)
        cl.login(USERNAME, PASSWORD)

        try:  # Check if session is valid
            cl.get_timeline_feed()
            time.sleep(2)
            print("Logged in via session")
            cl.dump_settings(SESSION_PATH)
            login_via_session = True

        except LoginRequired:
            print("Session is invalid, need to login via username and password")
            old_session = cl.get_settings()

            # use the same device uuids across logins
            # maybe this is problem
            cl.set_settings({})
            cl.set_uuids(old_session["uuids"])

    except Exception as e:
        print("Couldn't login using session information: %s" % e)

if not login_via_session and not login_via_creds:
    try:
        print("Attempting to login via username and password. username: %s" % USERNAME)
        if cl.login(USERNAME, PASSWORD):
            print("Logged in via credentials")
            cl.dump_settings(SESSION_PATH)
            login_via_creds = True
    except Exception as e:
        print("Couldn't login user using username and password: %s" % e)

if not login_via_creds and not login_via_session:
    raise Exception("Couldn't login user with either password or session")

# USER IDS
my_user_id = cl.user_id_from_username(USERNAME)
adelka_user_id = cl.user_id_from_username("adel.trn")
lostBoyKalv2_user_id = cl.user_id_from_username("lostboykal.v2")
foxNews_user_id = cl.user_id_from_username("foxnews")
myThreadID = "340282366841710301244259328861883103950"

# FILES & FOLDERS
UsedMemesPath = Path("UsedMemes.txt")
MediaDownloadsPath = Path("Media Downloads")


def main():
    # TODO possible while loop with gaps to run indefinitely

    #uploadMediaToAcc(findMediaViaHashtag("emogirls", "recent"))
    #getMediaFromDMs()
    print("test")

# ----------------------------------------------------------------------------------------------------------------------


def findMediaViaHashtag(customTag="", mode="top") -> Media or None:
    if customTag:
        searchTag = customTag.replace("#", "")
    else:
        searchTag = random.choice(searchTags).replace("#", "")

    print("Searching with hashtag: " + searchTag)

    assert mode.lower() in ["top", "recent"], "Choose top or recent"
    if mode.lower() == "top":
        media = cl.hashtag_medias_top(searchTag, amount=1)[0]
        if checkIfUsedMeme(media.pk):
            return
        print("Found media type " + str(media.media_type))
        return media

    if mode.lower() == "recent":
        media = cl.hashtag_medias_recent(searchTag, amount=1)[0]
        if checkIfUsedMeme(media.pk):
            return
        print("Found media type " + str(media.media_type))
        return media


def uploadMediaToAcc(media: Media or None):
    # TODO support reels with music
    # TODO maybe having vids in album causes error
    cleanUp()

    if media is None:
        print("Can't upload None")
        return

    toUseHashtags = generateTags()
    toUseCaption = random.choice(captions)
    readyHashtags = " ".join(toUseHashtags)
    GAP = "\n" + " " + "\n" + " " + "\n" + " " + "\n" + " " + "\n" + " " + "\n"
    CAPTION = toUseCaption + GAP + "ignore tags :3\n" + readyHashtags
    PK = media.pk

    # MEDIA TYPE CHECK & PROCESSING
    if media.media_type == 1:
        # photo
        cl.photo_download(int(PK), MediaDownloadsPath)
        print("Downloaded photo")
        time.sleep(3)
        fileName = os.listdir("Media Downloads")
        pathToMedia = Path("Media Downloads/" + str(fileName[0]))
        cl.photo_upload(pathToMedia, CAPTION)
        print("Uploaded photo")
        time.sleep(1)
        cleanUp()
        print("Cleaned up")

    elif media.media_type == 2 and media.product_type == "feed":
        # video
        cl.video_download(int(PK), MediaDownloadsPath)
        print("Downloaded video")
        time.sleep(3)
        fileName = os.listdir("Media Downloads")
        pathToMedia = Path("Media Downloads/" + str(fileName[0]))
        cl.video_upload(pathToMedia, CAPTION)
        print("Uploaded video")
        time.sleep(1)
        cleanUp()
        print("Cleaned up")


    elif media.media_type == 2 and media.product_type == "clips":
        # clip
        cl.clip_download(int(PK), MediaDownloadsPath)
        print("Downloaded clip")
        time.sleep(3)
        fileName = os.listdir("Media Downloads")
        pathToMedia = Path("Media Downloads/" + str(fileName[0]))
        cl.clip_upload(pathToMedia, CAPTION)
        print("Uploaded clip")
        time.sleep(1)
        cleanUp()
        print("Cleaned up")


    elif media.media_type == 8:
        # album
        cl.album_download(int(PK), MediaDownloadsPath)
        print("Downloaded album")
        time.sleep(3)
        fileNames = os.listdir("Media Downloads")
        listOfPaths = []

        for file in fileNames:
            pathToMedia = Path("Media Downloads/" + str(file))
            listOfPaths.append(pathToMedia)

        cl.album_upload(listOfPaths, CAPTION)
        print("Uploaded album")
        time.sleep(1)
        cleanUp()
        print("Cleaned up")





def getMediaFromDMs(allowedUsers="") -> Media or None:
    #TODO user id or username for allowedUsers

    threads = cl.direct_threads()
    myThread = cl.direct_thread(340282366841710301244259328861883103950)
    print(myThread.messages)


    # for dThread in threads:
    #     if dThread.thread_title == "David Erwin":
    #         print(dThread)
    #     if dThread.thread_title == "Thug Shaker Central 🤝":
    #         pass

    # cleanUp()
    #
    # toUseHashtags = generateTags()
    # toUseCaption = random.choice(captions)
    # readyHashtags = " ".join(toUseHashtags)
    # GAP = "\n" + " " + "\n" + " " + "\n" + " " + "\n" + " " + "\n" + " " + "\n"
    # CAPTION = toUseCaption + GAP + "ignore tags :3\n" + readyHashtags
    #
    # PK = "IDK"
    # cl.photo_download(int(PK), MediaDownloadsPath)
    # print("Downloaded photo")
    # time.sleep(3)
    # fileName = os.listdir("Media Downloads")
    # pathToMedia = Path("Media Downloads/" + str(fileName[0]))
    # cl.photo_upload(pathToMedia, CAPTION)
    # print("Uploaded photo")
    # time.sleep(1)
    # cleanUp()
    # print("Cleaned up")



def getMediaFromGroupChats(chatName="") -> Media or None:
    pass






def checkIfUsedMeme(PK) -> bool:
    usedMemesFile = open(UsedMemesPath, "r+")
    if PK in [string.strip() for string in usedMemesFile.readlines()]:
        print("Already used this meme")
        usedMemesFile.close()
        return True
    else:
        usedMemesFile.write(PK + "\n")
        print("Added meme to used memes list")
        usedMemesFile.close()
        return False


def updateUsedMemesWithAllPKs():
    file = open(UsedMemesPath, 'w')
    file.write('')
    listOfMyMedias = cl.user_medias(int(my_user_id))

    for media in listOfMyMedias:
        file.write(media.pk + "\n")

    file.close()


def cleanUp():
    folder_path = "Media Downloads"
    shutil.rmtree(folder_path)
    os.makedirs(folder_path)


if "__main__" == __name__:
    main()
