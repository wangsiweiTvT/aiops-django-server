import nacos

from django.conf import settings
from django.core.management.base import BaseCommand


class NacosService:
    def __init__(self, nacos_address, nacos_namespace, nacos_group, nacos_username, nacos_password):
        self.nacos_address = nacos_address
        self.nacos_namespace = nacos_namespace
        self.nacos_group = nacos_group
        self.nacos_username = nacos_username
        self.nacos_password = nacos_password
        self.client = nacos.NacosClient(self.nacos_address, namespace=self.nacos_namespace,
                                        username=self.nacos_username, password=self.nacos_password)

    def register_service(self, service_name, port):
        self.client.add_naming_instance(service_name, f"{settings.DOMAIN}:{port}", ip=settings.DOMAIN, port=port,
                                        group=self.nacos_group, weight=1, healthy=True, enabled=True, ephemeral=True)

    def deregister_service(self, service_name, port):
        self.client.remove_naming_instance(service_name, f"{settings.DOMAIN}:{port}", ip=settings.DOMAIN, port=port,
                                           group=self.nacos_group)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        nacos_service = NacosService(
            nacos_address='http://nacos-server-address:8848',
            nacos_namespace='namespace-id',
            nacos_group='group-name',
            nacos_username='nacos-username',
            nacos_password='nacos-password',
        )
        nacos_service.register_service('my_service', settings.PORT)