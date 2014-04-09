import random


def command_randomnumber(bot, user, channel, args):
    "Prints a random number."
    return bot.say(channel, "5")


def command_roll(bot, user, channel, args):
    "Roll the dice!"


def command_8ball(bot, user, channel, args):
    "Ask the magic 8ball anything and he will tell you what to do."
    phrases = ["It is certain", "It is decidedly so", "Without a doubt",
                "Yes definitely", "You may rely on it", "As I see it, yes",
                "Most likely", "Outlook good", "Signs point to yes",
                "Reply hazy, try again", "Ask again later", "Cannot predict now"
                "Better not tell you now", "Concentrate and ask again",
                "Don't count on it", "My reply is no", "My sources say no",
                "Outlook not so good", "Very doubtful"]

    if "?" not in args:
        return bot.say(channel, "Need a question, {}!".format(get_nick(user)))

    bot.say(channel, "{}, {}.".format(random.choice(phrases), get_nick(user)))

def command_cointoss(bot, user, channel, args):
    "Flip a coin!"
    if random.random() > 0.5:
        bot.say(channel, "Heads!")
    else:
        bot.say(channel, "Tails!")
