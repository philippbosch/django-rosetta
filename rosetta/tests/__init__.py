# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import datetime, os, shutil
from django.conf import settings

class RosettaTestCase(TestCase):
    urls = 'rosetta.tests.urls'

    def setUp(self):
        user = User.objects.create_user('test_admin', 'test@test.com', 'test_password')
        user.is_superuser = True
        user.save()
        
        self.client.login(username='test_admin',password='test_password')
        settings.LANGUAGES = (('xx','dummy language'),)
        

    def test_1_ListLoading(self):
        r = self.client.get(reverse('rosetta-pick-file') +'?rosetta')
        self.assertTrue('rosetta/locale/xx/LC_MESSAGES/django.po' in r.content)
        
        
    def test_2_PickFile(self):
        r = self.client.get(reverse('rosetta-language-selection', args=('xx',0,), kwargs=dict() ) +'?rosetta')
        r = self.client.get(reverse('rosetta-home'))
        
        self.assertTrue('dummy language' in r.content)
        
    def test_3_DownloadZIP(self):
        r = self.client.get(reverse('rosetta-language-selection', args=('xx',0,), kwargs=dict() ) +'?rosetta')
        r = self.client.get(reverse('rosetta-home'))
        r = self.client.get(reverse('rosetta-download-file' ) +'?rosetta')
        self.assertTrue ('content-type' in r._headers.keys() )
        self.assertTrue ('application/x-zip' in r._headers.get('content-type'))
    
    def test_4_DoChanges(self):
        curdir = os.path.dirname(__file__)
        # copy the template file
        shutil.copy(os.path.join(curdir,'../locale/xx/LC_MESSAGES/django.po'), os.path.join(curdir,'../locale/xx/LC_MESSAGES/django.po.orig'))
        shutil.copy(os.path.join(curdir,'./django.po.template'), os.path.join(curdir,'../locale/xx/LC_MESSAGES/django.po'))

        # Load the template file
        r = self.client.get(reverse('rosetta-language-selection', args=('xx',0,), kwargs=dict() ) +'?rosetta')
        r = self.client.get(reverse('rosetta-home') + '?filter=untranslated')
        r = self.client.get(reverse('rosetta-home'))
        
        # make sure both strings are untranslated
        self.assertTrue('dummy language' in r.content)
        self.assertTrue('String 1' in r.content)
        self.assertTrue('String 2' in r.content)
        
        # post a translation
        r = self.client.post(reverse('rosetta-home'), dict(m_1='Hello, world', _next='_next'))
        
        # reload all untranslated strings
        r = self.client.get(reverse('rosetta-language-selection', args=('xx',0,), kwargs=dict() ) +'?rosetta')
        r = self.client.get(reverse('rosetta-home') + '?filter=untranslated')
        r = self.client.get(reverse('rosetta-home'))
        
        # the translated string no longer is up for translation
        self.assertTrue('String 1'  in r.content)
        self.assertTrue('String 2' not in r.content)
        
        # display only translated strings
        r = self.client.get(reverse('rosetta-home') + '?filter=translated')
        r = self.client.get(reverse('rosetta-home'))
        
        # The tranlsation was persisted
        self.assertTrue('String 1' not  in r.content)
        self.assertTrue('String 2' in r.content)
        self.assertTrue('Hello, world' in r.content)
        
        # reset the original file
        shutil.move(os.path.join(curdir,'../locale/xx/LC_MESSAGES/django.po.orig'), os.path.join(curdir,'../locale/xx/LC_MESSAGES/django.po'))
        