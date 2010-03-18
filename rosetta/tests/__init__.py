# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import datetime
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
    
    