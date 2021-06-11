import re

import requests
import openpyxl
from pdfreader import PDFDocument, SimplePDFViewer
from geopy.geocoders import Nominatim
import os
import errno
import datetime

import django
from django.core import exceptions

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ArboModelData.settings')

django.setup()
from Databases.WeatherDB.models import Dates, WeatherStations, WeatherSensors, WeatherResults

def is_date(string, format="%m/%d/%y"):
    """

    :param string:
    :param format:
    :return:
    """
    try:
        datetime.datetime.strptime(string, format)
        return True

    except ValueError:
        return False



class FileNotOpened(Exception):

    def __init__(self, pdf_file_path):
        self.file = pdf_file_path

    def __str__(self):
        return f'the file, {self.file}, was not opened. Please open the file'

class FilePathNotAssigned(Exception):

    def __str__(self):
        return f'No file path given. Please set a filepath'



class MaricopaWeatherData:
    def __int__(self):
        self.pdf_filepath = ""
        self.pdf_file = ""
        self.num_pages = 0
        self.is_file_open = False

    def set_filepath(self, filepath):
        self.pdf_filepath = filepath

    def open_pdf_file(self):
        """
            Opens the final saved in self.pdf_file
            Checks if file was opened
            sets value of self.num_pages by calling self.get_num_pages()
        :return: boolean` true if file was opened, false otherwise
        """
        try:

            self.pdf_file = open(self.pdf_filepath, 'rb')
            self.is_file_open = True
            self.num_pages = self.get_num_pages()
            return True
        except FileNotFoundError:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.pdf_filepath)
        except AttributeError:
            raise FilePathNotAssigned

    def close_pdf_file(self):
        try:
            if not os.path.isfile(self.pdf_filepath):
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.pdf_filepath)
        except AttributeError:
            raise FilePathNotAssigned
        try:
            self.pdf_file.close()
        except AttributeError:
            raise FileNotOpened(self.pdf_filepath)

    def download_weather_pdf(self, pdf_url, pdf_output_file):

        r = requests.get(pdf_url, stream = True)

        if r.ok:
            with open(pdf_output_file, 'wb') as fd:
                fd.write(r.content)
        else:
            r.raise_for_status()

    def get_num_pages(self):
        pdf = PDFDocument(self.pdf_file)

        all_pages = [p for p in pdf.pages()]
        num_pages = len(all_pages)
        return num_pages

    def parse_sensor_pdf(self):

        pdf_viewer = SimplePDFViewer(self.pdf_file)

        for page in range(1, self.num_pages + 1):

            offset = 0
            num_of_columns = 0
            found_pointid = False

            pdf_viewer.navigate(page)
            pdf_viewer.render()

            text = "".join(pdf_viewer.canvas.strings)
            text_list = text.split()

            while text_list[offset+num_of_columns].lower().strip() != "stattype":

                if text_list[offset+num_of_columns].lower().strip() == "pointid" or  text_list[offset+num_of_columns].lower().strip() == "deviceid":
                    found_pointid = True


                if not found_pointid:
                    offset += 1

                else:

                    num_of_columns += 1


            i=offset


            header = " ".join(text_list[0:offset])
            # print(header)
            regex_match = re.search(r"g[0-9]+:(.*)(weather|fire|statistics)", header.strip().lower())
            station_name = re.sub(r"(weather|station)", "",regex_match.group(1)).strip().replace('.','')
            # print(station_name)
            try:
                weather_station = WeatherStations.objects.using('WeatherDB').get(name=station_name)
            except:
                if station_name == 'camelback @ citrus':
                    weather_station = WeatherStations.objects.using('WeatherDB').get(name='camelback rd @ citrus rd')
                elif station_name == 'fountain hills fire':
                    weather_station = WeatherStations.objects.using('WeatherDB').get(name='fountain hills fire dept')
                elif station_name == 'osborn @ 64th st':
                    weather_station = WeatherStations.objects.using('WeatherDB').get(name='osborn rd @ 64th st')
                elif station_name == 'pima @ jomax':
                    weather_station = WeatherStations.objects.using('WeatherDB').get(name='pima rd @ jomax rd')
                elif station_name == 'usery mtn park':
                    weather_station = WeatherStations.objects.using('WeatherDB').get(name='usery mountain park')
                elif station_name == "upper sycamore creek" or station_name == "sycamore creek upper":
                    weather_station = WeatherStations.objects.using('WeatherDB').get(name='sycamore creek - upper')
                else:
                    print(station_name)

            while i < len(text_list) and found_pointid:
                max_temp    = None
                mean_temp   = None
                min_temp    = None
                max_dewpnt  = None
                mean_dewpnt = None
                min_dewpnt  = None
                max_humid   = None
                min_humid   = None
                max_wind    = None
                max_bar     = None
                min_bar     = None
                max_sol_rad = None

                units_dict = {
                    "max_temp": max_temp,
                    "mean_temp": mean_temp,
                    "min_temp": min_temp,
                    "max_dewpnt": max_dewpnt,
                    "mean_dewpnt": mean_dewpnt,
                    "min_dewpnt": min_dewpnt,
                    "max_rhumid": max_humid,
                    "min_rhumid": min_humid,
                    "max_pkwind": max_wind,
                    "max_baropr": max_bar,
                    "min_baropr": min_bar,
                    "max_solrad": max_sol_rad
                }




                if text_list[i].lower().strip() == "stattype":
                    statype = text_list[i+1:i+num_of_columns]

                elif text_list[i].lower().strip() == "datatype":
                    datatype = text_list[i+1:i+num_of_columns]

                elif text_list[i].lower().strip() == "units":
                    sensors_used = []
                    for t in zip(statype, datatype):
                        sensors_used.append("_".join(t))
                elif text_list[i].lower().strip().replace(':','') == "totals":
                    found_pointid = False
                elif is_date(text_list[i]):

                    date_measured = datetime.datetime.strptime(text_list[i], "%m/%d/%y")

                    dates_obj, dates_obj_created = Dates.objects.using('WeatherDB').get_or_create(date=date_measured)

                    if dates_obj_created:
                        dates_obj.save()

                    for index in enumerate(sensors_used):
                        try:
                            units_dict[index[1]] = float(text_list[i+1+index[0]])

                        except ValueError:

                            units_dict[index[1]] = None


                    weather_results, weather_results_created = WeatherResults.objects.using('WeatherDB').get_or_create(
                        weather_station=weather_station,
                        date_recorded=dates_obj
                    )

                    weather_results.max_temp=units_dict["max_temp"]
                    weather_results.mean_temp=units_dict["mean_temp"]
                    weather_results.min_temp=units_dict["min_temp"]
                    weather_results.max_dewpnt=units_dict["max_dewpnt"]
                    weather_results.mean_dewpnt=units_dict["mean_dewpnt"]
                    weather_results.min_dewpnt=units_dict["min_dewpnt"]
                    weather_results.max_humid=units_dict["max_rhumid"]
                    weather_results.min_humid=units_dict["min_rhumid"]
                    weather_results.max_wind=units_dict["max_pkwind"]
                    weather_results.max_bar=units_dict["max_baropr"]
                    weather_results.min_bar=units_dict["min_baropr"]
                    weather_results.max_sol_rad=units_dict["max_solrad"]

                    weather_results.save()



                i+=num_of_columns

    def parse_rain_pdf(self):

        pdf_viewer = SimplePDFViewer(self.pdf_file)

        for page in range(1, self.num_pages + 1):

            offset = 0
            num_of_columns = 0
            found_pointid = False

            pdf_viewer.navigate(page)
            pdf_viewer.render()

            text = "".join(pdf_viewer.canvas.strings)
            text_list = text.split()

            while text_list[offset+num_of_columns].lower().strip() != "daily":

                if text_list[offset+num_of_columns].lower().strip() == "pointid" or text_list[offset+num_of_columns].lower().strip() == "id" :
                    found_pointid = True


                if not found_pointid:
                    offset += 1

                else:

                    num_of_columns += 1


            i=offset
            rain_sensors = text_list[i+1:i + num_of_columns]
            while i < len(text_list):

                # if text_list[i].lower().strip() == "pointid" or text_list[offset+num_of_columns].lower().strip() == "id":
                #     print("inside if")
                #     rain_sensors = text_list[i:i+num_of_columns]

                if is_date(text_list[i].lower().strip()):

                    date_measured = datetime.datetime.strptime(text_list[i], "%m/%d/%y")
                    i += 1

                    for sen in rain_sensors:
                        success = False
                        try:
                            weather_station = WeatherStations.objects.using('WeatherDB').get(old_rain_id=int(sen))
                            success = True

                        except exceptions.ObjectDoesNotExist:
                            try:
                                weather_station = WeatherStations.objects.using('WeatherDB').get(new_rain_id=int(sen))
                                success = True
                            except exceptions.ObjectDoesNotExist:
                                print(f"{sen} does not exist")


                        date_obj, date_obj_created = Dates.objects.using('WeatherDB').get_or_create(date=date_measured)

                        if date_obj_created:
                            date_obj.save()




                        weather_result, weather_result_created = WeatherResults.objects.using('WeatherDB').get_or_create(
                                                                    weather_station=weather_station,
                                                                    date_recorded=date_obj
                                                                    )

                        try:
                            weather_result.rain_amount = float(text_list[i])
                        except ValueError:
                            weather_result.rain_amount = None
                        finally:
                            weather_result.save()


                        i+=1
                else:
                    i+=1

if __name__ == '__main__':
    maricopa = MaricopaWeatherData()
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    years = ['12','13','14','15','16','17','18','19','20']

    for year in years:
        for month in months:

            try:
                print(f"starting: ws{month}{year}")
                maricopa.download_weather_pdf(pdf_url=f"http://alert.fcd.maricopa.gov/alert/Wx/ws{month}{year}.pdf",
                                          pdf_output_file=f"/home/chase/DissertationProjects/ArboModel/ArboModelData/Databases/WeatherDB/Weather_Data_Scraping/WS_PDFS/ws{month}{year}.pdf")

                maricopa.set_filepath(f"/home/chase/DissertationProjects/ArboModel/ArboModelData/Databases/WeatherDB/Weather_Data_Scraping/WS_PDFS/ws{month}{year}.pdf")
                maricopa.open_pdf_file()
                maricopa.parse_sensor_pdf()
                maricopa.close_pdf_file()
            except:
                print("########################### download failed ###############################")
                print(f"ws{month}{year}")

            try:
                print(f"starting: pcp{month}{year}")
                maricopa.download_weather_pdf(pdf_url=f"http://alert.fcd.maricopa.gov/alert/Rain/pcp{month}{year}.pdf",
                                              pdf_output_file=f"/home/chase/DissertationProjects/ArboModel/ArboModelData/Databases/WeatherDB/Weather_Data_Scraping/Rain_PDFS/pcp{month}{year}.pdf")
                maricopa.set_filepath(
                    f"/home/chase/DissertationProjects/ArboModel/ArboModelData/Databases/WeatherDB/Weather_Data_Scraping/Rain_PDFS/pcp{month}{year}.pdf")
                maricopa.open_pdf_file()
                maricopa.parse_rain_pdf()
                maricopa.close_pdf_file()

            except:
                print("########################### download failed ###############################")
                print(f"pcp{month}{year}")

