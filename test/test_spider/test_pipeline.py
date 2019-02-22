
from quixote.exception.exceptions import DropItem


class TestPipeline(object):
    count = 0

    def process_item(self, item, spider):
        self.count += 1
        if self.count % 10 != 0:
            item['pipeline'].append('TestPipeline')
            return item
        else:
            raise DropItem('TestPipeline DropItem: %s' % item)
