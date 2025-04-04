# -*- coding: utf-8 -*-
# Copyright (C) 1998-2016 by the Free Software Foundation, Inc.
#
# This file is part of Postorius.
#
# Postorius is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# Postorius is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Postorius.  If not, see <http://www.gnu.org/licenses/>.

# from django.conf.urls import include
# from django.contrib import admin
# from django.urls import path,re_path, reverse_lazy
# from django.views.generic import RedirectView
# import django_saml2_auth.views
# 
# urlpatterns = [
#     path(r'', RedirectView.as_view(
#         url=reverse_lazy('list_index'),
#         permanent=True)),
#     path(r'postorius/', include('postorius.urls')),
#     path(r'hyperkitty/', include('hyperkitty.urls')),
#     path(r'', include('django_mailman3.urls')),
#     path(r'accounts/', include('allauth.urls')),
#     # Django admin
#     path(r'admin/', admin.site.urls),
# ]

from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path, reverse_lazy
from django.views.generic import RedirectView
import django_saml2_auth.views

urlpatterns = [
    # Redirect the root URL to 'list_index'
    path('', RedirectView.as_view(url=reverse_lazy('list_index'), permanent=True)),

    # SAML 2.0 Authentication routes for Single Sign-On (SSO)
    re_path(r'^sso/', include('django_saml2_auth.urls')),
    re_path(r'^accounts/login/$', django_saml2_auth.views.signin),
    re_path(r'^admin/login/$', django_saml2_auth.views.signin),

    # Mailman 3 components
    path('postorius/', include('postorius.urls')),
    path('hyperkitty/', include('hyperkitty.urls')),
    path('mailman3/', include('postorius.urls')),
    path('archives/', include('hyperkitty.urls')),
    path('', include('django_mailman3.urls')),

    # Authentication related
    path('accounts/', include('allauth.urls')),

    # Django admin
    path('admin/', admin.site.urls),
]
