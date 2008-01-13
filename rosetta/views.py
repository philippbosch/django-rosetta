from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import ObjectPaginator, InvalidPage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from rosetta.poutil import find_pos
from rosetta.polib import pofile

import re,os


@user_passes_test(lambda user:can_translate(user))
def home(request):
    """
    Displays a list of messages to be translated
    """

    if 'rosetta_i18n_fn' in request.session:
        rosetta_i18n_fn=request.session.get('rosetta_i18n_fn')
        rosetta_i18n_pofile = request.session.get('rosetta_i18n_pofile')
        
        if 'filter' in request.GET:
            if request.GET.get('filter') == 'untranslated' or request.GET.get('filter') == 'translated' or request.GET.get('filter') == 'both':
                filter_ = request.GET.get('filter')
                request.session['rosetta_i18n_filter'] = filter_
                return HttpResponseRedirect(reverse('rosetta-home'))
        elif 'rosetta_i18n_filter' in request.session:
            rosetta_i18n_filter = request.session.get('rosetta_i18n_filter')
        else:
            rosetta_i18n_filter = 'both'
                
        if '_next' in request.POST:
            rx=re.compile(r'^m_([0-9]+)')
            rx_plural=re.compile(r'^m_([0-9]+)_([0-9]+)')
            file_change = False
            for k in request.POST.keys():
                if rx_plural.match(k):
                    id=int(rx_plural.match(k).groups()[0])
                    idx=str(rx_plural.match(k).groups()[1])
                    rosetta_i18n_pofile[id].msgstr_plural[idx] = request.POST.get(k)
                    file_change = True 
                elif rx.match(k):
                    id=int(rx.match(k).groups()[0])
                    rosetta_i18n_pofile[id].msgstr = request.POST.get(k)
                    file_change = True
                if file_change and 'fuzzy' in rosetta_i18n_pofile[id].flags:
                    rosetta_i18n_pofile[id].flags.remove('fuzzy')
                    
                        
            if file_change:
                rosetta_i18n_pofile.metadata['Last-Translator'] = str("%s %s <%s>" %(request.user.first_name,request.user.last_name,request.user.email))
                rosetta_i18n_pofile.save()
                rosetta_i18n_pofile.save_as_mofile(rosetta_i18n_fn.replace('.po','.mo'))
                request.session['rosetta_i18n_pofile']=rosetta_i18n_pofile
                    
            return HttpResponseRedirect(reverse('rosetta-home'))
            
        rosetta_i18n_lang_name = request.session.get('rosetta_i18n_lang_name')
        rosetta_i18n_lang_code = request.session.get('rosetta_i18n_lang_code')
        
        if rosetta_i18n_filter == 'both':
            paginator = ObjectPaginator(rosetta_i18n_pofile, 10)
        elif rosetta_i18n_filter == 'untranslated':
            paginator = ObjectPaginator(rosetta_i18n_pofile.untranslated_entries(), 10)
        elif rosetta_i18n_filter == 'translated':
            paginator = ObjectPaginator(rosetta_i18n_pofile.translated_entries(), 10)
        
        if 'page' in request.GET and int(request.GET.get('page')) < paginator.pages:
            page = int(request.GET.get('page'))
        else:
            page = 0
        messages = paginator.get_page(page)
        needs_pagination = paginator.pages > 1
        if needs_pagination:
            page_range = range(paginator.pages)
        ADMIN_MEDIA_PREFIX = settings.ADMIN_MEDIA_PREFIX
        return render_to_response('rosetta/pofile.html', locals())
    else:
        return list_languages(request)

@user_passes_test(lambda user:can_translate(user))
def list_languages(request):
    """
    Lists the languages for the current project, the gettext catalog files
    that can be translated and their translation progress
    """
    languages = []
    do_self = 'self' in request.GET
    for language in settings.LANGUAGES:
        pos = find_pos(language[0],do_self)
        languages.append(
            (language[0], 
            language[1],
            [(os.path.realpath(l), pofile(l)) for l in  pos],
            )
        )
    ADMIN_MEDIA_PREFIX = settings.ADMIN_MEDIA_PREFIX
    return render_to_response('rosetta/languages.html', locals())    

@user_passes_test(lambda user:can_translate(user))
def lang_sel(request,langid,idx):
    """
    Selects a file to be translated
    """
    if langid not in [l[0] for l in settings.LANGUAGES]:
        raise Http404
    else:
        do_self = 'self' in request.GET
        file_ = find_pos(langid,do_self)[int(idx)]
        request.session['rosetta_i18n_lang_code'] = langid
        request.session['rosetta_i18n_lang_name'] = [l[1] for l in settings.LANGUAGES if l[0] == langid][0]
        request.session['rosetta_i18n_fn'] = file_
        request.session['rosetta_i18n_meta'] = do_self
        po = pofile(file_)
        for i in range(len(po)):
            po[i].id = i
            
        request.session['rosetta_i18n_pofile'] = po
        
        return HttpResponseRedirect(reverse('rosetta-home'))

def can_translate(user):
    if not user.is_authenticated():
        return False
    elif user.is_superuser:
        return True
    else:
        try:
            from django.contrib.auth.models import Group
            translators = Group.objects.get(name='translators')
            return translators in user.groups.all()
        except Group.DoesNotExist:
            return False

