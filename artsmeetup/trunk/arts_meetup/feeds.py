from django.contrib.syndication.feeds  import Feed
from arts_meetup.users.models          import Profile

# You can put lots of classes here to define different feeds


class LatestEntries(Feed):
    title = "Latest users updating"
    link = "/sitenews/"
    description = "Who's currently updating their profile"

    def items(self):
        return User.objects.order_by('-last_activity')[:5]
