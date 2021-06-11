from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class Location(models.Model):
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    Country = models.CharField(null=True, max_length=50)
    State = models.CharField(null=True, max_length=50)
    County = models.CharField(null=True, max_length=50)
    Subcounty = models.CharField(null=True, max_length=50)
    City = models.CharField(null=True, max_length=50)
    District = models.IntegerField(null=True)
    class Meta:
        managed = False
        db_table='MosDB_location'

    def __str__(self):
        return f'{self.Country} and {self.State} and {self.County}'


class TrapID(models.Model):
    trapID = models.CharField(unique=True, max_length=105)

    def __str__(self):
        return f'{self.trapID}'

    class Meta:
        managed = False
        db_table = 'MosDB_trapid'


class MetaData(models.Model):
    entered_date = models.DateField()
    location = models.ForeignKey(
        'Location',
        on_delete=models.CASCADE)

    trap = models.ForeignKey(
        'TrapID',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.entered_date} {self.trap}'

    class Meta:
        managed = False
        db_table = 'MosDB_metadata'

class MosSpecies(models.Model):
    mosSpec = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.mosSpec}'
    class Meta:
        managed = False
        db_table = 'MosDB_mosspecies'

class MosCount(models.Model):
    mospec = models.ForeignKey(
        'MosSpecies',
        on_delete=models.CASCADE)
    metaData = models.ForeignKey(
        'MetaData',
        on_delete=models.CASCADE)

    males = models.IntegerField(default=0)
    females = models.IntegerField(default=0)

    def __str__(self):
        return f'Males: {self.males} and Femals:{self.females}'
    class Meta:
        managed = False
        db_table = 'MosDB_moscount'

class Virus(models.Model):
    virus = models.CharField(max_length=10)
    class Meta:
        managed = False

class Pool(models.Model):
    metaData = models.ForeignKey(
        'MetaData',
        on_delete=models.CASCADE)
    mos_spec = models.ForeignKey(
        'MosSpecies',
        on_delete=models.CASCADE)

    sequenced = models.ForeignKey(
        'Sequenced',
        on_delete=models.CASCADE)

    virus = models.ForeignKey(
        'Virus',
        on_delete=models.CASCADE)
    genome = models.ForeignKey('Genome',
                               null=True,
                               on_delete=models.SET_NULL
                               )

    SampleID = models.CharField(max_length=10)
    accession = models.CharField(max_length=10)

    positive = models.IntegerField(default=0)
    pool_num = models.IntegerField(default=0)
    num_female_mos = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.positive} {self.virus} {self.SampleID}'

    class Meta:
        managed = False
        db_table = 'MosDB_virus'

class Sequenced(models.Model):
    sequenced = models.CharField(default='No', max_length=25)
    # date_sequenced = models.DateField(null = True)
    # sequencing_type = models.CharField(null = True,max_length = 25)
    # sequencing_kit = models.CharField(null = True,max_length = 25)
    # number_of_samples_sequenced = models.IntegerField(default = 0)
    # sequencing_location = models.CharField(null = True ,max_length = 25)
    class Meta:
        managed = False
        db_table = 'MosDB_sequenced'

class Genome(models.Model):
    genome_raw = models.CharField(max_length=12000, null=True)
    genome_ORF = models.CharField(max_length=12000, null=True)

    class Meta:
        managed = False
        db_table = 'MosDB_genome'

########### Public Genome Model ###########

class PublicGenomes(models.Model):
    accession = models.CharField(max_length=25, unique=True)
    size = models.IntegerField(default=0)
    start_ORF = models.IntegerField(default=0)
    end_ORF = models.IntegerField(default=0)
    collection_date = models.DateField(null=True)
    genotype = models.IntegerField(null=True)

    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True)
    genome = models.ForeignKey(
        'Genome',
        on_delete=models.SET_NULL,
        null=True
        )
    host = models.ForeignKey(
        'MosSpecies',
        on_delete=models.SET_NULL,
        null=True)
    virus = models.ForeignKey(
        'Virus',
        on_delete=models.SET_NULL,
        null=True)
    class Meta:
        managed = False
        db_table = 'MosDB_publicgenomes'

# class SampleResult(models.Model):
#    metaData = models.ForeignKey(
##            'MetaData',
#            on_delete = models.CASCADE)
#    mos_spec = models.ForeignKey(
#            'MosSpecies',
#            on_delete=models.CASCADE)
#
#    test_date = models.DateField(null = True)
#
#
#    def __str__(self):
#       return f'{self.metaData} and {self.mos_spec}'




################################################################ California ###########################################################################################

class California(models.Model):
    agency_code = models.CharField(null=True, max_length=200)
    agency_collection_num = models.IntegerField(default=0)
    collection_id = models.IntegerField(default=0)


    meta_data = models.ForeignKey(
        'MetaData',
        on_delete=models.CASCADE)
    species = models.ForeignKey(
        'MosSpecies',
        on_delete=models.CASCADE)

    site_name = models.CharField(null=True, max_length=200)
    identified_by = models.CharField(null=True, max_length=200)
    trap_type = models.CharField(null=True, max_length=200)
    lure = models.CharField(null=True, max_length=200)
    num_trap = models.IntegerField(default=0)
    trap_nights = models.IntegerField(default=0)
    trap_problem = models.CharField(null=True, max_length=200)
    comments = models.CharField(null=True, max_length=500)

    females_unfed = models.IntegerField(null=True)
    males = models.IntegerField(null=True)
    females_gravid = models.IntegerField(null=True)
    females_bloodfed = models.IntegerField(null=True)
    females_mixed = models.IntegerField(null=True)
    larvae = models.IntegerField(null=True)

    def __str__(self):
        return f'agency_num: {self.agency_collection_num} site_name: {self.site_name}'

    class Meta:
        managed = False
        db_table = 'MosDB_california'

class California_Positives(models.Model):

    wk = models.IntegerField()

    pool = models.ForeignKey(
        'Pool',
        on_delete=models.CASCADE)

    california = models.ForeignKey(
        'California',
        on_delete=models.CASCADE)

    trap_style = models.CharField(max_length=200)

    def __str__(self):
        return f'week: {self.wk} trap_style: {self.trap_style}'

    class Meta:
        managed = False
        db_table = 'MosDB_positives'
