from feeds.models import Feed
keywords = ['cyclone', 'dhrought', 'earthquake', 'epidemic', 'fire', 'flood', 'heatwave', 'rain', 'infestation', 'landslide', 'snowfall', 'storm', 'tornado', 'tsunami', 'wind', 'volcano']

for keyword in keywords:
    # google
    print 'Generating a google feed for keyword: %s' % keyword
    f1 = Feed()
    f1.name = 'Feed from Google News for "%s"' % keyword
    f1.description = f1.name
    f1.url_xml = 'https://news.google.it/news/feeds?hl=en&q=%s' % keyword
    f1.url_html = f1.url_xml
    f1.enabled = True
    f1.save()
    f1.tags.add('crisis', keyword)
    # twitter
    f2 = Feed()
    f2.name = 'Tweets for "%s"' % keyword
    f2.description = f2.name
    f2.url_xml = 'http://search.twitter.com/search.rss?q=%s' % keyword
    f2.url_html = f2.url_xml
    f2.enabled = True
    f2.save()
    f2.tags.add('crisis', 'twitter', keyword)
