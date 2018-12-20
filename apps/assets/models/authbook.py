#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from django.db import models
from django.utils.translation import ugettext as _


from .base import AssetUser
from ..models import Asset


def get_auth_from_vault(query_field):
    # TODO: get auth from vault
    return {}


def update_or_create_vault():
    # TODO: set auth to vault
    pass


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

    @classmethod
    def update_or_create_auth_book_or_vault_by_asset(cls, asset):
        cls.update_or_create_by_asset(asset)
        update_or_create_vault()

    @classmethod
    def update_or_create_by_asset(cls, asset):
        if not isinstance(asset, Asset):
            return None

        admin_user = asset.admin_user
        kwargs = {
            'username': admin_user.username,
            'asset': asset
        }
        defaults = kwargs.update({
            'name': "{}:{}".format(admin_user.username, asset.hostname)
        })
        obj, created = cls.objects.update_or_create(defaults=defaults, **kwargs)

        auth = admin_user.get_auth()
        obj.set_auth(**auth)
        return obj

    def __str__(self):
        return '{}:{}'.format(self.asset.hostname, self.username)
