VERSION = (0, 4, 'pre')

def get_version(svn=False):
    "Returns the version as a human-format string."
    v = '.'.join([str(i) for i in VERSION])
    if svn:
        from django.utils.version import get_svn_revision
        svn_rev = get_svn_revision('.')
        if svn_rev:
            v = '%s-%s' % (v, svn_rev)
    return v
