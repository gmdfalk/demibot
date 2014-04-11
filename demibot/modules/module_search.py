"""Google Search using Custom Search Engine API

    From https://github.com/EArmour
"""
import re
import os


def get_cx(site, configdir):
    "Reads Google Search ID from a file."
    cx_id = None
    try:
        authfile = os.path.join(configdir, "auth")
        with open(authfile) as f:
            authstr = f.read()
    except IOError:
        cx_id = None
    else:
        cx_id = re.search("(?<={}\s).*".format(site), authstr)
        if cx_id:
            cx_id = cx_id.group()

    return cx_id


def get_searchresult(site, bot, channel, args, nick):
    "The flesh of this module. Parse the search result and return title & link"
    cx = get_cx(site, bot.factory.configdir)

    if not cx:
        return bot.say(channel, "Could not find a CX ID.")

    url = "https://www.googleapis.com/customsearch/v1?q=%s&cx=%s&num=1&safe"\
          "=off&key=AIzaSyCaXV2IVfhG1lZ38HP7Xr9HzkGycmsuSDU"

    search = get_urlinfo(url % (args, cx))
    parsed = search.json()

    results = parsed["searchInformation"]["totalResults"]

    if results == "0":
        return

    first_url = parsed["items"][0]["link"]
    title = parsed["items"][0]["title"]

    if title or first_url:
        return bot.say(channel, "{}, {} - <{}>.".format(nick, title, first_url))
    return bot.say(channel, "{}: nothing found for {}".format(nick, args))


def command_g(bot, user, channel, args):
    "Searches Google and returns the first result. Usage: g <searchterm>"

    if not args:
        return bot.say(channel, "Usage: g <searchterm>.")

    get_searchresult("gcx", bot, channel, args, get_nick(user))


def command_yt(bot, user, channel, args):
    "Searches Youtube and returns the first result. Usage: yt <searchterm>"

    if not args:
        return bot.say(channel, "Usage: yt <searchterm>.")

    get_searchresult("ytcx", bot, channel, args)


def command_wiki(bot, user, channel, args):
    "Searches Wikipedia and returns the first result. Usage: wiki <searchterm>"

    if not args:
        return bot.say(channel, "Usage: wiki <searchterm>.")

    get_searchresult("wikicx", bot, channel, args)

