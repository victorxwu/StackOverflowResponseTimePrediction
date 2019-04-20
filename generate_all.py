# generate.py
# Take filtered post data in json format and generate a set of features for
# each question consisting of the rsr, asr, pr, and finally the answer time
# for that post. Output all of these as a CSV file with one row per question.

# answer time = creation date of answer - creation date of question
# rsr = (users with avg response time below 2hr for that tag) / (total users)
# asr = (users with at least 10 answers for that tag) / (total users)
# pr = (number of tag occurances) / (total tag occurances)
# latf = stored the the sum of the time difference between all the questions' post date and their last activity time into each of the available tags. Then 
#        calculated the LATF feature for each question by adding all the time differences stored for each tag based on tags used in the question.
# vcf = finding the total view count of a tag across all the questions, then adding the views of tags together for each question based on the tags used in the question
# acf = finding the total answer count of a tag across all the questions, then adding the answer counts of tags together for each question based on the tags used in the question. 
# tcf = finding the total tag count across all the questions for all the tags by extracting information from Tags.XML through Stack Overflow data dump, 
#       then adding the tag counts together for each question based on the tags used in the question.
# H.E. Added a fix to remove extra blank lines  

import sys
import csv
import json
import numpy as np
from datetime import datetime

class RSRs:

    cache = {}

    def __init__(self, posts, tags):
        print('Calculating tag RSRs...')
        self.populate_cache(posts, tags)

    def populate_cache(self, posts, tags):
        users = {}
        question_map = {}
        # Populate map of questions
        for post in get_questions(posts):
            question_map[post['Id']] = post
        # Generate a dict of users which have tags 
        # which include response time stats
        for post in get_answers(posts):
            if 'OwnerUserId' in post and \
                post['OwnerUserId'] != 1 and \
                post['ParentId'] in question_map:
                if post['OwnerUserId'] not in users:
                    users[post['OwnerUserId']] = {}
                user = users[post['OwnerUserId']]
                question = question_map[post['ParentId']]
                time_diff = answer_time(question, post)
                for tag in tags.get_valid_tags(question):
                    if tag not in user:
                        user[tag] = { 'count' : 0, 'time' : 0 }
                    user[tag]['time'] += time_diff
                    user[tag]['count'] += 1
        # Count the number of users for each tag
        # with an avg response time under 2 hrs
        for user in users.values():
            for tag, stats in user.items():
                average = stats['time'] / float(stats['count'])
                if average < (60*60*2):
                    if tag not in self.cache: self.cache[tag] = 0
                    self.cache[tag] += 1
        # Convert the number into a ratio
        # of the total number of users 
        for tag in self.cache:
            self.cache[tag] = self.cache[tag] / float(len(users))

    def get(self, tag):
        return self.cache[tag] if tag in self.cache else 0 

class ASRs:

    cache = {}

    def __init__(self, posts, tags):
        print('Calculating tag ASRs...')
        self.populate_cache(posts, tags)

    def populate_cache(self, posts, tags):
        users = {}
        question_map = {}
        # Populate map of questions
        for post in get_questions(posts):
            question_map[post['Id']] = post
        # Generate a dict of users which have tags 
        # which include the count of their responses
        for post in get_answers(posts):
            if 'OwnerUserId' in post and \
                post['OwnerUserId'] != 1 and \
                post['ParentId'] in question_map:
                if post['OwnerUserId'] not in users:
                    users[post['OwnerUserId']] = {}
                user = users[post['OwnerUserId']]
                question = question_map[post['ParentId']]
                for tag in tags.get_valid_tags(question):
                    if tag not in user: user[tag] = 0
                    user[tag] += 1
        # Count the number of users for each tag
        # with at least 10 responses
        for user in users.values():
            for tag, count in user.items():
                if count >= 10:
                    if tag not in self.cache: self.cache[tag] = 0
                    self.cache[tag] += 1
        # Convert the number into a ratio
        # of the total number of users 
        for tag in self.cache:
            self.cache[tag] = self.cache[tag] / float(len(users))

    def get(self, tag):
        return self.cache[tag] if tag in self.cache else 0 

class PRs:

    cache = {}
    
    def __init__(self, posts, tags):
        print('Calculating tag PRs...')
        self.populate_cache(posts, tags)

    def populate_cache(self, posts, tags):
        total = 0
        tag_counts = {}
        # Populate a count of occurances
        # for each tag in the dataset
        for post in get_questions(posts):
            for tag in tags.get_valid_tags(post):
                if tag in tag_counts: tag_counts[tag] += 1
                else: tag_counts[tag] = 1
                total += 1
        # Convert the tag counts into a
        # ratio based on total tag occurances
        for tag in tag_counts:
            self.cache[tag] = (tag_counts[tag] / float(total))

    def get(self, tag):
        return self.cache[tag]



class TagCountFeature:

    cache = {}
    
    def __init__(self, posts, tags):
        print('Calculating tag tsf...')
        self.populate_cache(posts, tags)

    def populate_cache(self, posts, tags):
        tag_subcounts = {}
        # Populate a count of occurances
        # for each tag in the dataset
        for post in get_questions(posts):
            for tag in tags.get_valid_tags(post):
                if tag in tagdict:
                    tag_subcounts[tag] = float(tagdict[tag])
                else: tag_subcounts[tag] = 0
        for tag in tag_subcounts:
            self.cache[tag] = (tag_subcounts[tag])

    def get(self, tag):
        return self.cache[tag]

class LastActivityTimeFeature:

    cache = {}
    
    def __init__(self, posts, tags):
        print('Calculating tag latf...')
        self.populate_cache(posts, tags)

    def populate_cache(self, posts, tags):
        tag_timediffcounts = {}
        # Populate a count of occurances
        # for each tag in the dataset
        for post in get_questions(posts):
            time_diff = last_activity_time(post)
            for tag in tags.get_valid_tags(post):
                if tag in tagdict:
                    if tag in tag_timediffcounts: 
                        tag_timediffcounts[tag] += (time_diff / float (tagdict[tag]))
                    else: 
                        tag_timediffcounts[tag] = time_diff / float (tagdict[tag])
                else:
                    tag_timediffcounts[tag] = 0
        for tag in tag_timediffcounts:
                self.cache[tag] = (tag_timediffcounts[tag])
    def get(self, tag):
        return self.cache[tag]


# view count as feature
class ViewCountFeature:

    cache = {}
    
    def __init__(self, posts, tags):
        print('Calculating tag vcf...')
        self.populate_cache(posts, tags)

    def populate_cache(self, posts, tags):
        #total = 0
        tag_viewcounts = {}
        # Populate a count of occurances
        # for each tag in the dataset
        for post in get_questions(posts):
            view = viewcounts(post)
            for tag in tags.get_valid_tags(post):
                if tag in tag_viewcounts: tag_viewcounts[tag] += view
                else: tag_viewcounts[tag] = view
        for tag in tag_viewcounts:
            self.cache[tag] = (tag_viewcounts[tag])

    def get(self, tag):
        return self.cache[tag]

# answer count as feature
class AnswerCountFeature:

    cache = {}
    
    def __init__(self, posts, tags):
        print('Calculating tag acf...')
        self.populate_cache(posts, tags)

    def populate_cache(self, posts, tags):
        #total = 0
        tag_answercounts = {}
        # Populate a count of occurances
        # for each tag in the dataset
        for post in get_questions(posts):
            answer = answercounts(post)
            for tag in tags.get_valid_tags(post):
                if tag in tag_answercounts: tag_answercounts[tag] += answer
                else: tag_answercounts[tag] = answer
        for tag in tag_answercounts:
            self.cache[tag] = (tag_answercounts[tag])

    def get(self, tag):
        return self.cache[tag]


class QAMap:
#edited for version 2 as original code seems to have issues.
    qa_map = {}

    def __init__(self, posts):
        print('Generating answer cache...')
        self.populate_map(posts)

    def populate_map(self, posts):
        # Create a map of questions
        # and their accepted answer
        # Convert the map of accepted
        # answers to the actual answer
        for post in get_answers(posts):
            if post['ParentId'] in answerid:
                    self.qa_map[post['ParentId']] = post

    def has_answer(self, question):
        return False if self.get_answer(question) == None else True
                    
    def get_answer(self, question):
        if question['Id'] not in answerid: return None
        if question['Id'] not in self.qa_map: return None
        return self.qa_map[question['Id']]

class TagSet:

    valid_tags = set()

    def __init__(self, posts):
        print('Generating valid tag set...')
        self.populate_map(posts)
    
    def populate_map(self, posts):
        tags = {}
        question_map = {}
        # Populate map of questions
        for post in get_questions(posts):
           question_map[post['Id']] = post
        # Generate a dict of tags which are a set of 
        # unique responders to those tags
        for post in get_answers(posts):
            if 'OwnerUserId' in post and \
                post['OwnerUserId'] != 1 and \
                post['ParentId'] in question_map:
                question = question_map[post['ParentId']]
                for tag in self.get_tags(question):
                    if tag not in tags: tags[tag] = set()
                    tags[tag].add(post['OwnerUserId'])
        # If the tag has at least 15 responders
        # then populate it into valid_tags
        for tag, users in tags.items():
            count = len(users)
            if count >= 15: self.valid_tags.add(tag)
 
    def get_tags(self, post):
        return post['Tags'][1:-1].split('><')

    def get_valid_tags(self, post):
        tags = self.get_tags(post)
        return filter(lambda x: x in self.valid_tags, tags)

def get_tagname(tagrow): return tagrow['TagName']
def get_tagsub(tagrow): return tagrow['Count']
def get_answers(posts): return filter(is_answer, posts)
def get_questions(posts): return filter(is_question, posts)
def is_question(post): return post['PostTypeId'] == '1'
def is_answer(post): return post['PostTypeId'] == '2'

def answer_time(question, answer):
    q_xml_date = question['CreationDate']
    a_xml_date = answer['CreationDate']
    q_date = datetime.strptime(q_xml_date, '%Y-%m-%dT%H:%M:%S.%f')
    a_date = datetime.strptime(a_xml_date, '%Y-%m-%dT%H:%M:%S.%f')
    diff = a_date - q_date
    return diff.seconds
	
def last_activity_time(question):
    q_xml_date = question['CreationDate']
    a_xml_date = question['LastActivityDate']
    q_date = datetime.strptime(q_xml_date, '%Y-%m-%dT%H:%M:%S.%f')
    a_date = datetime.strptime(a_xml_date, '%Y-%m-%dT%H:%M:%S.%f')
    diff = a_date - q_date
    return diff.seconds

def find_tag_sub(tagrow):
    subcount = tagrow['Count']
    return subcount


def viewcounts(question):
    return int(question['ViewCount'])

def answercounts(question):
    return int(question['AnswerCount'])
	
def generate_dataset(posts, output):
    count = 0
    qas = QAMap(posts)
    tags = TagSet(posts)
    prs = PRs(posts, tags)
    asrs = ASRs(posts, tags)
    rsrs = RSRs(posts, tags)
    latf = LastActivityTimeFeature(posts, tags)
    vcf = ViewCountFeature(posts, tags)
    acf = AnswerCountFeature(posts, tags)
    tcf = TagCountFeature(posts, tags)
    writer = csv.writer(output)
    print('Generating features...')
    for post in get_questions(posts):
        if qas.has_answer(post):
            q_tags = tags.get_valid_tags(post)
            stats = [ [prs.get(t), asrs.get(t), rsrs.get(t), latf.get(t), vcf.get(t), acf.get(t), tcf.get(t)] for t in q_tags ]
            if len(stats) != 0:
                features = np.sum(stats, axis=0)
                resp_time = answer_time(post, qas.get_answer(post))
                writer.writerow(np.append(features, resp_time))
                count += 1
    return count
    
    
# create the dictionary for all tags (key) and subs (value)       
tagdict = {}
in_file_tags = open('filteredtags.json', 'r')
tagfile = json.load(in_file_tags)
for row in tagfile:
    tagdict[get_tagname(row)] = get_tagsub(row)
#print (tagdict)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 generate_all.py filtered2018.json features.csv')
        sys.exit(1)
   
    print('Loading json data...')
    in_file = open(sys.argv[1], 'r')
    posts = json.load(in_file)
    
    # create answer id to relate to questions later
    # old answer will appear first in json file
    answerid = {}

    for post in posts:
        if (post['PostTypeId'] == '2') and (post['ParentId'] not in answerid):
                answerid[post['ParentId']] = post['Id']
    #print(answerid)
    c = generate_dataset(posts, open(sys.argv[2], 'w', newline=''))
    print('\nQuestions extracted: ' + str(c))
    print('Features are: prs, asrs, rsrs, latf, vcf, acf, tsf; and response time as label')
