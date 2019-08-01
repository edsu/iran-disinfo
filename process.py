#!/usr/bin/env python3

import csv
import sys
import json

from glob import glob

# get the seed user ids and screen_names
# note: we use user id instead of screen_names wherever possible
# since user ids are immutable, and screen_names can be changed.

user_ids = set()
for line in open('seeds.jsonl'):
    user = json.loads(line)
    user_ids.add(user['id_str'])

# create a csv file to write matching tweets to

cols = ["tweetid","userid","user_display_name","user_screen_name","user_reported_location","user_profile_description","user_profile_url","follower_count","following_count","account_creation_date","account_language","tweet_language","tweet_text","tweet_time","tweet_client_name","in_reply_to_userid","in_reply_to_tweetid","quoted_tweet_tweetid","is_retweet","retweet_userid","retweet_tweetid","latitude","longitude","quote_count","reply_count","like_count","retweet_count","hashtags","urls","user_mentions","poll_choices"]
output = csv.DictWriter(open('results/tweets.csv', 'w'), fieldnames=cols)
output.writeheader()

# go through each of the tweets csv files and write any matches to our output file

matches = count = 0
for csv_file in glob('data/*tweets*.csv'):
    with open(csv_file) as fh:
        for tweet in csv.DictReader(fh):
            count += 1
            match = False

            # check these columns to see if our seed user_id is there
            for prop in ['userid', 'in_reply_to_userid', 'retweet_userid']:
                if tweet[prop] in user_ids:
                    match = True

            # unpack user_mentions which is a string like ["1234","5689"]
            user_mentions = set(tweet['user_mentions'].strip('"[] ').split(','))
            if user_mentions & user_ids :
                match = True

            if match:
                matches += 1
                output.writerow(tweet)
                sys.stdout.write('.')
                sys.stdout.flush()

print('\n{}/{} matches!'.format(matches, count))
