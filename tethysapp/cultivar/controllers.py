from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import Button, MapView, SelectInput, MVView
import random
import string

from django.shortcuts import render

from tethys_sdk.gizmos import *
from .app import Cultivar as app


WORKSPACE = 'cultivar'
GEOSERVER_URI = 'http://www.example.com/geoserver-app'



@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    # Retrieve a geoserver engine
    geoserver_engine = app.get_spatial_dataset_service(name='main_geoserver', as_engine=True)

    # Check for workspace and create workspace for app if it doesn't exist
    response = geoserver_engine.list_workspaces()

    if response['success']:
        workspaces = response['result']

        if WORKSPACE not in workspaces:
            geoserver_engine.create_workspace(workspace_id=WORKSPACE, uri=GEOSERVER_URI)




    view_options = MVView(
    projection='EPSG:4326',
    center=[-70.16, 18.83],
    zoom=8,
    maxZoom=18,
    minZoom=2
)
    cultivar_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        view=view_options,
        basemap=view_options,
    )
    select_input = SelectInput(display_text='Select an Irrigation District:',
                           name='select1',
                           multiple=False,
                           original=True,
                           options=[('Yaque Del Sur', '1'), ('San Juan', '2'), ('Sabaneta', '3')],
                           initial=['']
    )

    select_district_button = Button(
        display_text='Select',
        name='select-district-button',
        icon='glyphicon glyphicon-plus',
        style='success'
    )

    add_district_button = Button(
        display_text='Add District',
        name='add-district-button',
        icon='glyphicon glyphicon-plus',
        style='success'
    )

    context = {
        'cultivar_map': cultivar_map,
        'select_district_button': select_district_button,
        'add_district_button': add_district_button,
        'select_input': select_input
    }

    return render(request, 'cultivar/home.html', context)

@login_required()
def add_district(request):
    "Controller for Add-District Page"

    # Case where the form has been submitted
    if request.POST and 'submit' in request.POST:
        # Verify files are included with the form
        if request.FILES and 'files' in request.FILES:
            # Get a list of the files
            file_list = request.FILES.getlist('files')

            # Upload shapefile
            store = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
            store_id = WORKSPACE + ':' + store
            geoserver_engine.create_shapefile_resource(
                store_id=store_id,
                shapefile_upload=file_list,
                overwrite=True
            )

    add_district_button = Button(
        display_text='Add District',
        name='add-district-button',
        icon='glyphicon glyphicon-plus',
        style='success',
    )

    context = {
        'add_district_button': add_district_button

    }

    return render(request, 'cultivar/add_district.html', context)

@login_required
def map(request):
    """
    Controller for the map page
    """
    geoserver_engine = app.get_spatial_dataset_service(name='main_geoserver', as_engine=True)

    options = []

    response = geoserver_engine.list_layers(with_properties=False)

    if response['success']:
        for layer in response['result']:
            options.append((layer.title(), layer))

    select_options = SelectInput(
        display_text='Choose Layer',
        name='layer',
        multiple=False,
        options=options
    )

    map_layers = []

    if request.POST and 'layer' in request.POST:
        selected_layer = request.POST['layer']
        legend_title = selected_layer.title()

        geoserver_layer = MVLayer(
            source='ImageWMS',
            options={
                'url': 'http://localhost:8181/geoserver/wms',
                'params': {'LAYERS': selected_layer},
                'serverType': 'geoserver'
            },
            legend_title=legend_title,
            legend_extent=[-114, 36.5, -109, 42.5],
            legend_classes=[
                MVLegendClass('polygon', 'County', fill='#999999'),
        ])

        map_layers.append(geoserver_layer)



    view_options = MVView(
        projection='EPSG:4326',
        center=[-100, 40],
        zoom=4,
        maxZoom=18,
        minZoom=2
    )

    map_options = MapView(
        height='500px',
        width='100%',
        layers=map_layers,
        legend=True,
        view=view_options
    )

    context = {'map_options': map_options,
               'select_options': select_options}

    return render(request, 'cultivar/map.html', context)

def testmap(request):



    select_input = SelectInput(display_text='Select an Irrigation District:',
                           name='select1',
                           multiple=False,
                           original=True,
                           options=[('Yaque Del Sur', '1'), ('San Juan', '2'), ('Sabaneta', '3')],
                           initial=['']
    )

    select_district_button = Button(
        display_text='Select',
        name='select-district-button',
        icon='glyphicon glyphicon-plus',
        style='success'
    )

    add_district_button = Button(
        display_text='Add District',
        name='add-district-button',
        icon='glyphicon glyphicon-plus',
        style='success'
    )

    context = {

        'select_district_button': select_district_button,
        'add_district_button': add_district_button,
        'select_input': select_input
    }

    return render(request, 'cultivar/testmap.html', context)

def demand_calculator(request):

    select_input = SelectInput(display_text='Select an Irrigation District:',
                           name='select1',
                           multiple=False,
                           original=True,
                           options=[('Yaque Del Sur', '1'), ('San Juan', '2'), ('Sabaneta', '3')],
                           initial=['']
    )

    select_district_button = Button(
        display_text='Select',
        name='select-district-button',
        icon='glyphicon glyphicon-plus',
        style='success'
    )

    add_district_button = Button(
        display_text='Add District',
        name='add-district-button',
        icon='glyphicon glyphicon-plus',
        style='success'
    )

    context = {

        'select_district_button': select_district_button,
        'add_district_button': add_district_button,
        'select_input': select_input
    }

    return render(request, 'cultivar/demand_calculator.html', context)

def gis_data_manager(request):

    select_input = SelectInput(display_text='Select an Irrigation District:',
                           name='select1',
                           multiple=False,
                           original=True,
                           options=[('Yaque Del Sur', '1'), ('San Juan', '2'), ('Sabaneta', '3')],
                           initial=['']
    )

    select_district_button = Button(
        display_text='Select',
        name='select-district-button',
        icon='glyphicon glyphicon-plus',
        style='success'
    )

    add_district_button = Button(
        display_text='Add District',
        name='add-district-button',
        icon='glyphicon glyphicon-plus',
        style='success'
    )

    context = {

        'select_district_button': select_district_button,
        'add_district_button': add_district_button,
        'select_input': select_input
    }

    return render(request, 'cultivar/gis_data_manager.html', context)

@login_required()
def manage_districts(request):
    "Controller for Add-District Page"

    # Case where the form has been submitted
    if request.POST and 'submit' in request.POST:
        # Verify files are included with the form
        if request.FILES and 'files' in request.FILES:
            # Get a list of the files
            file_list = request.FILES.getlist('files')

            # Upload shapefile
            store = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
            store_id = WORKSPACE + ':' + store
            geoserver_engine.create_shapefile_resource(
                store_id=store_id,
                shapefile_upload=file_list,
                overwrite=True
            )

    context = {}

    return render(request, 'cultivar/manage_districts.html', context)
