# coding=UTF-8

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

import httplib2, datetime, re
from xml.etree.ElementTree import fromstring

NAME_TYPES = (
    ( u'A', _(u'accepted') ), # scientific
    ( u'S', _(u'synonym') ),  # scientific
    ( u'P', _(u'popular') ),  # vernacular
)

MONTHS = (
    ( 1 , _(u'january') ),
    ( 2 , _(u'february') ),
    ( 3 , _(u'march') ),
    ( 4 , _(u'april') ),
    ( 5 , _(u'may') ),
    ( 6 , _(u'june') ),
    ( 7 , _(u'july') ),
    ( 8 , _(u'august') ),
    ( 9 , _(u'september') ),
    ( 10, _(u'october') ),
    ( 11, _(u'november') ),
    ( 12, _(u'december') )
)

COLORS = (
    ( 1 , _(u'white') ),
    ( 2 , _(u'cream') ),
    ( 3 , _(u'yellow') ),
    ( 4 , _(u'pink') ),
    ( 5 , _(u'orange') ),
    ( 6 , _(u'red') ),
    ( 7 , _(u'green') ),
    ( 8 , _(u'purple') ),
)

FRUIT_TYPES = (
    ( u'B', _(u'Berry') ),
    ( u'C', _(u'Capsule') ),
    ( u'D', _(u'Drupe') ),
    ( u'L', _(u'Legume') ),
)

ROOT_SYSTEMS = (
    ( u'F', _(u'Fibrous') ),
    ( u'T', _(u'Taproot') ),
)

CROWN_SHAPES = (
    ( u'S', _(u'Spherical') ),
    ( u'E', _(u'Elliptical') ),
    ( u'C', _(u'Conical') ),
    ( u'L', _(u'Cylindrical') ),
    ( u'Y', _(u'Corymbiform') ),
    ( u'U', _(u'Umbelliform') ),
    ( u'F', _(u'Flabelliform') ),
    ( u'P', _(u'Pendant') ),
    ( u'I', _(u'Irregular') ),
)

BARK_TEXTURES = (
    ( u'S', _(u'Smooth') ),
    ( u'C', _(u'Cracked') ),
    ( u'R', _(u'Rough') ),
)

SEED_TYPES = (
    ( u'R', _(u'Recalcitrant') ),
    ( u'O', _(u'Orthodox') ),
)

PREGERMINATION_TREATMENTS = (
    ( u'N', _(u'No treatment') ),
    ( u'C', _(u'Chemical scarification') ),
    ( u'I', _(u'Immersion in hot or cold water') ),
    ( u'M', _(u'Mechanical scarification') ),
)

SOIL_TYPES = (
    ( u'F', _(u'wetland (frequent floods)') ),
    ( u'U', _(u'wetland (unfrequent floods)') ),
    ( u'M', _(u'marsh') ),
    ( u'D', _(u'dry and rocky') ),
    ( u'A', _(u'wet or dry') ),
)

LIGHT_REQUIREMENTS = (
    ( u'S', _(u'Shadow tolerant') ),
    ( u'U', _(u'Full sun') ),
)

TAXON_DATA = (
    ( u'RAR', _(u'Rarity') ),
    ( u'END', _(u'Endemic') ),
    ( u'SPE', _(u'Special features') ),
    ( u'SUG', _(u'Successional group') ),
    ( u'GRO', _(u'Growth rate') ),
    ( u'PRU', _(u'Pruning') ),
    ( u'FLP', _(u'Flowering period') ),
    ( u'FLC', _(u'Flowering color') ),
    ( u'POL', _(u'Pollinators') ),
    ( u'SED', _(u'Seed dispersal') ),
    ( u'DIS', _(u'Dispersers') ),
    ( u'FRT', _(u'Fruit type') ),
    ( u'SYM', _(u'Symbiotic association') ),
    ( u'ROT', _(u'Root system') ),
    ( u'FOL', _(u'Foliage persistence') ),
    ( u'CRD', _(u'Crown diameter') ),
    ( u'CRS', _(u'Crown shape') ),
    ( u'BRT', _(u'Bark texture') ),
    ( u'TRA', _(u'Trunk alignment') ),
    ( u'SIZ', _(u'Tree size') ),
    ( u'TOS', _(u'Thorns or spines') ),
    ( u'TOA', _(u'Toxic or allergenic') ),
    ( u'PAD', _(u'Pests and diseases') ),
    ( u'FRP', _(u'Fruiting period') ),
    ( u'SEC', _(u'Seed collection') ),
    ( u'SET', _(u'Seed type') ),
    ( u'PGT', _(u'Pre-germination treatment') ),
    ( u'SDL', _(u'Seedling production') ),
    ( u'GET', _(u'Germination time lapse') ),
    ( u'GER', _(u'Germination rate') ),
    ( u'LIG', _(u'Light requirements') ),
    ( u'USE', _(u'Use') ),
)

class Page( models.Model ):
    "Custom flat page"
    code = models.SlugField( _(u'Code'), help_text=_(u'Unique code to identify the page'), db_index=True )
    lang = models.CharField( _(u'Language'), choices=settings.LANGUAGES, max_length=12 )
    title = models.TextField( _(u'Title') )
    content = models.TextField( _(u'Content') )

    class Meta:
        verbose_name = _(u'page')
        verbose_name_plural = _(u'pages')
        unique_together = ((u'code', u'lang'),)
        ordering = [u'title']

    def __unicode__(self):
        return unicode(self.title)

class Reference( models.Model ):
    "Bibliographic reference"
    citation = models.TextField( _(u'Citation'), help_text=_(u'e.g. Paranagua et al. 2011'), unique=True )
    full = models.TextField( _(u'Full reference'), help_text=_(u'e.g. Paranagua, P. 2011. Building cool systems for native plants. Cool Journal, 123(4): 1-10') )

    class Meta:
        verbose_name = _(u'bibliographic reference')
        verbose_name_plural = _(u'bibliographic references')
        ordering = [u'citation']

    def __unicode__(self):
        return unicode(self.citation)

class TypeOfUse( models.Model ):
    "Types of use of a taxon"
    label = models.TextField( _(u'Label'), unique=True )

    class Meta:
        verbose_name = _(u'type of use')
        verbose_name_plural = _(u'types of use')
        ordering = [u'label']

    def __unicode__(self):
        return unicode(self.label)

class Taxon( models.Model ):
    "Plant taxon"
    genus      = models.CharField( _(u'Genus'), max_length=50 )
    species    = models.CharField( _(u'Species'), help_text=_(u'leave blank if unknown'), max_length=50, null=True, blank=True )
    subspecies = models.CharField( _(u'Variety'), help_text=_(u'do not include var.'), max_length=50, null=True, blank=True )
    author     = models.CharField( _(u'Author'), help_text=_(u'only if the species is known'), max_length=70, null=True, blank=True )
    family     = models.CharField( _(u'Family'), max_length=20, null=True, blank=True )
    # The following field was only created to order the admin form
    label      = models.TextField( _(u'Label'), null=True, blank=True )
    description = models.TextField( _(u'General description'), null=True, blank=True )
    ethno_notes = models.TextField( _(u'Ethnobotany description'), null=True, blank=True )
    references = models.ManyToManyField( Reference, through='TaxonDataReference' )
    restoration = models.BooleanField( _(u'Restoration') )
    urban_use   = models.BooleanField( _(u'Urban forestry') )
    uses      = models.ManyToManyField( TypeOfUse, through='TaxonUse' )
    h_flowers = models.BooleanField( _(u'Flowers') )
    h_leaves  = models.BooleanField( _(u'Leaves') )
    h_fruits  = models.BooleanField( _(u'Fruits') )
    h_crown   = models.BooleanField( _(u'Crown') )
    h_bark    = models.BooleanField( _(u'Bark') )
    # todo: potential_use
    rare        = models.NullBooleanField( _(u'Rare'), null=True, blank=True )
    max_density = models.IntegerField( _(u'Maximum density'), help_text=_(u'individuals per hectare'), null=True, blank=True )
    endemic = models.NullBooleanField( _(u'Endemic'), null=True, blank=True )
    sg_pioneer         = models.BooleanField( _(u'Pioneer') )
    sg_early_secondary = models.BooleanField( _(u'Early secondary') )
    sg_late_secondary  = models.BooleanField( _(u'Late secondary') )
    sg_climax          = models.BooleanField( _(u'Climax') )
    gr_slow     = models.BooleanField( _(u'Slow') )
    gr_moderate = models.BooleanField( _(u'Moderate') )
    gr_fast     = models.BooleanField( _(u'Fast') )
    gr_comments = models.TextField( _(u'Comments'), null=True, blank=True )
    pruning = models.NullBooleanField( _(u'Requires pruning'), null=True, blank=True )
    fl_start = models.IntegerField( _(u'Start'), null=True, blank=True, choices=MONTHS )
    fl_end   = models.IntegerField( _(u'End'), null=True, blank=True, choices=MONTHS )
    fl_color = models.IntegerField( _(u'Color'), null=True, blank=True, choices=COLORS )
    pollinators = models.TextField( _(u'Pollinators'), null=True, blank=True )
    dt_anemochorous = models.BooleanField( _(u'Anemochorous') )
    dt_autochorous  = models.BooleanField( _(u'Autochorous') )
    dt_hydrochorous = models.BooleanField( _(u'Hydrochorous') )
    dt_zoochorous   = models.BooleanField( _(u'Zoochorous') )
    dispersers  = models.TextField( _(u'Dispersers'), null=True, blank=True )
    fr_type = models.CharField( _(u'Fruit type'), null=True, blank=True, choices=FRUIT_TYPES, max_length=1 )
    symbiotic_assoc   = models.NullBooleanField( _(u'Presence'), null=True, blank=True )
    symbiotic_details = models.TextField( _(u'Details'), null=True, blank=True )
    r_type = models.CharField( _(u'Root system'), null=True, blank=True, choices=ROOT_SYSTEMS, max_length=1 )
    fo_evergreen = models.BooleanField( _(u'Evergreen') )
    fo_semideciduous = models.BooleanField( _(u'Semi-deciduous') )
    fo_deciduous = models.BooleanField( _(u'Deciduous') )
    cr_min_diameter = models.IntegerField( _(u'Minimum'), help_text=_(u'meters'), null=True, blank=True )
    cr_max_diameter = models.IntegerField( _(u'Maximum'), help_text=_(u'meters'), null=True, blank=True )
    cr_shape = models.CharField( _(u'Type'), null=True, blank=True, choices=CROWN_SHAPES, max_length=1 )
    bark_texture = models.CharField( _(u'Type'), null=True, blank=True, choices=BARK_TEXTURES, max_length=1 )
    tr_straight    = models.BooleanField( _(u'Straight') )
    tr_sl_inclined = models.BooleanField( _(u'Slightly inclined') )
    tr_inclined    = models.BooleanField( _(u'Inclined') )
    tr_sl_crooked  = models.BooleanField( _(u'Slightly crooked') )
    tr_crooked     = models.BooleanField( _(u'Crooked') )
    min_height     = models.FloatField( _(u'Minimum height'), help_text=_(u'meters'), null=True, blank=True )
    max_height = models.FloatField( _(u'Maximum height'), help_text=_(u'meters'), null=True, blank=True )
    min_dbh = models.IntegerField( _(u'Minimum DBH'), help_text=_(u'centimeters'), null=True, blank=True )
    max_dbh = models.IntegerField( _(u'Maximum DBH'), help_text=_(u'centimeters'), null=True, blank=True )
    thorns_or_spines = models.NullBooleanField( _(u'Presence'), null=True, blank=True )
    toxic_or_allergenic = models.NullBooleanField( _(u'Presence'), null=True, blank=True )
    pests_and_diseases = models.TextField( _(u'Information'), null=True, blank=True )
    fr_start = models.IntegerField( _(u'Start'), null=True, blank=True, choices=MONTHS )
    fr_end   = models.IntegerField( _(u'End'), null=True, blank=True, choices=MONTHS )
    seed_tree = models.BooleanField( _(u'Collect fruits from tree') )
    seed_soil = models.BooleanField( _(u'Collect fruits from soil') )
    seed_collection = models.TextField( _(u'Details'), null=True, blank=True )
    seed_type = models.CharField( _(u'Type'), null=True, blank=True, choices=SEED_TYPES, max_length=1 )
    pg_treatment = models.CharField( _(u'Treatment'), null=True, blank=True, choices=PREGERMINATION_TREATMENTS, max_length=1 )
    pg_details = models.TextField( _(u'Details'), null=True, blank=True )
    sl_seedbed = models.BooleanField( _(u'Seedbed under half shadow') )
    sl_containers = models.BooleanField( _(u'Individual containers') )
    sl_details = models.TextField( _(u'Details'), null=True, blank=True )
    seed_gmin_time = models.IntegerField( _(u'Minimum'), help_text=_(u'days'), null=True, blank=True )
    seed_gmax_time = models.IntegerField( _(u'Maximum'), help_text=_(u'days'), null=True, blank=True )
    seed_gmin_rate = models.IntegerField( _(u'Minimum'), help_text=_(u'%'), null=True, blank=True )
    seed_gmax_rate = models.IntegerField( _(u'Maximum'), help_text=_(u'%'), null=True, blank=True )
    #soil = models.CharField( _(u'Soil'), null=True, blank=True, choices=SOIL_TYPES, max_length=1 )
    light = models.CharField( _(u'Classification'), null=True, blank=True, choices=LIGHT_REQUIREMENTS, max_length=1 )
    created = models.DateTimeField( u'Date created', auto_now_add = True )
    modified = models.DateTimeField( u'Date modified', null=True )

    class Meta:
        verbose_name = _(u'plant')
        verbose_name_plural = _(u'plants')
        ordering = [u'label']

    def __unicode__(self):
        return unicode(self.label)

    def _get_field_label(self, name):
        'Return a field label given its name'
        return unicode(Taxon._meta.get_field_by_name(name)[0].verbose_name)

    def _get_boolean_concat(self, fields):
        '''
        Return comma separated labels given a list [(value,label)].
        Only labels where the value is True are returned in the string.
        '''
        types = ''
        sep = ', '
        prev = False
        for field in fields:
            if getattr(self, field):
                if prev:
                    types = string_concat(types, sep)
                types = string_concat(types, self._get_field_label(field))
                prev = True
        if prev:
            return types
        return None

    def _get_yes_no(self, value):
        'Return yes or no given a boolean value'
        if value == True:
            return _(u'yes')
        if value == False:
            return _(u'no')
        return None

    def _get_interval(self, minval, maxval, unit, decimals=None):
        'Return a string representation of an interval'
        if minval:
            if decimals is not None:
                format = '%.' + str(decimals) + 'f'
                val = format % minval
            else:
                val = str(minval)
            if maxval and maxval != minval:
                if decimals is not None:
                    val = val + '-' + (format % maxval)
                else:
                    val = val + '-' + str(maxval)
            return val + unit
        return None

    def get_use(self):
        return self._get_boolean_concat(['restoration', 'urban_use'])

    def get_successional_group(self):
        return self._get_boolean_concat(['sg_pioneer', 'sg_early_secondary', 'sg_late_secondary', 'sg_climax'])

    def get_rare(self):
        return self._get_yes_no(self.rare)

    def get_seed_gathering(self):
        if self.seed_tree and self.seed_soil:
            return _(u'Collect fruits from tree or soil')
        elif self.seed_tree:
            return self._get_field_label('seed_tree')
        elif self.seed_soil:
            return self._get_field_label('seed_soil')
        return None

    def get_seedbed(self):
        if self.sl_seedbed and self.sl_containers:
            return string_concat(self._get_field_label('sl_seedbed'),' ',_(u'or'),' ',self._get_field_label('sl_containers'))
        elif self.sl_seedbed:
            return self._get_field_label('sl_seedbed')
        elif self.sl_containers:
            return self._get_field_label('sl_containers')
        return None

    def get_germination_time_lapse(self):
        val = ''
        if self.seed_gmin_time is not None:
            val = str(self.seed_gmin_time)
            if self.seed_gmax_time is not None and self.seed_gmax_time != self.seed_gmin_time:
                val = string_concat(val, ' ', _(u'to'), ' ', str(self.seed_gmax_time), ' ', _(u'days'))
        elif self.seed_gmax_time is not None:
            val = string_concat(str(self.seed_gmax_time), ' ', _(u'days'))
        else:
            val = None
        return val

    def get_germination_rate(self):
        val = ''
        if self.seed_gmin_rate is not None:
            val = str(self.seed_gmin_rate)
            if self.seed_gmax_rate is not None and self.seed_gmax_rate != self.seed_gmin_rate:
                val = string_concat(val, ' ', _(u'to'), ' ', str(self.seed_gmax_rate), '%')
        elif self.seed_gmax_rate is not None:
            val = string_concat(str(self.seed_gmax_rate), '%')
        else:
            val = None
        return val

    def get_special_features(self):
        return self._get_boolean_concat(['h_flowers', 'h_leaves', 'h_fruits', 'h_crown', 'h_bark'])

    def get_growth_rate(self):
        return self._get_boolean_concat(['gr_slow', 'gr_moderate', 'gr_fast'])

    def get_dispersal_types(self):
        return self._get_boolean_concat(['dt_anemochorous', 'dt_autochorous', 'dt_hydrochorous', 'dt_zoochorous'])

    def get_endemic(self):
        return self._get_yes_no(self.endemic)

    def get_pruning(self):
        return self._get_yes_no(self.pruning)

    def get_symbiotic_assoc(self):
        return self._get_yes_no(self.symbiotic_assoc)

    def get_thorns_or_spines(self):
        return self._get_yes_no(self.thorns_or_spines)

    def get_toxic_or_allergenic(self):
        return self._get_yes_no(self.toxic_or_allergenic)

    def get_crown_diameter(self):
        return self._get_interval(self.cr_min_diameter, self.cr_max_diameter, 'm')

    def get_height(self):
        return self._get_interval(self.min_height, self.max_height, 'm', 1)

    def get_dbh(self):
        return self._get_interval(self.min_dbh, self.max_dbh, 'cm')

    def get_flowering_period(self):
        if self.fl_start:
            val = self.get_fl_start_display()
            if self.fl_end and self.fl_end != self.fl_start:
                val = string_concat(val, ' ', _(u'to'), ' ', self.get_fl_end_display())
            return val
        return None

    def get_fruiting_period(self):
        if self.fr_start:
            val = self.get_fr_start_display()
            if self.fr_end and self.fr_end != self.fr_start:
                val = string_concat(val, ' ', _(u'to'), ' ', self.get_fr_end_display())
            return val
        return None

    def get_trunk_alignment(self):
        return self._get_boolean_concat(['tr_straight', 'tr_sl_inclined', 'tr_inclined', 'tr_sl_crooked', 'tr_crooked'])

    def get_foliage_persistence(self):
        return self._get_boolean_concat(['fo_evergreen', 'fo_semideciduous', 'fo_deciduous'])

    # Functions used by the admin change list form
    def data_completeness(self):
        fieldsets = ((_('Taxonomic data'), bool(self.genus) and bool(self.species) and bool(self.author) and bool(self.family)),
                     (_('General description'), bool(self.description)),
                     (_('Ethnobotany description'), bool(self.ethno_notes)),
                     (_('Uses'), bool(self.restoration) or bool(self.urban_use)),
                     (_('Abundance'), self.rare is not None),

                     (_('Endemism'), self.endemic is not None),
                     (_('Special features'), (self.h_flowers is not None) and (self.h_leaves is not None) and (self.h_fruits is not None) and (self.h_crown is not None)),
                     (_('Successional group'), self.sg_pioneer or self.sg_early_secondary or self.sg_late_secondary or self.sg_climax),
                     (_('Growth rate'), self.gr_slow or self.gr_moderate or self.gr_fast),
                     (_('Pruning'), self.pruning is not None),
                     (_('Flowering period'), (self.fl_start is not None) and (self.fl_end is not None)),
                     (_('Flowering color'), self.fl_color is not None),
                     (_('Pollination'), bool(self.pollinators)),
                     (_('Seed dispersal'), (self.dt_anemochorous or self.dt_autochorous or self.dt_hydrochorous or self.dt_zoochorous)),
                     (_('Dispersion agents'), bool(self.dispersers)),
                     (_('Fruits'), self.fr_type is not None),
                     (_('Symbiotic association'), (self.symbiotic_assoc is not None) or bool(self.symbiotic_details)), 
                     (_('Roots'), self.r_type is not None), 
                     (_('Foliage persistence'), self.fo_evergreen or self.fo_semideciduous or self.fo_deciduous), 
                     (_('Crown diameter'), bool(self.cr_min_diameter) and bool(self.cr_max_diameter)), 
                     (_('Crown shape'), bool(self.cr_shape)), 
                     (_('Bark texture'), bool(self.bark_texture)), 
                     (_('Trunk alignment'), self.tr_straight or self.tr_sl_inclined or self.tr_inclined or self.tr_sl_crooked or self.tr_crooked), 
                     (_('Tree size'), bool(self.min_height) and bool(self.max_height) and bool(self.min_dbh) and bool(self.max_dbh)), 
                     (_('Thorns or spines'), self.thorns_or_spines is not None), 
                     (_('Toxic or allergenic'), self.toxic_or_allergenic is not None), 
                     (_('Pests and diseases'), bool(self.pests_and_diseases)), 
                     (_('Fruiting period'), (self.fr_start is not None) and (self.fr_end is not None)), 
                     (_('Seed collection'), self.seed_tree or self.seed_soil), 
                     (_('Seed type'), bool(self.seed_type)), 
                     (_('Pre-germination treatment'), self.pg_treatment is not None), 
                     (_('Seedling production'), self.sl_seedbed or self.sl_containers), 
                     (_('Germination time lapse'), bool(self.seed_gmin_time) and bool(self.seed_gmax_time)), 
                     (_('Germination rate'), bool(self.seed_gmin_rate) and bool(self.seed_gmax_rate)), 
                     (_('Light requirements'), self.light is not None), 
                     )
        html = ''
        cnt = 1
        for p in fieldsets:
            icon = 'no'
            alt = '-'
            if p[1]:
                icon = 'yes'
                alt = 'v'
            html = string_concat(html, '<a href="'+str(self.id)+'/#fset'+str(cnt)+'" title="',p[0],'"><img src="/static/admin/img/admin/icon-'+icon+'.gif" alt="'+alt+'" /></a>')
            cnt = cnt + 1
        return html
    data_completeness.short_description = _(u'Data completeness')
    data_completeness.allow_tags = True

    def clean(self):
        # Foliage persistence consistency
        if self.fo_evergreen and self.fo_deciduous:
            raise ValidationError(_(u'Foliage persistence cannot be evergreen and decidous simultaneously!'))
        # Crown diameter
        if self.cr_min_diameter > self.cr_max_diameter:
            raise ValidationError(_(u'Minimum crown diameter cannot be greater than the maximum diameter!'))
        self._ensure_both('cr_min_diameter', 'cr_max_diameter')
        # Height
        if self.min_height > self.max_height:
            raise ValidationError(_(u'Minimum height cannot be greater than the maximum height!'))
        self._ensure_both('min_height', 'max_height')
        # DBH
        if self.min_dbh > self.max_dbh:
            raise ValidationError(_(u'Minimum DBH cannot be greater than the maximum DBH!'))
        self._ensure_both('min_dbh', 'max_dbh')
        # Flowering period
        self._ensure_both('fl_start', 'fl_end')
        # Fruiting period
        self._ensure_both('fr_start', 'fr_end')
        # Germination time
        self._ensure_both('seed_gmin_time', 'seed_gmax_time')
        # Germination rate
        self._ensure_both('seed_gmin_rate', 'seed_gmax_rate')

    def _ensure_both(self, attr1, attr2):
        v1 = getattr(self, attr1)
        v2 = getattr(self, attr2)
        if v1 and (v2 is None):
            setattr(self, attr2, v1)
        elif v2 and (v1 is None):
            setattr(self, attr1, v2)

    def add_popular_name(self, name):
        self._add_name(u'P', name) 

    def add_synonym(self, name):
        self._add_name(u'S', name) 

    def check_name( self ):
        c_data = self._get_checklist_data()
        status = ''
        if len( c_data ):
            if c_data[1] == genus and c_data[2] == species:
                pass
            else:
                status = u'-> synonym of '+c_data[1]+' '+c_data[2]
        else:
            status = u'Not found!'

    def _add_name(self, ntype, name):
        try:
            q = TaxonName.objects.get(taxon=self, ntype=ntype, name=name)
            # do nothing if name already exists
        except Exception, e:
            # include if not found
            n = TaxonName(taxon=self, ntype=ntype, name=name)
            n.save()

    def _get_checklist_data( self ):
        query = 'http://checklist.florabrasil.net/service/ACCEPTED/FORMAT/xml/LANG/en/GENUS/'+self.genus+'/SPECIES/'+self.species
        h = httplib2.Http()
        resp, content = h.request(query)
        if resp.status == 200:
            tree = fromstring( content )
            rid = tree.findtext( 'record/id' )
            rgenus = tree.findtext( 'record/genus' )
            rspecies = tree.findtext( 'record/species' )
            assert rid, u'Checklist id is NULL'
            assert rspecies, u'Checklist genus is NULL'
            assert rgenus, u'Checklist species is NULL'
            return [rid, rgenus, rspecies]
        elif resp.status == 404:
            return []
        else:
            raise Exception(u'Problem communicating with checklist service: '+resp.status)

    def get_popular_names( self ):
        return self.taxonname_set.filter(ntype=u'P').order_by('name')

    def get_synonyms( self ):
        return self.taxonname_set.filter(ntype=u'S').order_by('name')

    def has_general_features_data(self):
        return (self.get_height() is not None) or (self.get_dbh() is not None) or (self.get_fl_color_display() is not None) or (self.get_growth_rate() is not None) or (self.gr_comments is not None and len(self.gr_comments) > 0) or (self.get_foliage_persistence() is not None) or (self.get_r_type_display() is not None) or (self.get_cr_shape_display() is not None) or (self.get_crown_diameter() is not None) or (self.get_trunk_alignment() is not None) or (self.get_bark_texture_display() is not None) or (self.get_fr_type_display() is not None) 

    def has_care_data( self ):
        return (self.get_pruning() is not None) or (self.pests_and_diseases() is not None) or (self.get_thorns_or_spines() is not None) or (self.get_toxic_or_allergenic() is not None)

    def has_ecology_and_reproduction_data( self ):
        return (self.get_successional_group() is not None) or (self.pollinators() is not None) or (self.get_flowering_period() is not None) or (self.get_dispersal_types() is not None) or (self.dispersers() is not None) or (self.get_fruiting_period() is not None) or (self.get_symbiotic_assoc() is not None) or (self.symbiotic_details is not None)

    def has_seedling_production_data( self ):
        return (self.get_seed_gathering() is not None) or (self.seed_collection) or (self.get_seed_type_display() is not None) or (self.get_pg_treatment_display() is not None) or (self.pg_details) or (self.get_seedbed() is not None) or (self.sl_details) or (self.get_germination_time_lapse() is not None) or (self.get_germination_rate() is not None) or (self.get_light_display() is not None)

    def has_bibliography_data( self ):
        return self.taxondatareference_set.all().count()

    def has_points( self ):
        return self.taxonoccurrence_set.all().count()

class TaxonName( models.Model ):
    "Taxon name"
    taxon = models.ForeignKey(Taxon)
    name = models.CharField( _(u'Name'), help_text=_(u'Taxon name'), max_length=50, db_index=True )
    ntype = models.CharField( _(u'Type'), help_text=_(u'Type'), choices=NAME_TYPES, max_length=1 )

    class Meta:
        verbose_name = _(u'name')
        verbose_name_plural = _(u'names')

    def __unicode__(self):
        return unicode(self.name)

    def clean(self):
        # Make sure there's only one accepted name for the taxon
        if self.ntype == 'A':
            try:
                other_accepted_names = TaxonName.objects.get( taxon=self.taxon, ntype='A' ).exclude( pk=self.id )
                raise ValidationError(u'A taxon may only have a single accepted name!')
            except Exception, e:
                # OK, no other accepted names
                pass

class ConservationAssessmentSource( models.Model ):
    "Conservation assessment source"
    acronym = models.CharField( _(u'Acronym'), max_length=30 )

    class Meta:
        verbose_name = _(u'conservation assessment source')
        verbose_name_plural = _(u'conservation assessment sources')

    def __unicode__(self):
        return unicode(self.acronym)

class ConservationStatus( models.Model ):
    "Conservation status"
    taxon  = models.ForeignKey(Taxon)
    source = models.ForeignKey(ConservationAssessmentSource, verbose_name=_(u'Source'))
    status = models.CharField( _(u'Status'), max_length=30 )

    class Meta:
        verbose_name = _(u'conservation status')
        verbose_name_plural = _(u'conservation statuses')

    def __unicode__(self):
        return unicode(self.status)

class TaxonDataReference( models.Model ):
    "Reference for a taxon data"
    taxon     = models.ForeignKey(Taxon)
    reference = models.ForeignKey(Reference, verbose_name=_(u'Reference'))
    data      = models.CharField( _(u'Data'), max_length=3, choices=TAXON_DATA )
    notes     = models.CharField( _(u'Notes'), help_text=_(u'Additional notes, such as page numbers'), max_length=80, null=True, blank=True )

    def __unicode__(self):
        return unicode(self.taxon) + u' ' + unicode(self.reference)

class TaxonUse( models.Model ):
    "Uses of a taxon"
    taxon = models.ForeignKey(Taxon)
    use   = models.ForeignKey(TypeOfUse, verbose_name=_(u'type of use'))
    fieldwork = models.BooleanField( _(u'Detected in fieldwork') )

    class Meta:
        unique_together = ((u'taxon', u'use'),)

    def __unicode__(self):
        return unicode(self.taxon) + u' ' + unicode(self.use)

class TaxonOccurrence( models.Model ):
    "Taxon occurrence"
    taxon     = models.ForeignKey(Taxon)
    label     = models.TextField( _(u'Label'), null=True, blank=True )
    locality  = models.TextField( _(u'Locality'), null=True, blank=True )
    long_orig = models.CharField( _(u'Original longitude'), max_length=30 )
    lat_orig  = models.CharField( _(u'Original latitude'), max_length=30 )

    def get_decimal_long(self):
        val = self.long_orig
        res = re.search(u'^-?\d{1,3}(\.\d+)?$', val)
        if ( res is not None ):
            return float(val)
        res = re.search(u'^(\d{1,3})([WE])(\d{1,2})\'(\d{1,2}\.\d+)\"?$', val)
        if ( res is not None ):
            retval = float(res.group(1)) + float(res.group(3))/60.0 + float(res.group(4))/60.0/60.0
            if res.group(2) == 'W':
                retval = -1*retval
            return retval
        raise Exception('Could not interpret longitude: '+self.long_orig)

    def get_decimal_lat(self):
        val = self.lat_orig
        res = re.search(u'^-?\d{1,2}(\.\d+)?$', val)
        if ( res is not None ):
            return float(val)
        res = re.search(u'^(\d{1,2})([NS])(\d{1,2})\'(\d{1,2}\.\d+)\"?$', val)
        if ( res is not None ):
            retval = float(res.group(1)) + float(res.group(3))/60.0 + float(res.group(4))/60.0/60.0
            if res.group(2) == 'S':
                retval = -1*retval
            return retval
        raise Exception('Could not interpret latitude: '+self.lat_orig)

############# Signal receivers #############

@receiver(post_save, sender=Taxon, dispatch_uid='post_save_taxon')
def post_save_taxon( sender, instance, created, raw, using, **kwargs ):
    # Update or include the corresponding accepted name without author
    short_name = instance.genus
    if instance.species is None:
        short_name = short_name + u' spp'
    else:
        short_name = short_name + ' ' + instance.species
    if created:
        accepted = TaxonName( taxon=instance, ntype=u'A', name=short_name )
        accepted.save()
    else:
        accepted = TaxonName.objects.get( taxon=instance, ntype=u'A' )
        if short_name <> accepted.name:
            accepted.name = short_name
            accepted.save()

@receiver(pre_save, sender=Taxon, dispatch_uid='pre_save_taxon')
def pre_save_taxon( sender, instance, raw, using, **kwargs ):
    instance.modified = datetime.datetime.now()
    # Update label
    if instance.species is None:
        instance.label = instance.genus + u' spp'
    else:
        if instance.subspecies:
            instance.label = instance.genus + ' ' + instance.species + u' var. ' + instance.subspecies + ' ' + instance.author
        else:
            instance.label = instance.genus + ' ' + instance.species + ' ' + instance.author
