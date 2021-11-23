import ee
import time
import random
from time import sleep
from Databases.WeatherDB.GEE.determine_weeks import get_week_start_end

ee.Initialize()

# def transformer(a_feat):
#     return a_feat.transform('ESPG:4326', 0.001)

# folder = ee.data.getAssetRoots()[0]['id']  # maybe not the most elegant way
# assets = ee.data.listAssets({'parent': folder})
# marmap_fc = ee.FeatureCollection(assets['assets'][0]['id'])
# marmap = marmap_fc.geometry(0.001)


# def clp(img):
#     return img.clip(marmap)

weeks = get_week_start_end("2018-01-01")

for start_date, end_date in weeks:
    era5_tp = ee.ImageCollection('ECMWF/ERA5/DAILY').select('total_precipitation').filter(
        ee.Filter.date(start_date, end_date))

    era5_2mt = ee.ImageCollection('ECMWF/ERA5/DAILY').select('mean_2m_air_temperature').filter(
        ee.Filter.date(start_date, end_date))
    era5_2d = ee.ImageCollection('ECMWF/ERA5/DAILY').select('dewpoint_2m_temperature').filter(
        ee.Filter.date(start_date, end_date))
    era5_mslp = ee.ImageCollection('ECMWF/ERA5/DAILY').select('mean_sea_level_pressure').filter(
        ee.Filter.date(start_date, end_date))
    era5_sp = ee.ImageCollection('ECMWF/ERA5/DAILY').select('surface_pressure').filter(
        ee.Filter.date(start_date, end_date))
    era5_u_wind_10m = ee.ImageCollection('ECMWF/ERA5/DAILY').select('u_component_of_wind_10m').filter(
        ee.Filter.date(start_date, end_date))

    #
    # era5_tp_clip = era5_tp.map(clp)
    # print(era5_tp_clip.getInfo())
    era5_tp_mean = era5_tp.sum()
    era5_2mt_mean = era5_2mt.mean()
    era5_2d_mean = era5_2d.mean()
    era5_mslp_mean = era5_mslp.mean()
    era5_sp_mean = era5_sp.mean()
    era5_u_wind_10m_mean = era5_u_wind_10m.mean()

    # print(ee.Element.geometry(era5_tp_clip_mean).getInfo())

    task_tp = ee.batch.Export.image.toDrive(image=era5_tp_mean.visualize(min=0,
                                                                         max=0.1,
                                                                         palette=['#FFFFFF', '#00FFFF', '#0080FF',
                                                                                  '#DA00FF', '#FFA400', '#FF0000']),
                                            description=f'tp_era5_whole_earth_{start_date}',
                                            folder='total_precipitation',
                                            fileFormat='GeoTIFF',
                                            dimensions="1440x721")

    task_2mt = ee.batch.Export.image.toDrive(image=era5_2mt_mean.visualize(min=250,
                                                                           max=320,
                                                                           palette=[
                                                                               '#000080', '#0000D9', '#4000FF',
                                                                               '#8000FF',
                                                                               '#0080FF', '#00FFFF', '#00FF80',
                                                                               '#80FF00', '#DAFF00', '#FFFF00',
                                                                               '#FFF500',
                                                                               '#FFDA00', '#FFB000', '#FFA400',
                                                                               '#FF4F00', '#FF2500', '#FF0A00',
                                                                               '#FF00FF'
                                                                           ]),
                                             description=f'2mt_era5_whole_earth_{start_date}',
                                             folder='mean_2m_air_temperature',
                                             fileFormat='GeoTIFF',
                                             dimensions="1440x721")
    task_2d = ee.batch.Export.image.toDrive(image=era5_2d_mean.visualize(min=250,
                                                                         max=320,
                                                                         palette=[
                                                                             '#000080', '#0000D9', '#4000FF', '#8000FF',
                                                                             '#0080FF', '#00FFFF', '#00FF80',
                                                                             '#80FF00', '#DAFF00', '#FFFF00', '#FFF500',
                                                                             '#FFDA00', '#FFB000', '#FFA400',
                                                                             '#FF4F00', '#FF2500', '#FF0A00', '#FF00FF'
                                                                         ]),
                                            description=f'2d_era5_whole_earth_{start_date}',
                                            folder='mean_2m_dewpoint_temperature',
                                            fileFormat='GeoTIFF',
                                            dimensions="1440x721")
    task_mslp = ee.batch.Export.image.toDrive(image=era5_mslp_mean.visualize(min=990,
                                                                             max=1050,
                                                                             palette=[
                                                                                 '#01FFFF', '#058BFF', '#0600FF',
                                                                                 '#DF00FF',
                                                                                 '#FF00FF', '#FF8C00', '#FF8C00'
                                                                             ]),
                                              description=f'mslp_era5_whole_earth_{start_date}',
                                              folder='mean_sea_level_pressure',
                                              fileFormat='GeoTIFF',
                                              dimensions="1440x721")
    task_sp = ee.batch.Export.image.toDrive(image=era5_sp_mean.visualize(min=500,
                                                                         max=1150,
                                                                         palette=[
                                                                             '#01FFFF', '#058BFF', '#0600FF', '#DF00FF',
                                                                             '#FF00FF', '#FF8C00', '#FF8C00'
                                                                         ]),
                                            description=f'sp_era5_whole_earth_{start_date}',
                                            folder='mean_surface_pressure',
                                            fileFormat='GeoTIFF',
                                            dimensions="1440x721")
    task_u_wind_10m = ee.batch.Export.image.toDrive(image=era5_u_wind_10m_mean.visualize(min=0,
                                                                                         max=30,
                                                                                         palette=[
                                                                                             '#01FFFF', '#058BFF',
                                                                                             '#0600FF', '#DF00FF',
                                                                                             '#FF00FF', '#FF8C00',
                                                                                             '#FF8C00'
                                                                                         ]),
                                                    description=f'wind_era5_whole_earth_{start_date}',
                                                    folder='wind',
                                                    fileFormat='GeoTIFF',
                                                    dimensions="1440x721")

    task_tp.start()
    task_2mt.start()
    task_2d.start()
    task_mslp.start()
    task_sp.start()
    task_u_wind_10m.start()
    print(f"current date: {start_date}")
    sleep_time = random.randint(1, 5)
    print(f"sleeping for {sleep_time}")
    time.sleep(sleep_time)

# start = task.start()
# status = task.status()['state']
# print(status)
# while status != 'COMPLETED':
#     sleep(2)
#     status = task.status()['state']
# print(task.status())
