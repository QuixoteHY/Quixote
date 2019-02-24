# -*- coding:utf-8 -*-
# @Time     : 2019-02-23 20:46
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : 爬虫中间件

from quixote.middleware import MiddlewareManager
from quixote.logger import logger
from quixote.exception.error import ErrorSettings
from quixote.utils.misc import fun_name, is_iterable


class SpiderMiddlewareManager(MiddlewareManager):
    component_name = 'spider middleware'

    @classmethod
    def _get_middleware_list_from_settings(cls, settings):
        mw_dict = settings['SPIDER_MIDDLEWARES']
        preprocess_mw_dict = dict()
        for k, v in mw_dict.items():
            if not v:
                continue
            if isinstance(v, int):
                preprocess_mw_dict[k] = v
            else:
                logger.error('There is an error in your settings file.\nThe variable SPIDER_MIDDLEWARES error.')
                raise ErrorSettings('Settings SPIDER_MIDDLEWARES error: '+str((k, v)))
        sorted_mw_list = sorted(preprocess_mw_dict.items(), key=lambda x: x[1], reverse=False)
        mw_list = list()
        for mw in sorted_mw_list:
            mw_list.append(mw[0])
        return mw_list

    def _add_middleware(self, mw):
        super(SpiderMiddlewareManager, self)._add_middleware(mw)
        if hasattr(mw, 'process_spider_input'):
            self.methods['process_spider_input'].append(mw.process_spider_input)
        if hasattr(mw, 'process_spider_output'):
            self.methods['process_spider_output'].insert(0, mw.process_spider_output)
        if hasattr(mw, 'process_spider_exception'):
            self.methods['process_spider_exception'].insert(0, mw.process_spider_exception)
        if hasattr(mw, 'process_start_requests'):
            self.methods['process_start_requests'].insert(0, mw.process_start_requests)

    def scrape_response(self, scrape_func, response, request, spider):
        def process_spider_input(_response):
            for method in self.methods['process_spider_input']:
                # try:
                #     _result = method(response=_response, spider=spider)
                #     assert _result is None, 'Middleware %s must returns None or raise an exception, got %s ' \
                #                             % (fun_name(method), type(_result))
                # except Exception as e:
                #     logger.warn(e)
                #     return scrape_func(e, request, spider)
                _result = method(response=_response, spider=spider)
                assert _result is None, 'Middleware %s must returns None or raise an exception, got %s ' \
                                        % (fun_name(method), type(_result))
            return scrape_func(_response, request, spider)

        # def process_spider_exception(_failure):
        #     exception = _failure.value
        #     for method in self.methods['process_spider_exception']:
        #         _result = method(response=response, exception=exception, spider=spider)
        #         assert _result is None or is_iterable(_result), \
        #             'Middleware %s must returns None, or an iterable object, got %s ' % \
        #             (fun_name(method), type(_result))
        #         if _result is not None:
        #             return _result
        #     return _failure
        
        def process_spider_output(_result):
            for method in self.methods['process_spider_output']:
                _result = method(response=response, result=_result, spider=spider)
                assert is_iterable(_result), 'Middleware %s must returns an iterable object, got %s ' % \
                                             (fun_name(method), type(_result))
            return _result

        try:
            result = process_spider_input(response)
            return process_spider_output(result)
        except Exception as e:
            print('type(e) = ', type(e))
            logger.warn(e)
            return [e]

    def process_start_requests(self, start_requests, spider):
        return self._process_chain('process_start_requests', start_requests, spider)
