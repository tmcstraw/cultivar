from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import SpatialDatasetServiceSetting
from tethys_sdk.app_settings import PersistentStoreDatabaseSetting



class Cultivar(TethysAppBase):
    """
    Tethys app class for Cultivar.
    """

    name = 'Cultivar'
    index = 'cultivar:home'
    icon = 'cultivar/images/tree.jpeg'
    package = 'cultivar'
    root_url = 'cultivar'
    color = '#27ae60'
    description = 'Place a brief description of your app here.'
    tags = '&quot;Hydrology&quot;,&quot;Irrigation&quot;'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='cultivar',
                controller='cultivar.controllers.home'
            ),
            UrlMap(name='add-district',
                   url='cultivar/add-district',
                   controller='cultivar.controllers.add_district'
            ),
            UrlMap(
                    name='map',
                    url='cultivar/map',
                    controller='cultivar.controllers.map'
            ),
            UrlMap(
                    name='test',
                    url='cultivar/test',
                    controller='cultivar.controllers.test'
            ),
            UrlMap(
                    name='demand-calculator',
                    url='cultivar/demand-calculator',
                    controller='cultivar.controllers.demand_calculator'
            ),
            UrlMap(
                    name='gis-data-manager',
                    url='cultivar/gis-data-manager',
                    controller='cultivar.controllers.gis_data_manager'
            ),
            UrlMap(
                    name='manage-districts',
                    url='cultivar/manage-districts',
                    controller='cultivar.controllers.manage_districts'
            ),
            UrlMap(
                    name='gistable',
                    url='cultivar/gistable',
                    controller='cultivar.controllers.gistable'
            ),
            UrlMap(
                    name='update-persistent-store-parcel',
                    url='cultivar/gistable/update-persistent-store-parcel',
                    controller='cultivar.controllers.update_persistent_store_parcel'
            ),
            # UrlMap(
            #         name='get-default-values',
            #         url='cultivar/gistable/get-default-values',
            #         controller='cultivar.controllers.get_default_values'
            # ),

        )

        return url_maps


    def spatial_dataset_service_settings(self):
        """
        Example spatial_dataset_service_settings method.
        """
        sds_settings = (
            SpatialDatasetServiceSetting(
                name='main_geoserver',
                description='spatial dataset service for app to use',
                engine=SpatialDatasetServiceSetting.GEOSERVER,
                required=True,
            ),
        )

        return sds_settings


    def persistent_store_settings(self):
        """
        Define Persistent Store Settings.
        """
        ps_settings = (
            PersistentStoreDatabaseSetting(
                name='primary_db',
                description='primary database',
                initializer='cultivar.model.init_primary_db',
                required=True
            ),
        )

        return ps_settings
