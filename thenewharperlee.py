#!/usr/bin/env python
# encoding: utf-8
"""
Harper Lee's next book is called...

Idea: https://twitter.com/emckean/status/619522225318707200
https://wordnik.com/lists/go-funk-a-megatron
"""
from __future__ import print_function
import argparse
import random
import inflect  # pip install inflect
import pronouncing  # pip install pronouncing
import sys
import twitter
import webbrowser
import yaml
from wordnik import swagger, WordsApi

import book_cover


def load_yaml(filename):
    """
    File should contain:
    consumer_key: TODO_ENTER_YOURS
    consumer_secret: TODO_ENTER_YOURS
    access_token: TODO_ENTER_YOURS
    access_token_secret: TODO_ENTER_YOURS
    wordnik_api_key: TODO_ENTER_YOURS
    """
    f = open(filename)
    data = yaml.safe_load(f)
    f.close()
    if not data.viewkeys() >= {
            'access_token', 'access_token_secret',
            'consumer_key', 'consumer_secret'}:
        sys.exit("Twitter credentials missing from YAML: " + filename)
    if not data.viewkeys() >= {
            'wordnik_api_key'}:
        sys.exit("Wordnik credentials missing from YAML: " + filename)
    return data


def tweet_it(string, credentials, image=None):
    """ Tweet string and image using credentials """
    if len(string) <= 0:
        return

    # Create and authorise an app with (read and) write access at:
    # https://dev.twitter.com/apps/new
    # Store credentials in YAML file
    t = twitter.Twitter(auth=twitter.OAuth(
        credentials['access_token'],
        credentials['access_token_secret'],
        credentials['consumer_key'],
        credentials['consumer_secret']))

    print("TWEETING THIS:\n", string)

    if args.test:
        print("(Test mode, not actually tweeting)")
    else:

        if image:
            print("Upload image")

            # Send images along with your tweets.
            # First just read images from the web or from files the regular way
            with open(image, "rb") as imagefile:
                imagedata = imagefile.read()
            # TODO dedupe auth=OAuth(...)
            t_up = twitter.Twitter(domain='upload.twitter.com',
                                   auth=twitter.OAuth(
                                       credentials['access_token'],
                                       credentials['access_token_secret'],
                                       credentials['consumer_key'],
                                       credentials['consumer_secret']))
            id_img = t_up.media.upload(media=imagedata)["media_id_string"]
        else:
            id_img = None  # Does t.statuses.update work with this?

        result = t.statuses.update(
            status=string, media_ids=id_img)

        url = "http://twitter.com/" + \
            result['user']['screen_name'] + "/status/" + result['id_str']
        print("Tweeted:\n" + url)
        if not args.no_web:
            webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


def get_random_words_from_wordnik(part_of_speech):
    """ Get a random word from Wordnik """
    words = words_api.getRandomWords(includePartOfSpeech=part_of_speech,
                                     limit=100)

    random_words = []
    for word in words:
        random_words.append(word.word)
#     print("Random " + part_of_speech + ": " + word)
    return random_words


def get_random_word(part_of_speech, syllables=None, skip_plurals=False):
    """
    Get this kind of word with this many syllables.
    If none found with this many syllables, any'll do.
    """
    words = get_random_words_from_wordnik(part_of_speech)
    for word in words:
        pronunciation_list = pronouncing.phones_for_word(word)
        for pronunciation in pronunciation_list:
            count = pronouncing.syllable_count(pronunciation)

            print(count, word)
            if skip_plurals and word[-1].lower() == "s" and word[-2] != "s":
                # Might be plural, just skip it
                print("Plural? Skip!")
                continue

            if count == syllables:
                # Bingo!
                return word

    # Any'll do
    return random.choice(words)


def a(word):
    """ Return the word with the correct article prepended """
    pronunciation_list = pronouncing.phones_for_word(word)
    try:
        if pronunciation_list[0][0] in "AEIOU":
            return "an " + word
        else:
            return "a " + word
    except IndexError:
        if word[0].lower() in "aeiou":
            return "an " + word
        else:
            return "a " + word


def thenewharperlee():
    """ New book title """
    print("Get words from Wordnik...")
    first = random.choice(["To", "Go"])
    verb = get_random_word("verb-transitive", 1)
    if first == "To":
        noun_syllables = 3
    else:
        noun_syllables = 2
    noun = get_random_word("noun", noun_syllables, skip_plurals=True)

    title = "{0} {1} {2}".format(first, verb.title(), p.a(noun.title()))

    intro = random.choice([
        "Announcing Harper Lee's new novel: {0}",
        "Discovered in Harper Lee's safety-deposit box: {0}",
        "Harper Lee's anticipated novel {0} hits bookshelves",
        "Will you read Harper Lee's new novel {0}?",
        "Harper Lee’s '{0}' Expected to Set Records",
        "The reviews are in for Harper Lee's {0}",
        "Harper Lee’s '{0}' Will Realign the Literary Universe",
        "Why is Harper Lee releasing '{0}' now?",
        "Harper Lee: The anticipated '{0}'",
        "Attention, Harper Lee Fans: '{0}' Is Coming Sooner Than You Thought",
        "Harper Lee's '{0}' Surprises In 1st Chapter",
        "Mixed feelings on Harper Lee's '{0}'",
        "'{0}': What does Harper Lee's book title mean?",
        "Harper Lee's '{0}' Being Published Against Her Will?",
        "Harper Lee's Lawyer Responds to '{0}' Speculation",
        "{0}, and five other sequels that should never happen",
        "Harper Lee's '{0}' Is Already a Best-Seller",
        "The Suspicious Story Behind Harper Lee's {0}",
        "Harper Lee to release another novel, '{0}'",
        "{0} by Harper Lee",
        "Who has read Harper Lee's {0}?",
        "Review: The Surprisingly Current Lessons of '{0}'",
        "Author Harper Lee Announces the Release of '{0}'",
        "Don't let '{0}' change the way you think about Atticus Finch",
        "LEE RETURNS: Literary world readies for '{0}' debut",
        "First chapter of '{0}' will be online",
        "Review: Some will rejoice, others resent Harper Lee's '{0}'",
        "Why I Refuse to Read '{0}'",
        "Investigation Surrounding Harper Lee’s ‘{0}’ Progresses",
        "People are going cray for '{0}'",
        "Readers ready to judge '{0}' for themselves",
        "Harper Lee's {0} draws hype and controversy",
        "Does Harper Lee Really Want {0} to be Published?",
        "Harper Lee’s ‘{0}’ Brings Division and Curiosity to Monroeville, "
        "Ala.",
        "Forget the controversies – '{0}' is worth reading",
        "Is {0} Disingenuous?",
        "While Some Are Shocked by ‘{0},’ "
        "Others Find Nuance in a Bigoted Atticus Finch",
        "{0}: mystery of Harper Lee manuscript discovery deepens",
        "{0} review – more complex than Harper Lee's original classic, "
        "but less compelling",
        "{0}'s first chapter, first review: a beguiling journey into the past",
        "Why I'm excited about Harper Lee's new book {0}",
        "Harper Lee's new novel {0} is a bolt from the blue",
        ])

    output = intro.format(title)

    print()
    print(output)
    print()
    return output, title


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Harper Lee's next book is called...",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-o', '--outfile', default="C:/stufftodelete/book_cover.png",
        help="Book cover image filename")
    parser.add_argument(
        '-y', '--yaml',
        # default='/Users/hugo/Dropbox/bin/data/thenewharperlee.yaml',
        default='M:/bin/data/thenewharperlee.yaml',
        help="YAML file location containing Twitter keys and secrets")
    parser.add_argument(
        '-nw', '--no-web', action='store_true',
        help="Don't open a web browser to show the tweeted tweet")
    parser.add_argument(
        '-x', '--test', action='store_true',
        help="Test mode: go through the motions but don't tweet anything")
    args = parser.parse_args()

    credentials = load_yaml(args.yaml)
    wordnik_client = swagger.ApiClient(credentials['wordnik_api_key'],
                                       'http://api.wordnik.com/v4')
    words_api = WordsApi.WordsApi(wordnik_client)

    p = inflect.engine()

    tweet, title = thenewharperlee()

    book_cover.book_cover(title, "Harper Lee", args.outfile)

    tweet_it(tweet, credentials, args.outfile)

# End of file
