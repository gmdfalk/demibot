import random
import re
import time

from twisted.internet import reactor


def read_quizfile(quizfile):
    "Reads the quiz file into a big dictionary."
    try:
        with open(quizfile) as f:
            linelist = f.readlines()
    except IOError:
        quizdictlist = None
    else:
        questionlist = []
        # Splits the line into category:question*answers match groups.
        rgx = re.compile("(?:([^:]*):)?([^*]*)\*(.*)")
        for line in linelist:
            match = rgx.search(line)
            question = match.group(1), match.group(2), match.group(3)
            questionlist.append(question)

    return questionlist

def command_quiz(bot, user, channel, args):
    "A very basic quiz bot. No hints, no points. Usage: quiz [on|off|<delay>]."
    # TODO:
    delay = 25

    if args == "on":
        bot.factory.quiz_enabled = True
        bot.say(channel, "Quiz is now enabled. Delay: {}.".format(delay))
    elif args == "off":
        bot.factory.quiz_enabled = False
        return bot.say(channel, "Quiz is now disabled.")
    elif args == "clue":
        bot.say(channel, "There currently are no clues. Sorry.")
    elif args == "help":
        bot.say(channel, "Usage: quiz [on|off|<delay>].")
    elif args.isdigit() and not args > 60:
        delay = int(args)
        bot.say(channel, "Delay changed to: {}.".format(delay))
    else:
        bot.say(channel, "Quiz running: {}. Delay: {}"
                .format(bot.factory.quiz_enabled, delay))

    quizlist = None
    if bot.factory.quiz_enabled:
        quizlist = read_quizfile("modules/quiz_general.txt")

    while bot.factory.quiz_enabled and quizlist:
        category, question, answers = random.choice(quizlist)
        question = question.strip().capitalize()  # Format the question poco.
        if category:
            bot.say(channel, "{}: {}?".format(category, question))
        else:
            bot.say(channel, "{}?".format(question))

        reactor.callLater(delay, bot.say, channel, answers)
        time.sleep(delay + 5)
