# -*- coding:utf-8 -*-
# @Time     : 2019-01-20 22:16
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : Downloader Middleware manager

import logging
import six

import asyncio

from quixote.protocol import Request, Response
from quixote.exception.error import ErrorSettings
from quixote.middleware import MiddlewareManager

logger = logging.getLogger(__name__)


class DownloaderMiddlewareManager(MiddlewareManager):
    component_name = 'downloader middleware'

    @classmethod
    def _get_middleware_list_from_settings(cls, settings):
        mw_dict = settings['DOWNLOADER_MIDDLEWARES']
        preprocess_mw_dict = dict()
        for k, v in mw_dict.items():
            if not v:
                continue
            if isinstance(v, int):
                preprocess_mw_dict[k] = v
            else:
                logger.error('There is an error in your settings file.\nThe variable DOWNLOADER_MIDDLEWARES error.')
                raise ErrorSettings('Settings DOWNLOADER_MIDDLEWARES error: '+str((k, v)))
        sorted_mw_list = sorted(preprocess_mw_dict.items(), key=lambda x: x[1], reverse=False)
        mw_list = list()
        for mw in sorted_mw_list:
            mw_list.append(mw[0])
        return mw_list

    def _add_middleware(self, mw):
        if hasattr(mw, 'process_request'):
            self.methods['process_request'].append(mw.process_request)
        if hasattr(mw, 'process_response'):
            self.methods['process_response'].insert(0, mw.process_response)
        if hasattr(mw, 'process_exception'):
            self.methods['process_exception'].insert(0, mw.process_exception)

    async def download(self, download_func, request, spider):

        async def process_request(_request):
            for method in self.methods['process_request']:
                response = await method(request=_request, spider=spider)
                assert response is None or isinstance(response, (Response, Request)), \
                    'Middleware %s.process_request must return None, Response or Request, got %s' % \
                    (six.get_method_self(method).__class__.__name__, response.__class__.__name__)
                if response:
                    return response
            return await download_func(_request, spider)

        def process_response(response):
            assert response is not None, 'Received None in process_response'
            if isinstance(response, Request):
                return Request
            for method in self.methods['process_response']:
                response = method(request=request, response=response, spider=spider)
                assert isinstance(response, (Response, Request)), \
                    'Middleware %s.process_response must return Response or Request, got %s' % \
                    (six.get_method_self(method).__class__.__name__, type(response))
                if isinstance(response, Request):
                    return Request
            return response

        # def process_exception(_failure):
        #     exception = _failure.value
        #     for method in self.methods['process_exception']:
        #         response = method(request=request, exception=exception, spider=spider)
        #         assert response is None or isinstance(response, (Response, Request)), \
        #             'Middleware %s.process_exception must return None, Response or Request, got %s' % \
        #             (six.get_method_self(method).__class__.__name__, type(response))
        #         if response:
        #             return

        task = asyncio.ensure_future(process_request(request))
        task.add_done_callback(process_response)
        return task
        # response = await self.process_request(request, spider)
        # if response:
        #     if isinstance(response, Response):
        #         await self.process_response(request, response, spider)
        #     if isinstance(response, Request):
        #         return response
        # else:
        #     return download_func(request, response)
