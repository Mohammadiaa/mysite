from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse
from myblog.models import Post


class RssTutorialsFeeds(Feed):
    title = "blog newest posts"
    link = "/rss/feed"
    description = "best blog ever"

    def items(self):
        return Post.objects.filter(status=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)

    def item_lastupdated(self, item):
        return item.updated_date