# -*- coding: utf-8 -*-
#
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from assets.models import AuthBook
from common.utils import get_logger
from .models import AssetPermission


logger = get_logger(__file__)


@receiver(m2m_changed, sender=AssetPermission.nodes.through)
def on_permission_nodes_changed(sender, instance=None, **kwargs):
    if isinstance(instance, AssetPermission) and kwargs['action'] == 'post_add':
        logger.debug("Asset permission nodes change signal received")
        nodes = kwargs['model'].objects.filter(pk__in=kwargs['pk_set'])
        system_users = instance.system_users.all()
        for system_user in system_users:
            system_user.nodes.add(*tuple(nodes))


@receiver(m2m_changed, sender=AssetPermission.assets.through)
def on_permission_assets_changed(sender, instance=None, **kwargs):
    if isinstance(instance, AssetPermission) and kwargs['action'] == 'post_add':
        logger.debug("Asset permission assets change signal received")
        assets = kwargs['model'].objects.filter(pk__in=kwargs['pk_set'])
        system_users = instance.system_users.all()
        for system_user in system_users:
            system_user.assets.add(*tuple(assets))


@receiver(m2m_changed, sender=AssetPermission.system_users.through)
def on_permission_system_users_changed(sender, instance=None, **kwargs):
    if isinstance(instance, AssetPermission) and kwargs['action'] == 'post_add':
        logger.debug("Asset permission system_users change signal received")
        system_users = kwargs['model'].objects.filter(pk__in=kwargs['pk_set'])
        assets = instance.assets.all()
        nodes = instance.nodes.all()
        for system_user in system_users:
            system_user.nodes.add(*tuple(nodes))
            system_user.assets.add(*tuple(assets))


@receiver(post_save, sender=AssetPermission, dispatch_uid='my_unique_identifier')
def on_permission_created_or_update(sender, instance, created=False, **kwargs):
    logger.info('on permission created or update')
    logger.info("Update the relationship between users and assets by perm `{}`"
                .format(instance))
    AuthBook.update_or_create_perms(instance)
