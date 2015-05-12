#!/usr/bin/env python
import urllib2
import json
from datetime import datetime

def get_url(offset):
    return "https://api.vk.com/method/wall.get?domain=teamnavalny&extended=1&filter=all&version=5.31&offset=%s&count=1000" % (offset)

def write_header(out):
    data = '\t'.join(['post_id', 'text', 'date', 'num_comments', 'num_likes', 'num_reposts', 'attachment_types'])
    line = '%s\n' % data
    out.write(line)

def save_posts(response, out):
    posts = response['wall'][1:]
    for post in posts:
        post_id = post['id']
        text = post['text']
        date = datetime.fromtimestamp(post['date'])
        comments = post['comments']['count']
        likes = post['likes']['count']
        reposts = post['reposts']['count']
        if 'attachments' in post:
            attachments = map(lambda x: x['type'], post['attachments'])
        else:
            attachments = []
        data = '\t'.join(map(str, [post_id, text.encode('utf-8'), date, comments, likes, reposts, ','.join(attachments)]))
        line = '%s\n' % data
        out.write(line)

filename = "data/posts.tsv"
out = open(filename, 'w')
url = get_url(0)
response = json.loads(urllib2.urlopen(url).read())['response']
write_header(out)
save_posts(response, out)
count = 2250 / 1000
for i in range(1, count + 1):
    url = get_url(i * 1000)
    response = json.loads(urllib2.urlopen(url).read())['response']
    save_posts(response, out)
out.close()
