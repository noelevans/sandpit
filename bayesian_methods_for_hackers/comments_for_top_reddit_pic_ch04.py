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

    N = posteriors[0].shape[0]
    lower_limits = []

    for i in range(len(comments)):
        j = comments[i]
        plt.hist(posteriors[i], bins=20, normed=True, alpha=.9,
                 histtype="step", color=colours[i], lw=3,
                 label='(%d up:%d down)\n%s...' % (votes[j, 0], votes[j, 1],
                                                   contents[j][:50]))
        plt.hist(posteriors[i], bins=20, normed=True, alpha=.2,
                 histtype="stepfilled", color=colours[i], lw=3, )
        v = np.sort(posteriors[i])[int(0.05 * N)]
        # plt.vlines( v, 0, 15 , color = "k", alpha = 1, linewidths=3 )
        plt.vlines(v, 0, 10, color=colours[i], linestyles="--", linewidths=3)
        lower_limits.append(v)
        plt.legend(loc="upper left")

    plt.legend(loc="upper left")
    plt.title("Posterior distributions of upvote ratios on different comments")
    plt.show()

    order = np.argsort(-np.array(lower_limits))
    print order, lower_limits

    # This is the closed form method to replace the Markov Chain process above
    # for real-time work

    def intervals(u, d):
        a = 1. + u
        b = 1. + d
        mu = a / (a + b)
        std_err = 1.65 * np.sqrt((a * b) / ((a + b) ** 2 * (a + b + 1.)))
        return (mu, std_err)

    print "Approximate lower bounds:"
    posterior_mean, std_err = intervals(votes[:, 0], votes[:, 1])
    lb = posterior_mean - std_err
    print lb
    print
    print "Top 40 Sorted according to approximate lower bounds:"
    print
    order = np.argsort(-lb)
    ordered_contents = []
    for i in order[:40]:
        ordered_contents.append(contents[i])
        print votes[i, 0], votes[i, 1], contents[i]
        print "-------------"

    # Sorting visually with the lower bound estimation. Also showing the mean
    # and its apparent random fluctuation i.e it's better to use lower bound
    r_order = order[::-1][-40:]
    plt.errorbar(posterior_mean[r_order], np.arange(len(r_order)),
                 xerr=std_err[r_order], xuplims=True, capsize=0, fmt="o",
                 color="#7A68A6")
    plt.xlim(0.3, 1)
    plt.yticks(np.arange(len(r_order) - 1, -1, -1),
               map(lambda x: x[:30].replace("\n", ""), ordered_contents))
    plt.show()


if __name__ == '__main__':
    main()
