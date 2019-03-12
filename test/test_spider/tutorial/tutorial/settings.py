

# BOT_NAME = 'tutorial'
# SPIDER_MODULES = ['tutorial.spiders']
# NEWSPIDER_MODULE = 'tutorial.spiders'
BOT_NAME = 'quixote'
SPIDER_MODULES = ['test.test_spider.tutorial.tutorial.spiders']
NEWSPIDER_MODULE = 'test.test_spider.tutorial.tutorial.spiders'


# ITEM_PIPELINES = {
#     'tutorial.tutorial.pipelines.TestPipeline': 100,
#     'tutorial.tutorial.pipelines.TestPipeline2': 101,
# }
ITEM_PIPELINES = {
    'quixote.test.test_spider.tutorial.tutorial.pipelines.TestPipeline': 100,
    'quixote.test.test_spider.tutorial.tutorial.pipelines.TestPipeline2': 101,
}


# SPIDER_MIDDLEWARES = {
#     'tutorial.tutorial.middleware.TestMiddleware': 100,
# }
SPIDER_MIDDLEWARES = {
    'quixote.test.test_spider.tutorial.tutorial.middleware.TestMiddleware': 100,
}
