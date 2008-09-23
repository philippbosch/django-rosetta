# Number of messages to display per page.
MESSAGES_PER_PAGE = 10

# Enable Google translation suggestions
ENABLE_TRANSLATION_SUGGESTIONS = True

"""
When running WSGI daemon mode, using mod_wsgi 2.0c5 or later, this setting 
can be used to automatically reload the contents of the gettext catalog 
being translated on the live site after each change, without the need to 
restart the whole Apache webserver process.

To enabled this feature, simply give the full path of the WSGI script file, 
as defined by the WSGIScriptAlias directive.

To disable it, set this variable to an empty string or None

Notes:

 * The WSGI daemon process must have write permissions on the WSGI script file.
 * set WSGIScriptReloading must be set to On (it is by default)
 * For the sake of performance, this setting should be disabled in production 
   environments
 * When the Rosetta application is being shared among different Django projects, 
   each running its own distinct WSGI script file, you can set this configuration 
   setting in your individual project configuration (i.e. in your project's settings.py )

Refs: 
 * http://code.google.com/p/modwsgi/wiki/ReloadingSourceCode 
 * http://code.google.com/p/modwsgi/wiki/ConfigurationDirectives#WSGIReloadMechanism
 
"""
WSGI_SCRIPT_FILE = ''
