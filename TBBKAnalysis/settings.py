# Scrapy settings for TBBKAnalysis project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'TBBKAnalysis'

SPIDER_MODULES = ['TBBKAnalysis.spiders']
NEWSPIDER_MODULE = 'TBBKAnalysis.spiders'

ITEM_PIPELINES = {
    'TBBKAnalysis.pipelines.TbbkanalysisPipeline':300
}

COOKIES_ENABLED = False
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'TBBKAnalysis (+http://www.yourdomain.com)'
DOWNLOADER_MIDDLEWARES = {
     'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
     'TBBKAnalysis.spiders.rotate_useragent.RotateUserAgentMiddleware' :400
}