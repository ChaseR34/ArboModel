# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Counties(models.Model):
    county = models.CharField(max_length=50)

class Countries(models.Model):
    country = models.CharField(max_length=50)
    country_code = models.CharField(max_length=5)

class Dates(models.Model):
    date = models.DateField()


class LatitudeLongitude(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()



class SensorType(models.Model):
    sensor_type = models.CharField(max_length=50)


class WeatherResults(models.Model):
    rain_amount = models.FloatField(blank=True, null=True)
    max_temp = models.IntegerField(blank=True, null=True)
    mean_temp = models.IntegerField(blank=True, null=True)
    min_temp = models.IntegerField(blank=True, null=True)
    max_dewpnt = models.IntegerField(blank=True, null=True)
    mean_dewpnt = models.IntegerField(blank=True, null=True)
    min_dewpnt = models.IntegerField(blank=True, null=True)
    max_humid = models.IntegerField(blank=True, null=True)
    min_humid = models.IntegerField(blank=True, null=True)
    max_wind = models.FloatField(blank=True, null=True)
    max_bar = models.IntegerField(blank=True, null=True)
    min_bar = models.IntegerField(blank=True, null=True)
    max_sol_rad = models.IntegerField(blank=True, null=True)
    date_recorded = models.ForeignKey(Dates, models.DO_NOTHING)
    weather_station = models.ForeignKey('WeatherStations', models.DO_NOTHING)


class WeatherSensors(models.Model):
    sensor_id = models.IntegerField(unique=True)
    installed_date_sensor = models.ForeignKey(Dates, models.DO_NOTHING)
    sensor_type = models.ForeignKey(SensorType, models.DO_NOTHING)
    station = models.ForeignKey('WeatherStations', models.DO_NOTHING)


class WeatherStations(models.Model):
    name = models.CharField(max_length=100)
    station_id = models.IntegerField(unique=True)
    old_station_id = models.IntegerField(unique=True, blank=True, null=True)
    elevation = models.IntegerField()
    station_loc_description = models.TextField(blank=True, null=True)
    new_rain_id = models.IntegerField(blank=True, null=True)
    old_rain_id = models.IntegerField(blank=True, null=True)
    new_water_level_id = models.IntegerField(blank=True, null=True)
    old_water_level_id = models.IntegerField(blank=True, null=True)
    country = models.ForeignKey(Countries, models.DO_NOTHING)
    county = models.ForeignKey(Counties, models.DO_NOTHING)
    installed_date_station = models.ForeignKey(Dates, models.DO_NOTHING)
    lat_lon = models.ForeignKey(LatitudeLongitude, models.DO_NOTHING)