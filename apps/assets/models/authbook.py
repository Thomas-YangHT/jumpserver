#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from django.db import models
from django.utils.translation import ugettext as _

from .base import AssetUser


class AuthBook(AssetUser):

    asset = models.ForeignKey('assets.Asset', on_delete=models.CASCADE, verbose_name=_('Asset'))

    def __str__(self):
        return '{}:{}'.format(self.asset.hostname, self.username)
