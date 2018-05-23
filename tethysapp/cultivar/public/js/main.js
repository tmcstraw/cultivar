MONTHLY_STATS = {
    'Jan': {'daylight': 7.8, 'temperature': 77.5, 'precip': 1.2},
    'Feb': {'daylight': 7.283, 'temperature': 77, 'precip': 1.2},
    'Mar': {'daylight': 8.416, 'temperature': 78, 'precip': 1.8},
    'Apr': {'daylight': 8.496, 'temperature': 79.5, 'precip': 2.5},
    'May': {'daylight': 9.099, 'temperature': 81.0, 'precip': 6.6},
    'Jun': {'daylight': 8.94, 'temperature': 82.0, 'precip': 5.1},
    'Jul': {'daylight': 9.19, 'temperature': 83.0, 'precip': 1.5},
    'Aug': {'daylight': 8.921, 'temperature': 83.0, 'precip': 2.6},
    'Sep': {'daylight': 8.294, 'temperature': 83.0, 'precip': 5.7},
    'Oct': {'daylight': 8.204, 'temperature': 81.0, 'precip': 7.3},
    'Nov': {'daylight': 7.631, 'temperature': 80.0, 'precip': 3.0},
    'Dec': {'daylight': 7.726, 'temperature': 78.0, 'precip': 1.8}
};


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


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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
            params: {'LAYERS': 'Yaqueds'},
            serverType: 'geoserver',
            crossOrigin: 'Anonymous',





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
    var riversLayer = new ol.layer.Image({
        source: new ol.source.ImageWMS({
            url: 'http://localhost:8181/geoserver/wms',
            params: {'LAYERS': 'dr_riv',},
            serverType: 'geoserver',
            crossOrigin: 'Anonymous'


        })
    });

    var parcelLayer = new ol.layer.Image({
        source: new ol.source.ImageWMS({
            url: 'http://localhost:8181/geoserver/wms',
            params: {'LAYERS': 'parcels',},
            serverType: 'geoserver',
            crossOrigin: 'Anonymous'


        })
    });

    var otherriversLayer = new ol.layer.Image({
        source: new ol.source.ImageWMS({
            url: 'http://localhost:8181/geoserver/wms',
            params: {'LAYERS': 'other_riv',},
            serverType: 'geoserver',
            crossOrigin: 'Anonymous'


        })
    });

    function showHide (evt){

	    if($('#parcel').val()=true){
		parcelsLayer.setVisible(true);
	    }
	    if(document.getElementById("rivers").checked){
		dr_rivLayer.setVisible(true);
	    }
    }

    demandmap.addLayer(parcelLayer);
    demandmap.addLayer(riversLayer);
    demandmap.addLayer(otherriversLayer);


 }
$('#input-k').text(0.4);

$('#kValue1').on('change', function () {
        if ($('#kValue1').val() == 999) {

            k = $('#kValue2').val();
            $('#input-k').text(k);
        } else {
            k = $('#kValue1').val();
            $('#input-k').text(k);

        }
});

$('#input-k2').text(0.4);

$('#k2Value1').on('change', function () {
        if ($('#k2Value1').val() == 999) {

            k = $('#k2Value2').val();
            $('#input-k2').text(k);
        } else {
            k = $('#k2Value1').val();
            $('#input-k2').text(k);

        }
});

$('#input-k3').text(0.4);

$('#k3Value1').on('change', function () {
        if ($('#k3Value1').val() == 999) {

            k = $('#k3Value2').val();
            $('#input-k3').text(k);
        } else {
            k = $('#k3Value1').val();
            $('#input-k3').text(k);

        }
});

$('#input-k4').text(0.4);

$('#k4Value1').on('change', function () {
        if ($('#k4Value1').val() == 999) {

            k = $('#k4Value2').val();
            $('#input-k4').text(k);
        } else {
            k = $('#k4Value1').val();
            $('#input-k4').text(k);

        }
});


function calculate_demand(){
// $('#calculate_button').on('click', function () {
            hidewatermodal();
            console.log('did it');
            var area_seeded_a = parseFloat($('#area_seeded_1').val());
            var area_seeded_b = parseFloat($('#area_seeded_2').val());
            var area_seeded_c = parseFloat($('#area_seeded_3').val());
            var area_seeded_d = parseFloat($('#area_seeded_4').val());
            var k, kb, kc, kd, t, p, crop, cropb, cropc, cropd;
            var uTotal = 0;
            var uTotal_b = 0;
            var uTotal_c = 0;
            var uTotal_d = 0;

            // AGRICULTURAL CALCULATIONS
            if ($('#kValue1').val() == 999) {

                k = $('#kValue2').val();
                crop = $('#cropName').val();
            } else {
                k = $('#kValue1').val();
                crop = $('#kValue1').find(':selected').text().split(' ')[1];
            }

            $('.month').each(function (i, obj) {
                var $this = $(obj);
                if ($this.is(':checked')) {
                    t = MONTHLY_STATS[$this.val()]['temperature'];
                    p = MONTHLY_STATS[$this.val()]['daylight'];
                    z = MONTHLY_STATS[$this.val()]['precip'];
                    uTotal += (k * t * p / 100) - z;

                    if (uTotal < 0){
                        uTotal = 0
                    };
                    console.log(uTotal);
                }
            });

            // area_seeded_a is in tareas (convert to m^2)
            // uTotal is in inches (convert to m)

            var uTotalm = uTotal * 2.54 / 100;
            var area_seeded_a_sqm = area_seeded_a * 628.8;
            var totaldemand = uTotalm * area_seeded_a_sqm;
            console.log(totaldemand);

            //populate results table

            $('#crop1-name').text($('#kValue1').find(':selected').text());
            $('#crop1-area').text(Number(area_seeded_a).toFixed(2));
            $('#crop1-demand-result').text(Number(totaldemand).toFixed(2));


            if ($('#k2Value1').val() == 999) {

                kb = $('#k2Value2').val();
                cropb = $('#crop2Name').val();
                console.log(kb);
            } else {
                kb = $('#k2Value1').val();
                cropb = $('#k2Value1').find(':selected').text().split(' ')[1];
            }

            $('.month').each(function (i, obj) {
                var $this = $(obj);
                if ($this.is(':checked')) {
                    t = MONTHLY_STATS[$this.val()]['temperature'];
                    p = MONTHLY_STATS[$this.val()]['daylight'];
                    z = MONTHLY_STATS[$this.val()]['precip'];
                    uTotal_b += (kb * t * p / 100) - z;

                    if (uTotal_b < 0){
                        uTotal_b = 0};


                    console.log('got here')
                }
            });

            // area_seeded_a is in tareas (convert to m^2)
            // uTotal is in inches (convert to m)

            var uTotalm_b = uTotal_b * 2.54 / 100;
            var area_seeded_b_sqm = area_seeded_b * 628.8;
            var totaldemandb = uTotalm_b * area_seeded_b_sqm;
            console.log(totaldemandb);

            //populate results table

            $('#crop2-name').text($('#k2Value1').find(':selected').text());
            $('#crop2-area').text(Number(area_seeded_b).toFixed(2));
            $('#crop2-demand-result').text(Number(totaldemandb).toFixed(2));


            if ($('#k3Value1').val() == 999) {

                kc = $('#k3Value2').val();
                cropc = $('#crop3Name').val();
                console.log(kc);
            } else {
                kc = $('#k3Value1').val();
                cropc = $('#k3Value1').find(':selected').text().split(' ')[1];
            }

            $('.month').each(function (i, obj) {
                var $this = $(obj);
                if ($this.is(':checked')) {
                    t = MONTHLY_STATS[$this.val()]['temperature'];
                    p = MONTHLY_STATS[$this.val()]['daylight'];
                    z = MONTHLY_STATS[$this.val()]['precip'];
                    uTotal_c += (kb * t * p / 100) - z;

                    if (uTotal_c < 0){
                        uTotal_c = 0};

                    console.log('got here')
                }
            });

            // area_seeded_a is in tareas (convert to m^2)
            // uTotal is in inches (convert to m)

            var uTotalm_c = uTotal_c * 2.54 / 100;
            var area_seeded_c_sqm = area_seeded_c * 628.8;
            var totaldemandc = uTotalm_c * area_seeded_c_sqm;
            console.log(totaldemandc);

            //populate results table

            $('#crop3-name').text($('#k3Value1').find(':selected').text());
            $('#crop3-area').text(Number(area_seeded_c).toFixed(2));
            $('#crop3-demand-result').text(Number(totaldemandc).toFixed(2));


            if ($('#k4Value1').val() == 999) {

                kd = $('#k4Value2').val();
                cropc = $('#crop4Name').val();
                console.log(kc);
            } else {
                kd = $('#k4Value1').val();
                cropd = $('#k4Value1').find(':selected').text().split(' ')[1];
            }

            $('.month').each(function (i, obj) {
                var $this = $(obj);
                if ($this.is(':checked')) {
                    t = MONTHLY_STATS[$this.val()]['temperature'];
                    p = MONTHLY_STATS[$this.val()]['daylight'];
                    z = MONTHLY_STATS[$this.val()]['precip'];
                    uTotal_d += (kb * t * p / 100) - z;

                    if (uTotal_d < 0){
                        uTotal_d = 0};


                    console.log('got here')
                }
            });

            // area_seeded_a is in tareas (convert to m^2)
            // uTotal is in inches (convert to m)

            var uTotalm_d = uTotal_d * 2.54 / 100;
            var area_seeded_d_sqm = area_seeded_d * 628.8;
            var totaldemandd = uTotalm_d * area_seeded_d_sqm;
            console.log(totaldemandd);

            //populate results table

            $('#crop4-name').text($('#k4Value1').find(':selected').text());
            $('#crop4-area').text(Number(area_seeded_d).toFixed(2));
            $('#crop4-demand-result').text(Number(totaldemandd).toFixed(2));

            var total_sum_area = area_seeded_a + area_seeded_b + area_seeded_c + area_seeded_d;
            var total_sum_demand = totaldemand + totaldemandb + totaldemandc + totaldemandd;

            $('#crop5-name').text('Total:');
            $('#crop5-area').text(Number(total_sum_area).toFixed(2));
            $('#crop5-demand-result').text(Number(total_sum_demand).toFixed(2));
};

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
        center: ol.proj.transform([-71.3, 18.4], 'EPSG:4326', 'EPSG:3857'),
        minZoom: 2,
        maxZoom: 18,
        zoom:8.7
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
            params: {'LAYERS': 'parcels',},
            serverType: 'geoserver',
            crossOrigin: 'Anonymous'


        })
    });

    gismap.addLayer(wmsLayer);

    gismap.on('singleclick', function(evt) {
        var coordinate = evt.coordinate;
        var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
            coordinate, 'EPSG:3857', 'EPSG:4326'));

        content.innerHTML = '<p>Owner:</p> <code>' + hdms +
            '</code>';
        overlay.setPosition(coordinate);
      });
 }

function cropnumber(){
    $('.crop2').toggleClass('hidden', $('#select-crop-number').val() < 2);
    $('.crop3').toggleClass('hidden', $('#select-crop-number').val() < 3);
    $('.crop4').toggleClass('hidden', $('#select-crop-number').val() < 4);
}


function update_persistent_store_parcel(){

    //I need to make sure that there are values in these things
    object_id_new = $('#object-id').text();
    console.log(object_id_new)
    var dueno_new = $('#specify-dueno').val();
    var area_new = $('#specify-area').val();
    var area_planted_new = $('#specify-area-planted').val();
    var crop_1_new = $('#specify-crop-1').val();
    var area_crop_1_new = $('#specify-area-crop-1').val();
    var crop_2_new = $('#specify-crop-2').val();
    var area_crop_2_new = $('#specify-area-crop-2').val();
    var crop_3_new = $('#specify-crop-3').val();
    var area_crop_3_new = $('#specify-area-crop-3').val();

    var csrftoken = getCookie('csrftoken');
    $.ajax({
        type:'POST',
        url:'update-persistent-store-parcel/',
        data: {
            'object_id':object_id_new,
            'dueno':dueno_new,
            'area':area_new,
            'area_planted':area_planted_new,
            'crop_1':crop_1_new,
            'area_crop_1':area_crop_1_new,
            'crop_2':crop_2_new,
            'area_crop_2':area_crop_2_new,
            'crop_3':crop_3_new,
            'area_crop_3':area_crop_3_new,
        },
        headers:{'X-CSRFToken':csrftoken},
        success: function (data) {
            if (!data.error) {
                console.log("this worked");


            }
        },
    })
};

function get_default_values(){

    //I need to make sure that there are values in these things
    object_id_new = $('#object-id').text();

    console.log(object_id_new)
    var dueno_new = $('#specify-dueno').val();
    var area_new = $('#specify-area').val();
    var area_planted_new = $('#specify-area-planted').val();
    var crop_1_new = $('#specify-crop-1').val();
    var area_crop_1_new = $('#specify-area-crop-1').val();
    var crop_2_new = $('#specify-crop-2').val();
    var area_crop_2_new = $('#specify-area-crop-2').val();
    var crop_3_new = $('#specify-crop-3').val();
    var area_crop_3_new = $('#specify-area-crop-3').val();

    var csrftoken = getCookie('csrftoken');
    $.ajax({
        type:'POST',
        url:'get-default-values/',
        data: {
            'object_id':object_id_new,
            'dueno':dueno_new,
            'area':area_new,
            'area_planted':area_planted_new,
            'crop_1':crop_1_new,
            'area_crop_1':area_crop_1_new,
            'crop_2':crop_2_new,
            'area_crop_2':area_crop_2_new,
            'crop_3':crop_3_new,
            'area_crop_3':area_crop_3_new,
        },
        headers:{'X-CSRFToken':csrftoken},
        success: function (data) {
            if (!data.error) {
                console.log("this worked");


            }
        },
    })
};



function dimensionmodal() {
    $("#dimensionmod").modal('show')
}
function watermodal() {
    $("#watermod").modal('show')
    tot_area=$("#select1").find(':selected').val()

    district_name=$("#select1").find(':selected').text()
    $('#totarea').text(Number(tot_area))
    $('#district-name').text(district_name)


}
function hidedimmodal() {
    $("#dimensionmod").modal('hide')
}
function hidewatermodal() {
    $("#watermod").modal('hide')
    $("#resultmod").modal('show')
}

function hideresultmodal() {
    $("#resultmod").modal('hide')
}
function show_user_k() {
    $("#user-k-value").modal('show')
}
function hide_user_k() {
    $("#user-k-value").modal('hide')
}

function updatemodal() {
    $("#update-modal").modal('show');
    var objid=$("#lot").val();
    console.log(objid);
    $('#object-id').text(Number(objid))
}
function hideupdatemodal() {
    $("#update-modal").modal('hide')
}
function show_success() {
    $("#success-modal").modal('show')
    }


$(function(){
//    $('#app-content-wrapper').removeClass('show-nav');
//    $('#app-actions').remove();
    $(".toggle-nav").removeClass('toggle-nav');
    init_demand_map();
    get_default_values();
    init_gis_map();



});


