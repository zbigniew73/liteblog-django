from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.utils.feedgenerator import Atom1Feed
from blog.models import Post
from django.urls import reverse


class LatestPostsFeed(Feed):
    title = "LiteBlog - Django"
    link = ""
    description = "New posts of my Liteblog"

    def items(self):
        return Post.objects.filter(status=Post.ACTIVE)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 100) # sto pierwszych słów

class AtomSiteNewsFeed(LatestPostsFeed):
    feed_type = Atom1Feed
    subtitle = LatestPostsFeed.description
