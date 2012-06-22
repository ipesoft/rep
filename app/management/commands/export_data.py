# coding=UTF-8

import codecs, string
from xml.sax.saxutils import escape
from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import translation
from django.utils.translation import string_concat
from django.utils.translation import ugettext_lazy as _
from app.models import Taxon

class Command( BaseCommand ):
    option_list = BaseCommand.option_list + (
        make_option('-f', '--file', dest='file_path', type='string',
            help='Output file path.'),
        )
    help = "Export data according to the TDWG Species Profile Model (SPM)"
    usage_str = "Usage: ./manage.py export_data app -f file_path"

    def handle( self, app=None, file_path=None, **options ):
        if file_path is None:
            print 'You must specify a file path'
            exit(1)
        f = codecs.open( file_path, 'wb', 'utf8' )
        f.write(u"<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n")
        f.write(u'<response xmlns="http://www.eol.org/transfer/content/0.3" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#" xmlns:dwc="http://rs.tdwg.org/dwc/dwcore/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.eol.org/transfer/content/0.3 http://services.eol.org/schema/content_0_3.xsd">')
        lang = settings.LANGUAGE_CODE
        translation.activate(lang)
        taxa = Taxon.objects.all()
        for taxon in taxa:
            guid = settings.GUID_FORMAT % taxon.id
            url = settings.SPECIES_URL_FORMAT % taxon.id
            start_taxon = u"\n\t<taxon>\n\t\t<dc:identifier>%s</dc:identifier>\n\t\t<dc:source>%s</dc:source>\n\t\t<dwc:Kingdom>Plantae</dwc:Kingdom>\n\t\t<dwc:Family>%s</dwc:Family>\n\t\t<dwc:ScientificName>%s %s %s</dwc:ScientificName>\n\t\t<rank>species</rank>" % (guid, url, escape(taxon.family), escape(taxon.genus), escape(taxon.species), escape(taxon.author))
            f.write( start_taxon )
            # Common names
            for pop in taxon.taxonname_set.filter(ntype='P'):
                name = u"\n\t\t<commonName xml:lang=\"%s\">%s</commonName>" % (lang, escape(pop.name))
                f.write( name )
            # Synonyms
            for syn in taxon.taxonname_set.filter(ntype='S'):
                name = u"\n\t\t<synonym relationship=\"synonym\">%s</synonym>" % escape(syn.name)
                f.write( name )
            # Agents
            creator = u"\n\t\t<agent homepage=\"%s\" logoURL=\"%s\" role=\"creator\">%s</agent>" % (settings.CREATOR_HOMEPAGE, settings.CREATOR_LOGO_URL, settings.CREATOR_NAME)
            f.write( creator )
            compilers = settings.COMPILERS
            for compiler in compilers:
                f.write(u"\n\t\t<agent role=\"compiler\">"+compiler+'</agent>')
            # Dates
            f.write(u"\n\t\t<dcterms:created>"+string.replace(str(taxon.created), ' ', 'T')+"</dcterms:created>")
            if taxon.modified is not None:
                f.write(u"\n\t\t<dcterms:modified>"+string.replace(str(taxon.modified), ' ', 'T')+"</dcterms:modified>")
            # Data objects
            ## General description
            desc = ''
            desc_ref = ['-']
            fol = taxon.get_foliage_persistence()
            if fol != '-':
                desc = string_concat( desc, _(u'Foliage persistence'), ': ', fol, '. ' )
                desc_ref.append('FOL')
            if taxon.fl_color is not None:
                desc = string_concat( desc, _(u'Flowering color'), ': ', taxon.get_fl_color_display(), '. ' )
                repro_ref.append('FLC')
            flp = taxon.get_flowering_period()
            if flp != '-':
                desc = string_concat( desc, _(u'Flowering period'), ': ', flp, '. ' )
                desc_ref.append('FLP')
            if taxon.r_type is not None:
                desc = string_concat( desc, taxon._get_field_label('r_type'), ': ', taxon.get_r_type_display(), '. ' )
                repro_ref.append('ROT')
            if taxon.cr_shape is not None:
                desc = string_concat( desc, _(u'Crown shape'), ': ', taxon.get_cr_shape_display(), '. ' )
                repro_ref.append('CRS')
            tra = taxon.get_trunk_alignment()
            if tra != '-':
                desc = string_concat( desc, _(u'Trunk alignment'), ': ', tra, '. ' )
                desc_ref.append('TRA')
            if taxon.bark_texture is not None:
                desc = string_concat( desc, _(u'Bark texture'), ': ', taxon.get_bark_texture_display(), '. ' )
                repro_ref.append('BRT')
            if len(desc):
                self._add_data_object( f, taxon, u'GeneralDescription', desc_ref, desc, lang)
            ## Size
            size = ''
            size_ref = ['SIZ']
            h = taxon.get_height()
            if h != '-':
                size = string_concat( _(u'height'), ': ', h, '. ' )
            dbh = taxon.get_dbh()
            if dbh != '-':
                size = string_concat( size, _(u'DBH'), ': ', dbh, '. ' )
            crd = taxon.get_crown_diameter()
            if crd != '-':
                size = string_concat( size, _(u'Crown diameter'), ': ', crd, '. ' )
                size_ref.append('CRD')
            if size != '':
                self._add_data_object( f, taxon, u'Size', size_ref, size, lang)
            ## Distribution
            distrib = settings.HABITAT_DESCRIPTION
            distrib_ref = ['-']
            if taxon.endemic:
                distrib = distrib + ' (' + taxon._get_field_label('endemic')  + ')'
                distrib_ref = ['END']
            self._add_data_object( f, taxon, u'Distribution', distrib_ref, distrib, lang)
            ## Growth
            growth_rate = taxon.get_growth_rate()
            if growth_rate != '-':
                self._add_data_object( f, taxon, u'Growth', ['GRO'], string_concat( _(u'Growth rate'), ': ', growth_rate), lang)
            ## Associations
            assoc = ''
            if taxon.pollinators:
                assoc = assoc + taxon._get_field_label('pollinators')+': ' + taxon.pollinators
            if taxon.symbiotic_assoc:
                if len(assoc):
                    assoc = assoc + '. '
                assoc = string_concat(assoc, _(u'Symbiotic association'),': ', taxon.symbiotic_details)
            if len(assoc):
                self._add_data_object( f, taxon, u'Associations', ['POL', 'SYM'], assoc, lang)
            ## Dispersal
            dispersal = ''
            d_types = taxon.get_dispersal_types()
            if d_types != '-':
                dispersal = string_concat(_(u'Seed dispersal'),': ', d_types)
            if taxon.dispersers:
                if len(dispersal):
                    dispersal = dispersal + '. '
                dispersal = dispersal + taxon._get_field_label('dispersers')+': '+taxon.dispersers
            if len(dispersal):
                self._add_data_object( f, taxon, u'Dispersal', ['DIS'], dispersal, lang)
            ## Diseases
            if taxon.pests_and_diseases:
                self._add_data_object( f, taxon, u'Diseases', ['PAD'], taxon.pests_and_diseases, lang)
            ## Uses
            if taxon.restoration or taxon.urban_use:
                self._add_data_object( f, taxon, u'Uses', ['-'], taxon.get_use(), lang)
            ## Conservation status
            conservation = ''
            for c_status in taxon.conservationstatus_set.all():
                if len(conservation):
                    conservation = conservation + ', '
                conservation = conservation + c_status.source.acronym + ': ' + c_status.status
            if len(conservation):
                self._add_data_object( f, taxon, u'ConservationStatus', ['-'], conservation, lang)
            ## Reproduction
            repro = ''
            repro_ref = ['-']
            fp = taxon.get_fruiting_period()
            if fp != '-':
                repro = string_concat( _(u'Fruiting period'), ': ', fp, '. ' )
                repro_ref.append('FRP')
            seed_g = taxon.get_seed_gathering()
            if seed_g != '-':
                repro = string_concat( repro, seed_g, '. ' )
                repro_ref.append('SEC')
            if taxon.seed_type is not None:
                repro = string_concat( repro, _(u'Seed type'), ': ', taxon.get_seed_type_display(), '. ' )
                repro_ref.append('SET')
            if taxon.pg_treatment is not None:
                repro = string_concat( repro, taxon._get_field_label('pg_treatment'), ': ', taxon.get_pg_treatment_display(), '. ' )
                repro_ref.append('PGT')
            seedbed = taxon.get_seedbed()
            if seedbed != '-':
                repro = string_concat( repro, _(u'Seedling production'), ': ', seedbed, '. ' )
                repro_ref.append('SDL')
            g_time_lapse = taxon.get_germination_time_lapse()
            if g_time_lapse != '-':
                repro = string_concat( repro, _(u'Germination time lapse'), ': ', g_time_lapse, '. ' )
                repro_ref.append('GET')
            g_rate = taxon.get_germination_rate()
            if g_rate != '-':
                repro = string_concat( repro, _(u'Germination rate'), ': ', g_rate, '. ' )
                repro_ref.append('GER')
            if taxon.light is not None:
                repro = string_concat( repro, _(u'Light requirements'), ': ', taxon.get_light_display(), '. ' )
                repro_ref.append('LIG')
            if len(repro):
                self._add_data_object( f, taxon, u'Reproduction', repro_ref, repro, lang)
            f. write(u"\n\t</taxon>")
        f.write(u"\n</response>")
        f.close()

    def _add_data_object( self, f, taxon, spm_subject, ids, c_content, lang=None ):
        f.write(u"\n\t\t<dataObject>")
        f.write(u"\n\t\t\t<dataType>http://purl.org/dc/dcmitype/Text</dataType>")
        content = u"\n\t\t\t<dc:description"
        if lang is not None:
            f.write(u"\n\t\t\t<dc:language>"+lang+u"</dc:language>")
            content = content + u' xml:lang="'+lang+'"'
        f.write(u"\n\t\t\t<audience>General public</audience>")
        content = content + u'>'+escape(c_content)+u'</dc:description>'
        f.write(u"\n\t\t\t<subject>http://rs.tdwg.org/ontology/voc/SPMInfoItems#"+spm_subject+"</subject>")
        f.write(content)
        refs = taxon.taxondatareference_set.filter(data__in=ids)
        ref_ids = {}
        for ref in refs:
            if ref.reference_id not in ref_ids:
                f.write(u"\n\t\t\t<reference>"+escape(ref.reference.full)+u'</reference>')
                ref_ids[ref.reference_id] = True
        f.write(u"\n\t\t</dataObject>")
    
