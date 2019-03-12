

class TestMiddleware(object):

    def process_start_requests(self, request, spider):
        request.url = request.url + '_YYYYYYYYYY'
        return request
