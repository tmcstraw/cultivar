/*Global Variables */

var layers,
    featureOverlay,
    wmsLayer,
    wms_url,
    map,
    info,
    displayFeatureInfo,
    view,
    current_layer,
    res_name,
    coordinate,
    map_events;

/*this function creates the base map on the home page*/
function init_map(){


    /*basemap for the map*/
    var base_layer = new ol.layer.Tile({
        source: new ol.source.BingMaps({
            key: 'eLVu8tDRPeQqmBlKAjcw~82nOqZJe2EpKmqd-kQrSmg~AocUZ43djJ-hMBHQdYDyMbT-Enfsk0mtUIGws1WeDuOvjY4EXCH-9OK3edNLDgkc',
            imagerySet: 'AerialWithLabels'
        })
    });

    /*initial view for the map. You can change the view by changing the lat,long or zoom */
    var view = new ol.View({
        center: ol.proj.transform([-70.8, 18.83], 'EPSG:4326', 'EPSG:3857'),
        minZoom: 2,
        maxZoom: 18,
        zoom:7.8
    });




    /*identifies which layers will show in the map*/
    layers = [base_layer];

    /*creates the map with the specified views, layers, and popups from above*/
    map = new ol.Map({
        target: 'map',
        view: view,
        layers:layers,
    });

    /*searched for the reservoir layer on the geoserver and grabs it. This will need to be changed when installed on a different computer*/
    var wmsLayer = new ol.layer.Image({
        source: new ol.source.ImageWMS({
            url: 'http://localhost:8181/geoserver/wms',
            params: {'LAYERS': 'districts'},
            serverType: 'geoserver',
            crossOrigin: 'Anonymous'


        })
    });

    map.addLayer(wmsLayer);
 }

$(function(){
//    $('#app-content-wrapper').removeClass('show-nav');
//    $('#app-actions').remove();
    $(".toggle-nav").removeClass('toggle-nav');
    init_map();
});


function init_demand_map(){


    /*basemap for the map*/
    var base_layer = new ol.layer.Tile({
        source: new ol.source.BingMaps({
            key: 'eLVu8tDRPeQqmBlKAjcw~82nOqZJe2EpKmqd-kQrSmg~AocUZ43djJ-hMBHQdYDyMbT-Enfsk0mtUIGws1WeDuOvjY4EXCH-9OK3edNLDgkc',
            imagerySet: 'AerialWithLabels'
        })
    });

    /*initial view for the map. You can change the view by changing the lat,long or zoom */
    var view = new ol.View({
        center: ol.proj.transform([-70.8, 18.83], 'EPSG:4326', 'EPSG:3857'),
        minZoom: 2,
        maxZoom: 18,
        zoom:7.8
    });




    /*identifies which layers will show in the map*/
    layers = [base_layer];

    /*creates the map with the specified views, layers, and popups from above*/
    demandmap = new ol.Map({
        target: 'demandmap',
        view: view,
        layers:layers,
    });

    /*searched for the reservoir layer on the geoserver and grabs it. This will need to be changed when installed on a different computer*/
    var wmsLayer = new ol.layer.Image({
        source: new ol.source.ImageWMS({
            url: 'http://localhost:8181/geoserver/wms',
            params: {'LAYERS': 'districts'},
            serverType: 'geoserver',
            crossOrigin: 'Anonymous'


        })
    });

    demandmap.addLayer(wmsLayer);
 }

 function init_gis_map(){


    /*basemap for the map*/
    var base_layer = new ol.layer.Tile({
        source: new ol.source.BingMaps({
            key: 'eLVu8tDRPeQqmBlKAjcw~82nOqZJe2EpKmqd-kQrSmg~AocUZ43djJ-hMBHQdYDyMbT-Enfsk0mtUIGws1WeDuOvjY4EXCH-9OK3edNLDgkc',
            imagerySet: 'AerialWithLabels'
        })
    });

    /*initial view for the map. You can change the view by changing the lat,long or zoom */
    var view = new ol.View({
        center: ol.proj.transform([-70.8, 18.83], 'EPSG:4326', 'EPSG:3857'),
        minZoom: 2,
        maxZoom: 18,
        zoom:7.8
    });




    /*identifies which layers will show in the map*/
    layers = [base_layer];

    var container = document.getElementById('popup');
      var content = document.getElementById('popup-content');
      var closer = document.getElementById('popup-closer');


      /**
       * Create an overlay to anchor the popup to the map.
       */
      var overlay = new ol.Overlay({
        element: container,
        autoPan: true,
        autoPanAnimation: {
          duration: 250
        }
      });


      /**
       * Add a click handler to hide the popup.
       * @return {boolean} Don't follow the href.
       */
      closer.onclick = function() {
        overlay.setPosition(undefined);
        closer.blur();
        return false;
      };

    /*creates the map with the specified views, layers, and popups from above*/
    gismap = new ol.Map({
        target: 'gismap',
        view: view,
        layers:layers,
        overlays:[overlay]
    });

    /*searched for the reservoir layer on the geoserver and grabs it. This will need to be changed when installed on a different computer*/
    var wmsLayer = new ol.layer.Image({
        source: new ol.source.ImageWMS({
            url: 'http://localhost:8181/geoserver/wms',
            params: {'LAYERS': 'parcels'},
            serverType: 'geoserver',
            crossOrigin: 'Anonymous'


        })
    });

    gismap.addLayer(wmsLayer);

    gismap.on('singleclick', function(evt) {
        var coordinate = evt.coordinate;
        var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
            coordinate, 'EPSG:3857', 'EPSG:4326'));

        content.innerHTML = '<p>You clicked here:</p><code>' + hdms +
            '</code>';
        overlay.setPosition(coordinate);
      });
 }


$(function(){
//    $('#app-content-wrapper').removeClass('show-nav');
//    $('#app-actions').remove();
    $(".toggle-nav").removeClass('toggle-nav');
    init_demand_map();
    init_gis_map();
});


