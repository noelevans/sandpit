import sys
import numpy as np
import praw
from IPython.core.display import Image


def main():
    reddit = praw.Reddit("BayesianMethodsForHackers")
    subreddit  = reddit.get_subreddit( "pics" )
    top_submissions = subreddit.get_top()

    n_pic = int( sys.argv[1] ) if len(sys.argv) > 1 else 1

    i = 0
    while i < n_pic:
        top_submission = top_submissions.next()
        while "i.imgur.com" not in top_submission.url:
            #make sure it is linking to an image, not a webpage.
            top_submission = top_submissions.next()
        i+=1

    print "Title of submission: \n", top_submission.title
    top_post_url = top_submission.url
    #top_submission.replace_more_comments(limit=5, threshold=0)
    print top_post_url
    Image(top_post_url)

    upvotes = []
    downvotes = []
    contents = []
    _all_comments = top_submission.comments
    all_comments=[]
    for comment in _all_comments:
        try:
            upvotes.append( comment.ups )
            downvotes.append( comment.downs )
            contents.append( comment.body )
        except Exception as e:
            continue

    votes = np.array( [ upvotes, downvotes] ).T

    n_comments = len(contents)
    comments = np.random.randint(n_comments, size=4)

    print "Some Comments (out of %d total) \n-----------" % n_comments
    for i in comments:
        print '"' + contents[i] + '"'
        print"upvotes/downvotes: ", votes[i, :]
        print


if __name__ == '__main__':
    main()
