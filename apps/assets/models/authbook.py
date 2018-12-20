#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from django.db import models
from django.utils.translation import ugettext as _


from perms.models import AssetPermission
from .base import AssetUser
from ..models import Asset


class AuthBook(AssetUser):

    asset = models.ForeignKey(
        'assets.Asset', on_delete=models.CASCADE, verbose_name=_('Asset')
    )

    @classmethod
    def get_auth_from_auth_book(cls, query_field):
        try:
            obj = cls.objects.get(**query_field)
        except AuthBook.DoesNotExist:
            auth = {}
        else:
            auth = obj.get_auth_from_local()
        return auth

    @classmethod
    def update_or_create_by_asset(cls, asset):
        if not isinstance(asset, Asset):
            return None
        admin_user = asset.admin_user
        obj = cls.update_or_create_by_user_asset(admin_user, asset)
        return obj

    @classmethod
    def update_or_create_perms(cls, perm):
        if not isinstance(perm, AssetPermission):
            return None

        assets = set(perm.assets.all())
        for node in perm.nodes.all():
            assets.update(set(node.assets.all()))
        system_users = set(perm.system_users.all())

        for asset in assets:
            for system_user in system_users:
                cls.update_or_create_by_user_asset(system_user, asset)

    @classmethod
    def update_or_create_by_user_asset(cls, user, asset):
        """
        :param user: 继承了assets.models.AssetUser的类的实例对象
        :param asset: assets.models.Asset
        :return: AuthBook obj
        """
        lookup = {
            'username': user.username, 'asset': asset
        }

        auth = user.get_auth()
        defaults = {
            'name': "{}:{}".format(user.username, asset.hostname)
        }
        defaults.update(**lookup)
        defaults.update(**auth)
        obj = cls.update_or_create(defaults, **lookup)
        return obj

    @classmethod
    def update_or_create(cls, defaults, **kwargs):
        auth = {
            'password': defaults.pop('password'),
            'public_key': defaults.pop('public_key'),
            'private_key': defaults.pop('private_key')
        }
        obj, created = cls.objects.update_or_create(defaults=defaults, **kwargs)
        obj.set_auth(**auth)
        return obj

    def __str__(self):
        return '{}:{}'.format(self.asset.hostname, self.username)
