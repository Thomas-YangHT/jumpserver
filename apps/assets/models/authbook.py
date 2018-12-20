#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from django.db import models
from django.utils.translation import ugettext as _

from .base import AssetUser


def get_auth_from_vault(query_field):
    # TODO: get auth from vault
    return {}


class AuthBook(AssetUser):

    asset = models.ForeignKey(
        'assets.Asset', on_delete=models.CASCADE, verbose_name=_('Asset')
    )

    @classmethod
    def get_auth_from_auth_book_or_vault(cls, query_field):
        try:
            obj = cls.objects.get(**query_field)
        except AuthBook.DoesNotExist:
            auth = get_auth_from_vault(query_field)
        else:
            auth = obj.get_auth_from_local()
        return auth

    def __str__(self):
        return '{}:{}'.format(self.asset.hostname, self.username)
