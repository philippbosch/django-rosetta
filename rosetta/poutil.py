import re, string, sys, os
from django.conf import settings

def find_pos(lang, include_djangos = False, include_rosetta = False):
    """
    scans a couple possible repositories of gettext catalogs for the given 
    language code
    
    """
    
    paths = []
    
    # project/locale
    parts = settings.SETTINGS_MODULE.split('.')
    project = __import__(parts[0], {}, {}, [])
    paths.append(os.path.join(os.path.dirname(project.__file__), 'locale'))
    
    # django/locale
    if include_djangos:
        paths.append(os.path.join(os.path.dirname(sys.modules[settings.__module__].__file__), 'locale'))
    
    # settings 
    for localepath in settings.LOCALE_PATHS:
        if os.path.isdir(localepath):
            paths.append(localepath)
    
    # project/app/locale
    for appname in settings.INSTALLED_APPS:
        if 'rosetta' == appname and include_rosetta == False:
            continue
            
        p = appname.rfind('.')
        if p >= 0:
            app = getattr(__import__(appname[:p], {}, {}, [appname[p+1:]]), appname[p+1:])
        else:
            app = __import__(appname, {}, {}, [])

        apppath = os.path.join(os.path.dirname(app.__file__), 'locale')

        if os.path.isdir(apppath):
            paths.append(apppath)
            
    ret = []
    rx=re.compile(r'(\w+)/../\1')
    for path in paths:
        dirname = rx.sub(r'\1', '%s/%s/LC_MESSAGES/' %(path,lang))
        for fn in ('django.po','djangojs.po',):
            if os.path.isfile(dirname+fn):
                ret.append(dirname+fn)
    return ret
