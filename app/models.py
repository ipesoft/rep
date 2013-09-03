# coding=UTF-8

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.utils.translation import ugettext
from django.utils import translation
from treebeard.mp_tree import MP_Node
from tinymce.models import HTMLField

import httplib2, datetime, re, string
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

FRUIT_CLASSES = (
    ( u'D', _(u'Dry dehiscent') ),
    ( u'I', _(u'Dry indehiscent') ),
    ( u'F', _(u'Fleshy indehiscent') ),
    ( u'N', _(u'Infructescence') ),
    ( u'M', _(u'Multiple') ),
    ( u'P', _(u'Pseudofruit') ),
)

FRUIT_TYPES = (
    ( u'B', _(u'Berry') ),
    ( u'C', _(u'Capsule') ),
    ( u'D', _(u'Drupe') ),
    ( u'L', _(u'Legume') ),
    ( u'F', _(u'Follicle') ),
    ( u'S', _(u'Silicle') ),
    ( u'M', _(u'Samara') ),
    ( u'A', _(u'Achene') ),
    ( u'Y', _(u'Caryopsis') ),
    ( u'N', _(u'Syconium') ),
    ( u'H', _(u'Hesperidium') ),
    ( u'P', _(u'Pepo') ),
    ( u'X', _(u'Pyxis') ),
    ( u'O', _(u'Operculate') ),
    ( u'G', _(u'Glans') ),
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
    ( u'I', _(u'Intermediary') ),
    ( u'U', _(u'Unclassified') ),
)

#SOIL_TYPES = (
#    ( u'F', _(u'wetland (frequent floods)') ),
#    ( u'U', _(u'wetland (unfrequent floods)') ),
#    ( u'M', _(u'marsh') ),
#    ( u'D', _(u'dry and rocky') ),
#    ( u'A', _(u'wet or dry') ),
#)

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
    ( u'SYM', _(u'Symbiotic association with roots') ),
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
    ( u'SPW', _(u'Seeds per weight') ),
    ( u'LIG', _(u'Light requirements') ),
    ( u'TER', _(u'Terrain drainage') ),
    ( u'USE', _(u'Use') ),
)

# Translate languages, since this is not possible in the settings file
translated_languages = []
for lang_code, lang_name in settings.LANGUAGES:
    translated_languages.append( (lang_code, ugettext(lang_name)) )

class StaticContent( models.Model ):
    "Static content"
    code = models.SlugField( _(u'Code'), help_text=_(u'Unique code'), db_index=True )
    lang = models.CharField( _(u'Language'), choices=translated_languages, max_length=12 )
    description = models.TextField( _(u'Description') )
    title = models.TextField( _(u'Title'), null=True, blank=True )
    content = HTMLField( _(u'Content') )

    class Meta:
        verbose_name = _(u'static content')
        verbose_name_plural = _(u'static contents')
        unique_together = ((u'code', u'lang'),)
        ordering = [u'description']

    def __unicode__(self):
        return unicode(self.description)

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

class TypeOfUse( MP_Node ):
    "Types of use of a taxon"
    label = models.TextField( _(u'Label'), unique=True )
    node_order_by = [u'label']

    class Meta:
        verbose_name = _(u'type of use')
        verbose_name_plural = _(u'types of use')
        ordering = [u'path']

    def __unicode__(self):
        if self.depth > 1:
            return u'-'*(self.depth-1)+unicode(self.label)
        else:
            return unicode(self.label)

class Interview( models.Model ):
    "Interview"
    title        = models.TextField( _(u'Title') )
    locality     = models.TextField( _(u'Locality'), null=True, blank=True )
    when         = models.DateTimeField( u'When', null=True, blank=True )
    duration     = models.CharField( _(u'Duration'), max_length=10, null=True, blank=True )
    interviewers = models.CharField( _(u'Interviewers'), max_length=100 )
    interviewees = models.CharField( _(u'Interviewees'), max_length=100 )
    content      = models.TextField( _(u'Content'))
    audio_url    = models.CharField( _(u'Audio URL'), max_length=200, null=True, blank=True )

    class Meta:
        verbose_name = _(u'interview')
        verbose_name_plural = _(u'interviews')
        ordering = [u'title']

    def __unicode__(self):
        return unicode(self.title)

    def get_citations(self):
        return TaxonCitation.objects.filter(interview=self).order_by('cited_name', 'page')

    def get_parts(self):
        return InterPart.objects.filter(interview=self).order_by('page')

    def update_references(self):
        import re
        if len(self.content):
            import xml.etree.ElementTree as etree
            from app.interview_paginator import InterviewPaginator
            paginator = InterviewPaginator(self.content, 1, 0, True, 40)
            cit_keys = []
            part_keys = []
            for page_num in range(1, paginator.num_pages+1):
                page_obj = paginator.page(page_num)
                # Note: There must always one object
                # Note: without the encode I get psycopg "can't adapt" error (??)
                content = page_obj.object_list[0].encode('utf-8')
                root = etree.fromstring('<?xml version="1.0" encoding="UTF-8"?><x>'+content+'</x>')
                nodes = root.findall(".//a")
                for node in nodes:
                    #### Species citations ###############
                    if node.get('class') == 'sp_citation':
                        name = node.text.lower()
                        if node.get('href') is None:
                            recs = TaxonCitation.objects.filter(interview=self.id, page=page_num, taxon__isnull=True, cited_name=name)
                            if len(recs) > 0:
                                # same citation already exists in the database
                                cit_keys.append(recs[0].id)
                            else:
                                # new or changed citation
                                rec = TaxonCitation(interview=self, page=page_num, cited_name=name)
                                rec.save()
                                cit_keys.append(rec.id)
                        else:
                            url = node.get('href')
                            # patterns:
                            # search by name: /sp/?name=sp_name
                            # exact link: /sp/18
                            pos = url.find('?name=')
                            if pos > 0:
                                recs = TaxonCitation.objects.filter(interview=self, page=page_num, taxon__isnull=True, cited_name=name)
                                if len(recs) > 0:
                                    # same citation already exists in the database
                                    cit_keys.append(recs[0].id)
                                else:
                                    # new or changed citation
                                    rec = TaxonCitation(interview=self, page=page_num, cited_name=name)
                                    rec.save()
                                    cit_keys.append(rec.id)
                            else:
                                # extract taxon id
                                m = re.search('\/sp\/(\d+)\/?', url)
                                if len( m.groups() ) == 1:
                                    taxon_id = int( m.group(1) )
                                    try:
                                        taxon = Taxon.objects.get(pk=taxon_id)
                                        recs = TaxonCitation.objects.filter(interview=self, taxon=taxon, page=page_num, cited_name=name)
                                        if len(recs) > 0:
                                            # same citation already exists in the database
                                            cit_keys.append(recs[0].id)
                                        else:
                                            # new or changed citation
                                            rec = TaxonCitation(interview=self, taxon=taxon, page=page_num, cited_name=name)
                                            rec.save()
                                            cit_keys.append(rec.id)
                                    except Taxon.DoesNotExist:
                                        raise Exception('Taxon '+taxon_id+' referenced in page '+str(page_num)+' does not exist!')
                                else:
                                    raise Exception('Bad formatted taxon reference link in page '+str(page_num))
                    #### Parts #########################
                    elif node.get('class') == 'part':
                        title = node.text
                        anchor_id = node.get('id')
                        try:
                            rec = InterPart.objects.get(interview=self.id, anchor=anchor_id)
                            # Part already exists in the database
                            if rec.page != page_num or rec.title != title:
                                rec.page = page_num
                                rec.title = title
                                rec.save()
                        except InterPart.DoesNotExist:
                            # new or changed anchor
                            rec = InterPart(interview=self, page=page_num, title=title, anchor=anchor_id)
                            rec.save()
                        part_keys.append(rec.id)
            # Remove out dated references
            TaxonCitation.objects.filter(interview=self).exclude(id__in=cit_keys).delete()
            InterPart.objects.filter(interview=self).exclude(id__in=part_keys).delete()
        else:
            TaxonCitation.objects.filter(interview=self).delete()
            InterPart.objects.filter(interview=self).delete()

    def get_pdf_name(self):
        return 'interview_' + str(self.id) + '.pdf'

    def generate_pdf(self):
        # For now, save document only in the settings language
        cur_language = translation.get_language()
        if cur_language <> settings.LANGUAGE_CODE:
            translation.activate( settings.LANGUAGE_CODE )
        pdf_file = settings.PDF_ROOT + self.get_pdf_name()
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_JUSTIFY
        from reportlab.rl_config import defaultPageSize
        from reportlab.lib.units import inch
        PAGE_HEIGHT=defaultPageSize[1]
        PAGE_WIDTH=defaultPageSize[0]
        styles = getSampleStyleSheet()
        styles.add( ParagraphStyle(name='Justify', alignment=TA_JUSTIFY) )
        doc = SimpleDocTemplate( pdf_file )
        Story = [Spacer(1,2*inch)]
        style = styles['Justify']
        px = 7.0
        py = 0.75
        # Page functions
        def myFirstPage( canvas, doc ):
            canvas.saveState()
            x1 = 70
            x2 = 520
            y1 = 700
            y2 = 820
            crosshairs = [(x1,y1,x1,y2), (x1,y2,x2,y2), (x2,y2,x2,y1), (x2,y1,x1,y1)]
            canvas.lines(crosshairs)
            canvas.setFont( 'Times-Roman', 12 )
            # IMPORTANT: String concatenation doesn't seem to work here, but you can use the % operator
            #            otherwise you get a utf parameter number error
            canvas.drawString( 1.1*inch, 11.1*inch, '%s: %s' % ( ugettext(u'Interviewee(s)'), self.interviewees) )
            canvas.drawString( 1.1*inch, 10.8*inch, '%s: %s' % ( ugettext(u'Interviewer(s) and transcription'), self.interviewers) )
            canvas.drawString( 1.1*inch, 10.5*inch, '%s: %s' % ( ugettext(u'Date'), self.when.strftime("%d/%m/%Y")) )
            canvas.drawString( 1.1*inch, 10.2*inch, '%s: %s' % ( ugettext(u'Place'), self.locality) )
            canvas.drawString( 1.1*inch, 9.9*inch, '%s: %s' % ( ugettext(u'Duration'), self.duration) )
            canvas.setFont( 'Times-Roman', 9 )
            canvas.drawString( 1.1*inch, 9.5*inch, '%s' % ugettext(u'Symbology') )
            canvas.drawString( 1.1*inch, 9.3*inch, '[...]: %s.' % ugettext(u'excerpt removed or not transcribed') )
            canvas.setFont( 'Times-Roman', 12 )
            canvas.drawString( 1.1*inch, 8.8*inch, '%s' % ugettext(u'TRANSCRIPTION') )
            canvas.setFont( 'Times-Roman', 9 )
            canvas.drawString( px*inch, py*inch,"p. %d" % (doc.page) )
            canvas.restoreState()
        def myLaterPages( canvas, doc ):
            canvas.saveState()
            canvas.setFont( 'Times-Roman', 9 )
            canvas.drawString( px*inch, py*inch,"p. %d" % (doc.page) )
            canvas.restoreState()
        # Strip tags
        content = re.compile(r'<[^<]*?/?>').sub('', self.content)
        # Loop over paragraphs
        paragraphs = content.split("\n")
        for paragraph in paragraphs:
            try:
                sep = paragraph.index(': ', 1)
                # Only colons close to the beginning
                if sep < 30:
                    paragraph = '<b>' + paragraph[:sep] + '</b>' + paragraph[sep:]
            except:
                pass
            p = Paragraph( paragraph, style )
            Story.append( p )
            Story.append( Spacer(1, 0.2*inch) )
        doc.build( Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages )

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
    citations = models.ManyToManyField( Interview, through='TaxonCitation' )
    restoration  = models.BooleanField( _(u'Restoration') )
    urban_use    = models.BooleanField( _(u'Urban forestry') )
    silviculture = models.BooleanField( _(u'Silviculture') )
    uses      = models.ManyToManyField( TypeOfUse, through='TaxonUse' )
    # Special features
    h_flowers = models.BooleanField( _(u'Flowers') )
    h_leaves  = models.BooleanField( _(u'Leaves') )
    h_fruits  = models.BooleanField( _(u'Fruits') )
    h_crown   = models.BooleanField( _(u'Crown') )
    h_bark    = models.BooleanField( _(u'Bark') )
    h_seeds   = models.BooleanField( _(u'Seeds') )
    h_wood    = models.BooleanField( _(u'Wood') )
    h_roots   = models.BooleanField( _(u'Roots') )
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
    fl_details = models.TextField( _(u'Details'), null=True, blank=True )
    fl_color = models.IntegerField( _(u'Color'), null=True, blank=True, choices=COLORS )
    fl_color_details = models.TextField( _(u'Details'), null=True, blank=True )
    pollinators = models.TextField( _(u'Pollinators'), null=True, blank=True )
    dt_anemochorous = models.BooleanField( _(u'Anemochorous') )
    dt_autochorous  = models.BooleanField( _(u'Autochorous') )
    dt_barochorous = models.BooleanField( _(u'Barochorous') )
    dt_hydrochorous = models.BooleanField( _(u'Hydrochorous') )
    dt_zoochorous   = models.BooleanField( _(u'Zoochorous') )
    dispersers  = models.TextField( _(u'Dispersers'), null=True, blank=True )
    fr_class = models.CharField( _(u'Fruit class'), null=True, blank=True, choices=FRUIT_CLASSES, max_length=1 )
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
    fr_details = models.TextField( _(u'Details'), null=True, blank=True )
    seed_tree = models.BooleanField( _(u'Collect fruits from tree') )
    seed_soil = models.BooleanField( _(u'Collect fruits from soil') )
    seed_collection = models.TextField( _(u'Details'), null=True, blank=True )
    seed_type = models.CharField( _(u'Type'), null=True, blank=True, choices=SEED_TYPES, max_length=1 )
    pg_no_need    = models.BooleanField( _(u'No need for treatment') )
    pg_thermal    = models.BooleanField( _(u'Thermal treatment') )
    pg_chemical   = models.BooleanField( _(u'Chemical treatment') )
    pg_water      = models.BooleanField( _(u'Immersion in water') )
    pg_mechanical = models.BooleanField( _(u'Mechanical scarification') )
    pg_combined   = models.BooleanField( _(u'Combined treatments') )
    pg_other      = models.BooleanField( _(u'Other') )
    pg_details = models.TextField( _(u'Details'), null=True, blank=True )
    sl_seedbed = models.BooleanField( _(u'Seedbed') )
    sl_containers = models.BooleanField( _(u'Individual containers') )
    sl_details = models.TextField( _(u'Details'), null=True, blank=True )
    seed_gmin_time = models.IntegerField( _(u'Minimum'), help_text=_(u'days'), null=True, blank=True )
    seed_gmax_time = models.IntegerField( _(u'Maximum'), help_text=_(u'days'), null=True, blank=True )
    seed_gmin_rate = models.IntegerField( _(u'Minimum'), help_text=_(u'%'), null=True, blank=True )
    seed_gmax_rate = models.IntegerField( _(u'Maximum'), help_text=_(u'%'), null=True, blank=True )
    seeds_per_weight = models.IntegerField( _(u'Quantity'), help_text=_(u'num/Kg'), null=True, blank=True )
    #soil = models.CharField( _(u'Soil'), null=True, blank=True, choices=SOIL_TYPES, max_length=1 )
    wetland = models.BooleanField( _(u'Wetland') )
    dry = models.BooleanField( _(u'Well-drained') )
    terrain_details = models.TextField( _(u'Details'), null=True, blank=True )
    light = models.CharField( _(u'Classification'), null=True, blank=True, choices=LIGHT_REQUIREMENTS, max_length=1 )
    light_details = models.TextField( _(u'Details'), null=True, blank=True )
    has_pictures = models.BooleanField( _(u'Has pictures') )
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
        return self._get_boolean_concat(['restoration', 'urban_use', 'silviculture'])

    def get_specific_uses(self):
        # Original simple comma separated list
        #uses = self.uses.all().order_by('label').values_list('label', flat=True)
        #return string.join(uses, ', ')
        #
        # List of root nodes indicating subnodes inside parentheses
        uses = self.uses.all().order_by('path')
        roots = {} # root id => [root label, [descendant labels]]
        for use in uses:
            if use.is_root():
                roots[use.id] = [use.label, []]
            else:
                root = use.get_root()
                if roots.has_key(root.id):
                    roots[root.id][1].append( use.label )
                else:
                    roots[root.id] = [root.label, [use.label]]
        is_first = True
        uses_str = ''
        for rid, rdata in roots.iteritems():
            if is_first:
                is_first = False
                uses_str = rdata[0]
            else:
                uses_str += ', ' + rdata[0]
            if len( rdata[1] ) > 0:
                uses_str += ' (' + ', '.join(rdata[1]) + ')'
        return uses_str

    def get_successional_group(self):
        return self._get_boolean_concat(['sg_pioneer', 'sg_early_secondary', 'sg_late_secondary', 'sg_climax'])

    def get_pregermination_treatment(self):
        return self._get_boolean_concat(['pg_no_need', 'pg_thermal', 'pg_chemical', 'pg_water', 'pg_mechanical', 'pg_combined', 'pg_other'])

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
        val = None
        if self.seed_gmin_time is not None:
            if self.seed_gmax_time is not None and self.seed_gmax_time != self.seed_gmin_time:
                val = string_concat(str(self.seed_gmin_time), ' ', _(u'to'), ' ', str(self.seed_gmax_time), ' ', _(u'days'))
            else:
                val = string_concat(str(self.seed_gmin_time), ' ', _(u'days'))
        elif self.seed_gmax_time is not None:
            val = string_concat(str(self.seed_gmax_time), ' ', _(u'days'))
        return val

    def get_germination_rate(self):
        val = None
        if self.seed_gmin_rate is not None:
            if self.seed_gmax_rate is not None and self.seed_gmax_rate != self.seed_gmin_rate:
                val = string_concat(str(self.seed_gmin_rate), ' ', _(u'to'), ' ', str(self.seed_gmax_rate), '%')
            else:
                val = string_concat(str(self.seed_gmin_rate), '%')
        elif self.seed_gmax_rate is not None:
            val = string_concat(str(self.seed_gmax_rate), '%')
        return val

    def get_special_features(self):
        return self._get_boolean_concat(['h_flowers', 'h_leaves', 'h_fruits', 'h_crown', 'h_bark', 'h_seeds', 'h_wood', 'h_roots'])

    def get_growth_rate(self):
        return self._get_boolean_concat(['gr_slow', 'gr_moderate', 'gr_fast'])

    def get_dispersal_types(self):
        return self._get_boolean_concat(['dt_anemochorous', 'dt_autochorous', 'dt_barochorous', 'dt_hydrochorous', 'dt_zoochorous'])

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

    def get_terrain_drainage(self):
        return self._get_boolean_concat(['wetland', 'dry'])

    def get_fruit_classification(self):
        val = None
        if self.fr_class:
            val = self.get_fr_class_display()
        if self.fr_type:
            if self.fr_class:
                val += ' (' + self.get_fr_type_display() + ')'
            else:
                val = self.get_fr_type_display()
        return val

    def has_pregermination_treatment(self):
        return (self.pg_no_need or self.pg_thermal or self.pg_chemical or self.pg_water or self.pg_mechanical or self.pg_combined or self.pg_other)

    # Functions used by the admin change list form
    def data_completeness(self):
        fieldsets = ((_('Taxonomic data'), bool(self.genus) and bool(self.species) and bool(self.author) and bool(self.family)),
                     (_('General description'), bool(self.description)),
                     (_('Ethnobotany description'), bool(self.ethno_notes)),
                     (_('Uses'), bool(self.restoration) or bool(self.urban_use) or bool(self.silviculture)),
                     (_('Abundance'), self.rare is not None),

                     (_('Endemism'), self.endemic is not None),
                     (_('Special features'), (self.h_flowers is not None) and (self.h_leaves is not None) and (self.h_fruits is not None) and (self.h_crown is not None) and (self.h_bark is not None) and (self.h_seeds is not None) and (self.h_wood is not None) and (self.h_roots is not None)),
                     (_('Successional group'), self.sg_pioneer or self.sg_early_secondary or self.sg_late_secondary or self.sg_climax),
                     (_('Growth rate'), self.gr_slow or self.gr_moderate or self.gr_fast),
                     (_('Pruning'), self.pruning is not None),
                     (_('Flowering period'), (self.fl_start is not None) and (self.fl_end is not None)),
                     (_('Flowering color'), self.fl_color is not None),
                     (_('Pollination'), bool(self.pollinators)),
                     (_('Seed dispersal'), (self.dt_anemochorous or self.dt_autochorous or self.dt_barochorous or self.dt_hydrochorous or self.dt_zoochorous)),
                     (_('Dispersion agents'), bool(self.dispersers)),
                     (_('Fruits'), (self.fr_type is not None or self.fr_class is not None)),
                     (_('Symbiotic association with roots'), (self.symbiotic_assoc is not None) or bool(self.symbiotic_details)), 
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
                     (_('Pre-germination treatment'), self.has_pregermination_treatment()), 
                     (_('Seedling production'), self.sl_seedbed or self.sl_containers), 
                     (_('Germination time lapse'), bool(self.seed_gmin_time) and bool(self.seed_gmax_time)), 
                     (_('Germination rate'), bool(self.seed_gmin_rate) and bool(self.seed_gmax_rate)), 
                     (_('Seeds per weight'), bool(self.seeds_per_weight)), 
                     (_('Light requirements'), self.light is not None), 
                     (_('Terrain drainage'), self.wetland or self.dry), 
                     )
        html = ''
        cnt = 1
        for p in fieldsets:
            icon = 'no'
            alt = '-'
            if p[1]:
                icon = 'yes'
                alt = 'v'
            html = string_concat(html, '<a href="'+str(self.id)+'/#fset'+str(cnt)+'" title="',p[0],'"><img src="/static/admin/img/icon-'+icon+'.gif" alt="'+alt+'" /></a>')
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
        # Fruit classification
        if self.fr_class and self.fr_type:
            if self.fr_class == 'D' and self.fr_type not in ('F', 'L', 'S', 'C', 'O', 'X'):
                raise ValidationError(_(u'Fruit type incompatible with fruit class!'))
            elif self.fr_class == 'I' and self.fr_type not in ('A', 'M', 'Y', 'G'):
                raise ValidationError(_(u'Fruit type incompatible with fruit class!'))
            elif self.fr_class == 'F' and self.fr_type not in ('D', 'B', 'H', 'P'):
                raise ValidationError(_(u'Fruit type incompatible with fruit class!'))
            elif self.fr_class == 'N' and self.fr_type not in ('N'):
                raise ValidationError(_(u'Fruit type incompatible with fruit class!'))

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

    def check_name( self, verbose=False ):
        status = ''
        try:
            c_data = self._get_checklist_data( verbose )
            if len( c_data ):
                if c_data[1] == self.genus and c_data[2] == self.species:
                    pass
                else:
                    status = u'-> synonym of '+c_data[1]+' '+c_data[2]
            else:
                status = u' Not found!'
        except Exception, e:
            status = u' Exception: ' + str(e)
        return status

    def _add_name(self, ntype, name):
        try:
            q = TaxonName.objects.get(taxon=self, ntype=ntype, name=name)
            # do nothing if name already exists
        except Exception, e:
            # include if not found
            n = TaxonName(taxon=self, ntype=ntype, name=name)
            n.save()

    def _get_checklist_data( self, verbose=False ):
        query = 'http://checklist.florabrasil.net/service/ACCEPTED/FORMAT/xml/LANG/en/GENUS/'+self.genus+'/SPECIES/'+self.species
        if verbose:
            print query
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
        return (self.get_height() is not None) or (self.get_dbh() is not None) or (self.get_fl_color_display() is not None) or (self.get_growth_rate() is not None) or (self.gr_comments is not None and len(self.gr_comments) > 0) or (self.get_foliage_persistence() is not None) or (self.get_r_type_display() is not None) or (self.get_cr_shape_display() is not None) or (self.get_crown_diameter() is not None) or (self.get_trunk_alignment() is not None) or (self.get_bark_texture_display() is not None) or (self.get_fr_class_display() is not None) or (self.get_fr_type_display() is not None) or (self.fl_color_details is not None and len(self.fl_color_details) > 0)

    def has_care_data( self ):
        return (self.get_pruning() is not None) or (self.pests_and_diseases is not None) or (self.get_thorns_or_spines() is not None) or (self.get_toxic_or_allergenic() is not None) or self.wetland or self.dry

    def has_ecology_and_reproduction_data( self ):
        return (self.get_successional_group() is not None) or (self.pollinators is not None and len(self.pollinators) > 0) or (self.get_flowering_period() is not None) or (self.get_dispersal_types() is not None) or (self.dispersers is not None and len(self.dispersers) > 0) or (self.get_fruiting_period() is not None) or (self.get_symbiotic_assoc() is not None) or (self.symbiotic_details is not None and len(self.symbiotic_details) > 0) or (self.fr_details is not None and len(self.fr_details) > 0) or (self.fl_details is not None and len(self.fl_details) > 0)

    def has_seedling_production_data( self ):
        return (self.get_seed_gathering() is not None) or (self.seed_collection) or (self.get_seed_type_display() is not None) or (self.get_pregermination_treatment() is not None) or (self.pg_details) or (self.get_seedbed() is not None) or (self.sl_details) or (self.get_germination_time_lapse() is not None) or (self.get_germination_rate() is not None) or (self.get_light_display() is not None) or (self.seeds_per_weight is not None) or (self.light_details is not None and len(self.light_details) > 0)

    def has_bibliography_data( self ):
        return (self.taxondatareference_set.all().count() > 0)

    def has_points( self ):
        return (self.taxonoccurrence_set.all().count() > 0)

    def has_history( self ):
        return (self.citations.count() > 0)

    def get_citations( self ):
        return TaxonCitation.objects.filter(taxon=self).order_by('interview', 'page')

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

class TaxonCitation( models.Model ):
    "Taxon citation in an interview"
    interview  = models.ForeignKey(Interview)
    # Note1: The taxon may not be uniquely identified or even present in the DB
    # Note2: The same taxon may be cited more than once in the same interview
    taxon      = models.ForeignKey(Taxon, null=True)
    cited_name = models.CharField( _(u'Cited name'), max_length=50 )
    page       = models.IntegerField( _(u'Page number') )

    def __unicode__(self):
        return unicode(self.taxon) + u' in ' + unicode(self.interview) + u'(p.' + str(self.page) + u')'

class InterPart( models.Model ):
    "Highlight of an interview"
    interview = models.ForeignKey(Interview)
    title     = models.CharField( _(u'Title'), max_length=100 )
    page      = models.IntegerField( _(u'Page number') )
    anchor    = models.CharField( _(u'Anchor id'), max_length=20 )

    def __unicode__(self):
        return unicode(self.title) + u' in ' + unicode(self.interview)

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

@receiver(post_save, sender=Interview, dispatch_uid='post_save_interview')
def post_save_interview( sender, instance, created, raw, using, **kwargs ):
    # Update citations
    instance.update_references()
    instance.generate_pdf()
