from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import Button, MapView, SelectInput, MVView, TextInput, TableView
import random
import string
from django.http import HttpResponse
from django.shortcuts import render
from model import get_all_parcels, Parcel
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
    select_district = SelectInput(display_text='Select an Irrigation District:',
                           name='select1',
                           multiple=False,
                           original=True,
                           options=[('Yaque Del Sur', '1'), ('Valle de San Juan', '2'), ('Lago Enriquillo', '3'), ('Azua', '4'), ('Laguna de Cabral', '5'),],
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
        'select_district': select_district
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

def test(request):

    parcel_button = Button(display_text='Update Parcel',
                                name='parcel_button',
                                style='',
                                icon='',
                                href='',
                                submit=False,
                                disabled=False,
                                attributes={"onclick": "dimensionmodal()"},
                                classes=''
                            )

    select_district = SelectInput(display_text='Select an Irrigation District:',
                           name='select1',
                           multiple=False,
                           original=True,
                           options=[('Yaque Del Sur', '1'), ('San Juan', '2'), ('Sabaneta', '3')],
                           initial=['']
                            )

    update_button = Button(display_text='Update Parcel',
                                name='update_parcels',
                                style='success',
                                icon='glyphicon glyphicon-plus',
                                href='',
                                submit=False,
                                disabled=False,
                                attributes={"onclick": "hidedimmodal()"},
                                classes=''
                            )

    parcel_data_edit = TableView(column_names=('Attribute', 'Value (ft)'),
                                rows=[('Parcel ID', 012345),
                                      ('Owner First Name', 'First Name'),
                                      ('Owner Last Name', 'Last Name'),
                                      ('Age (years)', 30),
                                      ('Gender (M/F)', 'M'),
                                      ('Area (ac)', 540),
                                      ('Purcahse Date', 'MM/DD/YYYY'),
                                      ('Area Planted (ac)', 450),
                                      ],
                                hover=True,
                                striped=True,
                                bordered=True,
                                condensed=True,
                                editable_columns=(False, 'Value (ft)'),
                                row_ids=[21, 25, 31]
                               )

    context = {
        'parcel_button': parcel_button,
        'parcel_data_edit': parcel_data_edit,
        'update_button' : update_button,
        'select_district' : select_district
    }

    return render(request, 'cultivar/test.html', context)


def demand_calculator(request):


    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    k_value_options = [('Maiz(Iniciales)', 0.4),
                                    ('Maiz(Desarollo)', 0.8),
                                    ('Maiz(Mediados)', 1.125),
                                    ('Maiz(Finales)', 1.075),
                                    ('Maiz(Recoleccion)', 0.875),
                                    ('Platano(Iniciales)', 0.45),
                                    ('Platano(Desarollo)', 0.775),
                                    ('Platano(Mediados)', 1.05),
                                    ('Platano(Finales)', 0.95),
                                    ('Platano(Recoleccion)', 0.8),
                                    ('Cana(Iniciales)', 0.6),
                                    ('Cana(Desarollo)', 0.8),
                                    ('Cana(Mediados)', 1),
                                    ('Cana(Finales)', 0.85),
                                    ('Cana(Recoleccion)', 0.75),
                                    ('Arroz(Iniciales)', 1.125),
                                    ('Arroz(Desarollo)', 1.3),
                                    ('Arroz(Mediados)', 1.2),
                                    ('Arroz(Finales)', 1),
                                    ('Arroz(Recoleccion)', 1),
                                    ('Other...(Specify)', 999)]


    select_district = SelectInput(display_text='Select an Irrigation District:',
                           name='select1',
                           multiple=False,
                           original=True,
                           options=[('Yaque Del Sur', '219114'), ('Valle de San Juan', '609024'), ('Lago Enriquillo', '413236'), ('Azua', '871546'), ('Laguna de Cabral', '700'),],
                           initial=['']
    )

    select_crop_number = SelectInput(display_text='Number of Crop Types Planted:',
                           name='select_crop_number',
                           multiple=False,
                           original=True,
                           options=[('1', 1), ('2', 2), ('3', 3),('4',4)],
                           initial=['1'],
                           attributes={'onchange': "cropnumber()"}
    )

    select_crop_type = SelectInput(display_text='Crop Type(Growth Stage):',
                           name='kValue1',
                           multiple=False,
                           original=True,
                           options=k_value_options,
                           attributes= {'onchange': "$('.user-k-value').toggleClass('hidden', this.value != 999)"}

    )


    input_k_value = TextInput(display_text='Crop K Value',
                              name='kValue2')

    input_crop_name = TextInput(display_text='Crop Type',
                                name='cropName')

    select_crop_2_type = SelectInput(display_text='Crop Type(Growth Stage):',
                           name='k2Value1',
                           multiple=False,
                           original=True,
                           options=k_value_options,
                           attributes= {'onchange': "$('.user-k-value').toggleClass('hidden', this.value != 999)"}

    )


    input_k_2_value = TextInput(display_text='Crop K Value',
                              name='k2Value2')

    input_crop_2_name = TextInput(display_text='Crop Type',
                                name='crop2Name')

    select_crop_3_type = SelectInput(display_text='Crop Type(Growth Stage):',
                           name='k3Value1',
                           multiple=False,
                           original=True,
                           options=k_value_options,
                           attributes= {'onchange': "$('.user-k-value').toggleClass('hidden', this.value != 999)"}

    )


    input_k_3_value = TextInput(display_text='Crop K Value',
                              name='k3Value2')

    input_crop_3_name = TextInput(display_text='Crop Type',
                                name='crop3Name')


    select_crop_4_type = SelectInput(display_text='Crop Type(Growth Stage):',
                           name='k4Value1',
                           multiple=False,
                           original=True,
                           options=k_value_options,
                           attributes= {'onchange': "$('.user-k-value').toggleClass('hidden', this.value != 999)"}

    )


    input_k_4_value = TextInput(display_text='Crop K Value',
                              name='k4Value2')

    input_crop_4_name = TextInput(display_text='Crop Type',
                                name='crop4Name')


    input_parameters_button = Button(
        display_text='Input Parameters',
        name='input-parameters-button',
        icon='',
        style='',
        submit=False,
        disabled=False,
        attributes={"onclick": "watermodal()"},
        classes=''
    )

    calculate_button = Button(display_text='Calculate Demand',
                                name='calculate_demand',
                                style='success',
                                icon='glyphicon',
                                href='',
                                submit=False,
                                disabled=False,
                                attributes={"onclick": "calculate_demand()"},
                                classes=''
                            )

    area_seeded_1 = TextInput(display_text='Area Seeded(tareas)',
                       name='area_seeded_1',
                       placeholder='e.g.: 10.00',
                       prepend='*')

    area_seeded_2 = TextInput(display_text='Area Seeded(tareas)',
                       name='area_seeded_2',
                       placeholder='e.g.: 10.00',
                       prepend='*')

    area_seeded_3 = TextInput(display_text='Area Seeded(tareas)',
                       name='area_seeded_3',
                       placeholder='e.g.: 10.00',
                       prepend='*')

    area_seeded_4 = TextInput(display_text='Area Seeded(tareas)',
                       name='area_seeded_4',
                       placeholder='e.g.: 10.00',
                       prepend='*')

    close_button = Button(display_text='Close',
                                name='close_button',
                                style='',
                                icon='',
                                href='',
                                submit=False,
                                disabled=False,
                                attributes={"onclick": "hideresultmodal()"},
                                classes=''
                            )

    water_results = TableView(column_names=('Crop Type', 'Area of Planted Crop (ac)', 'Total Demand for specified time period (ac-ft)'),
                                rows=[('Corn', 150, 47),
                                      ('Cocoa', 200, 58),
                                      ('Rice', 75, 35),
                                      ('Total', 425, 140),
                                      ],
                                hover=True,
                                striped=True,
                                bordered=True,
                                condensed=True,
                                editable_columns=(False, False),
                                row_ids=[21, 25, 31]
                               )



    context = {
        'input_crop_name': input_crop_name,
        'input_k_value': input_k_value,
        'input_crop_2_name': input_crop_2_name,
        'input_k_2_value': input_k_2_value,
        'input_crop_3_name': input_crop_3_name,
        'input_k_3_value': input_k_3_value,
        'input_crop_4_name': input_crop_4_name,
        'input_k_4_value': input_k_4_value,
        'k_value_options': k_value_options,
        'area_seeded_1': area_seeded_1,
        'area_seeded_2': area_seeded_2,
        'area_seeded_3': area_seeded_3,
        'area_seeded_4': area_seeded_4,
        'months': months,
        'water_results': water_results,
        'close_button': close_button,
        'calculate_button': calculate_button,
        'select_crop_type': select_crop_type,
        'select_crop_2_type': select_crop_2_type,
        'select_crop_3_type': select_crop_3_type,
        'select_crop_4_type': select_crop_4_type,
        'select_crop_number': select_crop_number,
        'input_parameters_button': input_parameters_button,
        'select_district': select_district,
    }

    return render(request, 'cultivar/demand_calculator.html', context)

def gis_data_manager(request):

    parcel_button = Button(display_text='Update Parcel',
                                name='parcel_button',
                                style='',
                                icon='',
                                href='',
                                submit=False,
                                disabled=False,
                                attributes={"onclick": "dimensionmodal()"},
                                classes=''
                            )

    select_district = SelectInput(display_text='Select an Irrigation District:',
                           name='select1',
                           multiple=False,
                           original=True,
                           options=[('Yaque Del Sur', '219114'), ('Valle de San Juan', '609024'), ('Lago Enriquillo', '413236'), ('Azua', '871546'), ('Laguna de Cabral', '700'),],
                           initial=['']
    )

    update_button = Button(display_text='Update Parcel',
                                name='update_parcels',
                                style='success',
                                icon='glyphicon glyphicon-plus',
                                href='',
                                submit=False,
                                disabled=False,
                                attributes={"onclick": "hidedimmodal()"},
                                classes=''
                            )

    parcel_data_edit = TableView(column_names=('Attribute', 'Value (ft)'),
                                rows=[('Parcel ID', 012345),
                                      ('Owner First Name', 'First Name'),
                                      ('Owner Last Name', 'Last Name'),
                                      ('Age (years)', 30),
                                      ('Gender (M/F)', 'M'),
                                      ('Area (ac)', 540),
                                      ('Purcahse Date', 'MM/DD/YYYY'),
                                      ('Area Planted (ac)', 450),
                                      ],
                                hover=True,
                                striped=True,
                                bordered=True,
                                condensed=True,
                                editable_columns=(False, 'Value (ft)'),
                                row_ids=[21, 25, 31]
                               )

    context = {
        'parcel_button': parcel_button,
        'parcel_data_edit': parcel_data_edit,
        'update_button' : update_button,
        'select_district' : select_district
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

def gistable(request):


    yaque_parcels_list = get_all_parcels()


    parcels_in_table = []
    for item in yaque_parcels_list:



        table_entry = (
            item.fid,
            item.object_id,
            item.dueno,
            item.AREA,
            item.Area_Planted,
            item.Crop_1,
            item.Area_Crop_1,
            item.Crop_2,
            item.Area_Crop_2,
            item.Crop_3,
            item.Area_Crop_3
        )
        parcels_in_table.append(table_entry)


    datatable_results = DataTableView(
        column_names=('FID', 'Object ID', 'Dueno', 'Area', 'Area Planted', 'Crop 1', 'Area Crop 1', 'Crop 2', 'Area Crop 2', 'Crop 3', 'Area Crop 3'),
        rows=parcels_in_table,
        searching=False,
        orderClasses=False,
    )

    select_district = SelectInput(display_text='Select an Irrigation District:',
                           name='select_district',
                           multiple=False,
                           original=True,
                           options=[('Yaque Del Sur', '1'), ('Valle de San Juan', '2'), ('Lago Enriquillo', '3'), ('Azua', '4'), ('Laguna de Cabral', '5'),],
                           initial=['']
    )

    specify_lot = TextInput(display_text='Type the Object ID of the lot you wish to update',
                              name='lot',
                              initial=1)

    update_button = Button(display_text='Update Parcel',
                                name='update_parcels',
                                style='success',
                                icon='glyphicon glyphicon-plus',
                                href='',
                                submit=False,
                                disabled=False,
                                attributes={"onclick": "updatemodal()"},
                                classes=''
                            )
    submit_changes_button = Button(display_text='Update Parcel',
                                name='update_parcels',
                                style='success',
                                icon='glyphicon',
                                href='',
                                submit=False,
                                disabled=False,
                                attributes={"onclick": "update_persistent_store_parcel()"},
                                classes=''
                            )

    specify_dueno = TextInput(display_text='Dueno',
                              name='specify-dueno')


    specify_area = TextInput(display_text='Area of Lot',
                              name='specify-area')

    specify_area_planted = TextInput(display_text='Area Planted in Lot',
                              name='specify-area-planted')

    specify_crop_1 = TextInput(display_text='Crop 1 Name',
                              name='specify-crop-1')

    specify_area_crop_1 = TextInput(display_text='Area planted with Crop 1',
                              name='specify-area-crop-1')

    specify_crop_2 = TextInput(display_text='Crop 2 Name',
                              name='specify-crop-2')

    specify_area_crop_2 = TextInput(display_text='Area planted with Crop 2',
                              name='specify-area-crop-2')

    specify_crop_3 = TextInput(display_text='Crop 3 Name',
                              name='specify-crop-3')

    specify_area_crop_3 = TextInput(display_text='Area planted with Crop 3',
                              name='specify-area-crop-3')

    context = {
        'datatable_results': datatable_results,
        'select_district': select_district,
        'specify_lot': specify_lot,
        'update_button': update_button,
        'submit_changes_button': submit_changes_button,
        'specify_dueno': specify_dueno,
        'specify_area': specify_area,
        'specify_area_planted': specify_area_planted,
        'specify_crop_1': specify_crop_1,
        'specify_area_crop_1': specify_area_crop_1,
        'specify_crop_2': specify_crop_2,
        'specify_area_crop_2': specify_area_crop_2,
        'specify_crop_3': specify_crop_3,
        'specify_area_crop_3': specify_area_crop_3
    }
    return render(request, 'cultivar/gistable.html', context)

def update_persistent_store_parcel(request):

    object_id_ajax = request.POST.get('object_id')
    dueno_ajax = request.POST.get('dueno')
    area_ajax = request.POST.get('area')
    area_planted_ajax = request.POST.get('area_planted')
    crop_1_ajax = request.POST.get('crop_1')
    area_crop_1_ajax = request.POST.get('area_crop_1')
    crop_2_ajax = request.POST.get('crop_2')
    area_crop_2_ajax = request.POST.get('area_crop_2')
    crop_3_ajax = request.POST.get('crop_3')
    area_crop_3_ajax = request.POST.get('area_crop_3')

    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()

    target = session.query(Parcel).filter_by(object_id=object_id_ajax).first()
    print(target)
    target.dueno = dueno_ajax
    target.AREA = area_ajax
    target.Area_Planted = area_planted_ajax
    target.Crop_1 = crop_1_ajax
    target.Area_Crop_1 = area_crop_1_ajax
    target.Crop_2 = crop_2_ajax
    target.Area_Crop_2 = area_crop_2_ajax
    target.Crop_3 = crop_3_ajax
    target.Area_Crop_3 = area_crop_3_ajax

    session.commit()
    session.close()

    return HttpResponse('Changes Made')


