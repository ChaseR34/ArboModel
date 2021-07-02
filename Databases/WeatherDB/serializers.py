from rest_framework import serializers

from .models import WeatherResults

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherResults
        fields = (
            "id",
           "rain_amount",
           "max_temp",
           # "mean_temp",
           # "min_temp",
           # "max_dewpnt",
           # "mean_dewpnt",
           # "min_dewpnt",
           # "max_humid",
           # "min_humid",
           # "max_wind",
           # "max_bar",
           # "min_bar",
           # "max_sol_rad",
           "date_recorded_id",
           "weather_station_id"
        )
