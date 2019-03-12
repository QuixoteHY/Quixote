# -*- coding:utf-8 -*-
# @Time     : 2019-03-12 17:31
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : Frame Template

import os
import re
import string

from shutil import ignore_patterns, move, copy2, copystat

from quixote import FRAME_PATH


def render_templatefile(path, **kwargs):
    with open(path, 'rb') as fp:
        raw = fp.read().decode('utf8')
    content = string.Template(raw).substitute(**kwargs)
    render_path = path[:-len('.tmpl')] if path.endswith('.tmpl') else path
    with open(render_path, 'wb') as fp:
        fp.write(content.encode('utf8'))
    if path.endswith('.tmpl'):
        os.remove(path)


CAMELCASE_INVALID_CHARS = re.compile('[^a-zA-Z\d]')
IGNORE = ignore_patterns('*.pyc', '.svn')


def string_camelcase(_string):
    """ Convert a word  to its CamelCase version and remove invalid chars
    >> string_camelcase('lost-pound')
    'LostPound'
    >> string_camelcase('missing_images')
    'MissingImages'
    """
    return CAMELCASE_INVALID_CHARS.sub('', _string.title())


def _copytree(src, dst):
        """
        Since the original function always creates the directory, to resolve
        the issue a new function had to be created. It's a simple copy and
        was reduced for this case.
        """
        print('src='+src+'\ndst='+dst)
        ignore = IGNORE
        names = os.listdir(src)
        ignored_names = ignore(src, names)
        if not os.path.exists(dst):
            os.makedirs(dst)
        for name in names:
            if name in ignored_names:
                continue
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            if os.path.isdir(srcname):
                _copytree(srcname, dstname)
            else:
                copy2(srcname, dstname)
        copystat(src, dst)


def genspider():
    pass


def startproject(project_path, project_name):
    if not os.path.exists(project_path):
        logger.info('你指定的项目所在目录不存在')
        return
    project_path = project_path+'/'+project_name
    if os.path.exists(project_path):
        logger.info('你指定的项目已存在，请检查')
        return
    os.makedirs(project_path)
    if not os.path.exists(project_path):
        logger.info('你指定的项目创建失败')
        return
    templates_dir = FRAME_PATH+'/templates/project'
    _copytree(templates_dir, project_path)


if __name__ == '__main__':
    import sys
    from quixote.logger import logger

    argv_project_path = '/Users/muyichun/Desktop'
    argv_project_name = 'huyuan'
    startproject(argv_project_path, argv_project_name)

    # order = sys.argv[1]
    # if order == 'startproject':
    #     try:
    #         argv_project_path = sys.argv[2]
    #         argv_project_name = sys.argv[3]
    #         startproject(argv_project_path, argv_project_name)
    #     except Exception as e:
    #         logger.info(logger.exception(e))
    # elif order == 'genspider':
    #     try:
    #         genspider()
    #     except Exception as e:
    #         logger.info(logger.exception(e))
    # else:
    #     logger.info('参数错误')
