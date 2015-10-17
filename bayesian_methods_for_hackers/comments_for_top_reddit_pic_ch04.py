import sys
import numpy as np
import praw
import pymc as pm
from matplotlib import pyplot as plt
from IPython.core.display import Image


def posterior_upvote_ratio(upvotes, downvotes, samples=20000):
    """ This function accepts the number of upvotes and downvotes a particular
        comment received, and the number of posterior samples to return to the
        user. Assumes a uniform prior.
    """
    N = upvotes + downvotes
    upvote_ratio = pm.Uniform("upvote_ratio", 0, 1)
    observations = pm.Binomial("obs", N, upvote_ratio, value=upvotes,
                               observed=True)
    # do the fitting; first do a MAP as it is cheap and useful.
    map_ = pm.MAP([upvote_ratio, observations]).fit()
    mcmc = pm.MCMC([upvote_ratio, observations])
    mcmc.sample(samples, samples / 4)
    return mcmc.trace("upvote_ratio")[:]


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
        print "upvotes/downvotes: ", votes[i, :]
        print

    posteriors = []
    colours = ["#348ABD", "#A60628", "#7A68A6", "#467821", "#CF4457"]
    for i in range(len(comments)):
        j = comments[i]
        posteriors.append(posterior_upvote_ratio(votes[j, 0], votes[j, 1]))
        label = '(%d up:%d down)\n%s...' % (votes[j, 0], votes[j, 1],
                                            contents[j][:50])
        plt.hist(posteriors[i], bins=18, normed=True, alpha=.9,
                 histtype="step", color=colours[i % 5], lw=3,
                 label=label)
        plt.hist(posteriors[i], bins=18, normed=True, alpha=.2,
                 histtype="stepfilled", color=colours[i], lw=3, )

    plt.legend(loc="upper left")
    plt.xlim(0, 1)
    plt.title("Posterior distributions of upvote ratios on different comments")
    plt.show()


if __name__ == '__main__':
    main()
