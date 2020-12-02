# coding=UTF-8

from app.models import StaticContent, Taxon, TaxonName, TaxonDataReference, COLORS, MONTHS, ROOT_SYSTEMS, CROWN_SHAPES, LIGHT_REQUIREMENTS, SEED_TYPES, FRUIT_TYPES, BARK_TEXTURES, GROWTH_RATE, FOLIAGE_PERSISTENCE, TRUNK_ALIGNMENT, SOIL_TYPES, SEED_DISPERSAL_TYPE, SEED_COLLECTION, PRE_GERMINATION_TREATMENT, ConservationStatus, Interview, TypeOfUse, TaxonUse, Habitat, TaxonHabitat
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils import translation
from django.utils.encoding import force_text
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from django.db.models import Q, F

# General definitions
no_matter_str = _(u'indifferent')
null_boolean_choices = (( -1, no_matter_str ),( 1 , _(u'yes') ),( 0 , _(u'no') ))

# Form classes
class CommonSearchForm(forms.Form):
    month_choices = [(0, no_matter_str)] + list(MONTHS)
    #family_choices = [('NULL', no_matter_str)] + list( Taxon.objects.filter(family__gte=u'a').distinct('family').order_by('family').values_list('family', 'family') )
    #family      = forms.ChoiceField(label=_(u'Family'), initial='NULL', choices=family_choices)
    # uses
    use_choices = TypeOfUse.objects.all().order_by('path')
    my_use_choices = []
    for choice in use_choices:
        my_use_choices.append([choice.id, str(choice)])
    uses = forms.MultipleChoiceField(label=_(u'Specific use'), choices=my_use_choices)
    # Rarity
    rare = forms.BooleanField(label=_(u'Rare'))
    # Endemism
    endemic = forms.BooleanField(label=_(u'Endemic'))
    # Growth rate
    gr_slow     = forms.BooleanField(label=_(u'Slow'))
    gr_moderate = forms.BooleanField(label=_(u'Moderate'))
    gr_fast     = forms.BooleanField(label=_(u'Fast'))
    # Pruning
    pruning = forms.ChoiceField(label=_(u'Requires pruning'), initial=-1, choices=null_boolean_choices)
    # Flowering month
    fl_month = forms.ChoiceField(label=_(u'With flower in month'), initial=0, choices=month_choices)
    fr_month = forms.ChoiceField(label=_(u'With fruits in month'), initial=0, choices=month_choices)
    # Root system
    root_system_choices = [('NULL', no_matter_str)] + list(ROOT_SYSTEMS)
    r_type = forms.ChoiceField(label=_(u'Root system'), initial='NULL', choices=root_system_choices)
    # Foliage persistence
    fo_evergreen     = forms.BooleanField(label=_(u'Evergreen'))
    fo_semideciduous = forms.BooleanField(label=_(u'Semi-deciduous'))
    fo_deciduous     = forms.BooleanField(label=_(u'Deciduous'))
    # Light requirement
    light_requirement_choices = [('NULL', no_matter_str)] + list(LIGHT_REQUIREMENTS)
    light = forms.ChoiceField(label=_(u'Light requirements'), initial='NULL', choices=light_requirement_choices)
    # Height
    min_height = forms.IntegerField(initial=None, widget=forms.TextInput(attrs={'size':'3'}))
    max_height = forms.IntegerField(initial=None, widget=forms.TextInput(attrs={'size':'3'}))
    # Crown diameter
    cr_min_diameter = forms.IntegerField(initial=None, widget=forms.TextInput(attrs={'size':'3'}))
    cr_max_diameter = forms.IntegerField(initial=None, widget=forms.TextInput(attrs={'size':'3'}))
    # Terrain drainage
    wetland = forms.BooleanField(label=_(u'Wetland'))
    dry     = forms.BooleanField(label=_(u'Well-drained'))
    # Type of dispersion
    dt_anemochorous = forms.BooleanField(label=_(u'Anemochorous'))
    dt_autochorous  = forms.BooleanField(label=_(u'Autochorous'))
    dt_barochorous  = forms.BooleanField(label=_(u'Barochorous'))
    dt_hydrochorous = forms.BooleanField(label=_(u'Hydrochorous'))
    dt_zoochorous   = forms.BooleanField(label=_(u'Zoochorous'))

class UrbanForestrySearchForm(CommonSearchForm):
    color_choices = [(0, no_matter_str)] + list(COLORS)
    crown_shape_choices = [('NULL', no_matter_str)] + list(CROWN_SHAPES)
    toxic    = forms.ChoiceField(label=_(u'Toxic or allergenic'), initial=-1, choices=null_boolean_choices)
    thorns   = forms.ChoiceField(label=_(u'Thorns or spines'), initial=-1, choices=null_boolean_choices)
    color    = forms.ChoiceField(label=_(u'Flowering color'), initial=0, choices=color_choices)
    cr_shape = forms.ChoiceField(label=_(u'Crown shape'), initial='NULL', choices=crown_shape_choices)
    # Special features
    h_flowers   = forms.BooleanField(label=_(u'Flowers'))
    h_leaves    = forms.BooleanField(label=_(u'Leaves'))
    h_fruits    = forms.BooleanField(label=_(u'Fruits'))
    h_crown     = forms.BooleanField(label=_(u'Crown'))
    h_bark      = forms.BooleanField(label=_(u'Bark'))
    h_seeds     = forms.BooleanField(label=_(u'Seeds'))
    h_wood      = forms.BooleanField(label=_(u'Wood'))
    h_roots     = forms.BooleanField(label=_(u'Roots'))
    # Trunk alignement
    tr_straight    = forms.BooleanField(label=_(u'Straight'))
    tr_sl_inclined = forms.BooleanField(label=_(u'Slightly inclined'))
    tr_inclined    = forms.BooleanField(label=_(u'Inclined'))
    tr_sl_crooked  = forms.BooleanField(label=_(u'Slightly crooked'))
    tr_crooked     = forms.BooleanField(label=_(u'Crooked'))
    # Conservation status
    status_choices = [('NULL', no_matter_str)] + [(c['status'], c['status']) for c in ConservationStatus.objects.filter(taxon__urban_use=True).values('status').order_by('status').distinct()]
    status = forms.ChoiceField(label=_(u'Conservation status'), initial='NULL', choices=status_choices)
    # Pollination
    pollinators = forms.ChoiceField(label=_(u'Pollinators'), initial=-1, choices=null_boolean_choices)

class RestorationSearchForm(CommonSearchForm):
    toxic = forms.ChoiceField(label=_(u'Toxic or allergenic'), initial=-1, choices=null_boolean_choices)
    symb_assoc = forms.ChoiceField(label=_(u'Symbiotic association with roots'), initial=-1, choices=null_boolean_choices)
    # Successional group
    sg_pioneer         = forms.BooleanField(label=_(u'Pioneer'))
    sg_early_secondary = forms.BooleanField(label=_(u'Early secondary'))
    sg_late_secondary  = forms.BooleanField(label=_(u'Late secondary'))
    sg_climax          = forms.BooleanField(label=_(u'Climax'))
    # Conservation status
    status_choices = [('NULL', no_matter_str)] + [(c['status'], c['status']) for c in ConservationStatus.objects.filter(taxon__restoration=True).values('status').order_by('status').distinct()]
    status = forms.ChoiceField(label=_(u'Conservation status'), initial='NULL', choices=status_choices)
    # Pre-germination treatment
    pg_no_need    = forms.BooleanField(label=_(u'No need for treatment'))
    pg_thermal    = forms.BooleanField(label=_(u'Thermal treatment'))
    pg_chemical   = forms.BooleanField(label=_(u'Chemical treatment'))
    pg_water      = forms.BooleanField(label=_(u'Immersion in water'))
    pg_mechanical = forms.BooleanField(label=_(u'Mechanical scarification'))
    pg_combined   = forms.BooleanField(label=_(u'Combined treatments'))
    pg_other      = forms.BooleanField(label=_(u'Other'))
    # Seed type
    seed_type_choices = [('NULL', no_matter_str)] + list(SEED_TYPES)
    s_type = forms.ChoiceField(label=_(u'Seed type'), initial='NULL', choices=seed_type_choices)
    # Germination rate
    seed_gmin_rate = forms.IntegerField(initial=None, widget=forms.TextInput(attrs={'size':'3'}))
    seed_gmax_rate = forms.IntegerField(initial=None, widget=forms.TextInput(attrs={'size':'3'}))

class SilvicultureSearchForm(CommonSearchForm):
    # Successional group
    sg_pioneer         = forms.BooleanField(label=_(u'Pioneer'))
    sg_early_secondary = forms.BooleanField(label=_(u'Early secondary'))
    sg_late_secondary  = forms.BooleanField(label=_(u'Late secondary'))
    sg_climax          = forms.BooleanField(label=_(u'Climax'))
    # DBH
    min_dbh   = forms.IntegerField(initial=None, widget=forms.TextInput(attrs={'size':'3'}))
    max_dbh   = forms.IntegerField(initial=None, widget=forms.TextInput(attrs={'size':'3'}))
    # Diseases
    diseases = forms.ChoiceField(label=_(u'Pests and diseases'), initial=-1, choices=null_boolean_choices)
    # Pollination
    pollinators = forms.ChoiceField(label=_(u'Pollinators'), initial=-1, choices=null_boolean_choices)
    # Habitats
    habitat_choices = Habitat.objects.all().order_by('path')
    my_habitat_choices = []
    for choice in habitat_choices:
        my_habitat_choices.append([choice.id, str(choice)])
    habitats = forms.MultipleChoiceField(label=ugettext(u'Biome')+'/'+ugettext(u'Fitofisionomy'), choices=my_habitat_choices)
    # Density
    min_density = forms.IntegerField(initial=None, widget=forms.TextInput(attrs={'size':'3'}))
    max_density = forms.IntegerField(initial=None, widget=forms.TextInput(attrs={'size':'3'}))
    # Has MAI curve
    has_mai_curve = forms.ChoiceField(label=_(u'Has mean annual increment curve'), initial=-1, choices=null_boolean_choices)

# Internal methods
def _handle_language(request):
    if request.GET.has_key('setlang'):
        available_langs = []
        for lang in settings.LANGUAGES:
            available_langs.append(lang[0])
        if request.GET['setlang'] in available_langs:
            translation.activate( request.GET['setlang'] )
            request.session['django_language'] = request.GET['setlang']
    else:
        if not request.session.has_key('django_language'):
            translation.activate( settings.LANGUAGE_CODE )
            request.session['django_language'] = settings.LANGUAGE_CODE

def _add_and_conditions(request, qs, fields):
    for field in fields:
        if ( request.GET.has_key(field)):
            kwargs = {'%s' % (field): True}
            qs = qs.filter(**kwargs)
    return qs

def _add_or_conditions(request, qs, fields):
    new_filter = None
    for field in fields:
        if ( request.GET.has_key(field)):
            kwargs = {'%s' % (field): True}
            if new_filter is None:
                new_filter = Q(**kwargs)
            else:
                new_filter = new_filter | Q(**kwargs)
    if new_filter is not None:
        qs = qs.filter(new_filter)
    return qs

def _add_interval_condition(request, qs, min_field, max_field):
    if ( request.GET.has_key(min_field)):
        ok_min = False
        min_val = request.GET.get(min_field)
        if not isinstance( min_val, int ):
            if min_val.isdigit():
                min_val = int(min_val)
                ok_min = True
        else:
            ok_min = True
        if ok_min:
            kwargs = {'%s__gte' % (min_field): min_val}
            qs = qs.filter(**kwargs)
    if ( request.GET.has_key(max_field)):
        ok_max = False
        max_val = request.GET.get(max_field)
        if not isinstance( max_val, int ):
            if max_val.isdigit():
                max_val = int(max_val)
                ok_max = True
        else:
            ok_max = True
        if ok_max:
            kwargs = {'%s__lte' % (max_field): max_val}
            qs = qs.filter(**kwargs)
    return qs

def _add_single_field_interval_condition(request, qs, field, min_param, max_param):
    if ( request.GET.has_key(min_param)):
        ok_min = False
        min_val = request.GET.get(min_param)
        if not isinstance( min_val, int ):
            if min_val.isdigit():
                min_val = int(min_val)
                ok_min = True
        else:
            ok_min = True
        if ok_min:
            kwargs = {'%s__gte' % (field): min_val}
            qs = qs.filter(**kwargs)
    if ( request.GET.has_key(max_param)):
        ok_max = False
        max_val = request.GET.get(max_param)
        if not isinstance( max_val, int ):
            if max_val.isdigit():
                max_val = int(max_val)
                ok_max = True
        else:
            ok_max = True
        if ok_max:
            kwargs = {'%s__lte' % (field): max_val}
            qs = qs.filter(**kwargs)
    return qs

def _add_month_condition(request, qs, param, min_field, max_field):
    ok = False
    val = request.GET.get(param)
    if val in ('0', 0):
        return qs
    if not isinstance( val, int ):
        if val.isdigit():
            val = int(val)
            ok = True
    else:
        ok = True
    if ok:
        kwargs_in = {'%s__gte' % (max_field): F(min_field)}
        kwargs_out = {'%s__gt' % (min_field): F(max_field)}
        kwargs1 = {'%s__lte' % (min_field): val}
        kwargs2 = {'%s__gte' % (max_field): val}
        inside = Q(**kwargs_in) & Q(**kwargs1) & Q(**kwargs2)
        outside = Q(**kwargs_out) & (Q(**kwargs1) | Q(**kwargs2))
        qs = qs.filter(inside | outside)
    return qs

def _json_raw_encode(data):
    """
    Return the specified data encoded in json.
    """
    import types
    from django.core import serializers
    from json.encoder import JSONEncoder
    if type(data) is types.InstanceType: # assuming a Django object
        json_serializer = serializers.get_serializer("json")()
        return json_serializer.serialize(data, ensure_ascii=False)
    else:
        return JSONEncoder().encode(data)

def _add_link(abs_uri, link, page_number, label, params):
    sep = u', ' if len(link) > 0 else u''
    params = params + u'&' if len(params) > 0 else u''
    return u'%s%s<%s?%spage=%d>; rel="%s"' % (link, sep, str(abs_uri), params, page_number, label)

def _pdf_for_species_list( qs ):
    """
    Generate a PDF for a species list retrieved by the provided query.
    """
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_LEFT
    from reportlab.rl_config import defaultPageSize
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    PAGE_HEIGHT=defaultPageSize[1]
    PAGE_WIDTH=defaultPageSize[0]
    styles = getSampleStyleSheet()
    styles.add( ParagraphStyle(name='Left', alignment=TA_LEFT, spaceAfter=20) )
    
    response = HttpResponse( content_type='application/pdf' )
    response['Content-Disposition'] = 'attachment; filename="search_result.pdf"'

    # Create the PDF object, using the response object as its "file."
    doc = SimpleDocTemplate( response, topMargin=0.2*inch, showBoundary=0 )
    Story = [Spacer(1,2*inch)]
    style = styles['Left']
    px = 7.0
    py = 0.75

    def myFirstPage( canvas, doc ):
        canvas.saveState()
        canvas.setFont( 'Times-Roman', 14 )
        canvas.drawString( 1.1*inch, 10.5*inch, _(u'Search Results') )
        canvas.setFont( 'Times-Roman', 9 )
        canvas.drawString( px*inch, py*inch,"p. %d" % (doc.page) )
        canvas.restoreState()
    def myLaterPages( canvas, doc ):
        canvas.saveState()
        canvas.setFont( 'Times-Roman', 9 )
        canvas.drawString( px*inch, py*inch,"p. %d" % (doc.page) )
        canvas.restoreState()

    # Add content
    for sp in qs:
        myp = '<i>' + sp.genus + ' ' + sp.species + '</i>'
        if sp.subspecies is not None and len(sp.subspecies) > 0:
            myp += ' var. <i>' + sp.subspecies + '</i>'
        popnames = sp.get_popular_names().values_list('name', flat=True)
        sep = ', '
        if len(popnames) > 0:
            myp += ' <font size="8" color="gray">('+ sep.join(popnames) +')</font>'
        if sp.has_pictures:
            myp += ' <img src="'+ settings.STATIC_ROOT + 'images/photo.png" width="10" height="8" valign="middle"/>'
        if sp.has_history():
            myp += ' <img src="'+ settings.STATIC_ROOT + 'images/microphone.png" width="10" height="10"/>'
        if sp.ethno_notes is not None and len(sp.ethno_notes) > 0:
            myp += ' <img src="'+ settings.STATIC_ROOT + 'images/hand.png" width="10" height="10"/>'
        synonyms = sp.get_synonyms().values_list('name', flat=True)
        if len(synonyms) > 0:
            myp += '<br/><font size="8">' + ugettext(u'Synonyms') + ': <i>' + sep.join(synonyms) + '</i></font>'
        p = Paragraph( myp, style )
        Story.append( p )
    
    doc.build( Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages )
    
    return response

def _pdf_for_species_page( taxon, refs, citations ):
    """
    Generate a PDF for the species page.
    """
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
    from reportlab.rl_config import defaultPageSize
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    PAGE_HEIGHT=defaultPageSize[1]
    PAGE_WIDTH=defaultPageSize[0]
    styles = getSampleStyleSheet()
    styles.add( ParagraphStyle(name='Left', alignment=TA_LEFT, spaceAfter=20) )
    styles.add( ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, spaceAfter=20) )
    
    response = HttpResponse( content_type='application/pdf' )
    file_name = taxon.genus+'_'+taxon.species
    if taxon.subspecies is not None and len(taxon.subspecies) > 0:
        file_name += '_'+taxon.subspecies
    response['Content-Disposition'] = 'attachment; filename="'+file_name+'.pdf"'

    # Create the PDF object, using the response object as its "file."
    doc = SimpleDocTemplate( response, topMargin=0.2*inch, showBoundary=0 )
    Story = []
    style = styles['Left']
    px = 7.0
    py = 0.75

    def myPage( canvas, doc ):
        canvas.saveState()
        canvas.setFont( 'Times-Roman', 9 )
        canvas.drawString( px*inch, py*inch,"p. %d" % (doc.page) )
        canvas.restoreState()
    def _appendSection( story, title ):
        story.append( Paragraph( '<font size="13"><u>'+title+'</u></font>', styles['Justify'] ) )
    def _appendLabelAndContent( story, label, content, key, style='Left' ):
        p = '<b>'+ugettext(label)+':</b> '
        if not content:
            content = '-'
        p += force_text( content )
        if refs.has_key( key ):
            p += '<sup>' + refs[key] + '</sup>'
        Story.append( Paragraph( p, styles[style] ) )
    def _appendDetails( story, content ):
        if content:
            Story.append( Paragraph( content, styles['Justify'] ) )

    # Add content
    subsp = ''
    if taxon.subspecies is not None and len(taxon.subspecies) > 0:
        subsp = 'var. <i>' + taxon.subspecies + '</i> '
    myp = '<font size="14"><i>' + taxon.genus + ' ' + taxon.species + '</i> ' + subsp + taxon.author + '</font>'
    popnames = taxon.get_popular_names().values_list('name', flat=True)
    sep = ', '
    if len(popnames) > 0:
        myp += '<br/><br/><font size="11">('+ sep.join(popnames) +')</font>'
    p = Paragraph( myp, style )
    Story.append( p )
    _appendLabelAndContent( Story, ugettext(u'Family'), taxon.family, '' )
    synonyms = taxon.get_synonyms().values_list('name', flat=True)
    if len(synonyms) > 0:
        Story.append( Paragraph( '<font size="10"><b>' + ugettext(u'Synonyms') + ':</b> <i>' + sep.join(synonyms) + '</i></font>', style ) )
    t = '<b>'+ugettext(u'Endemic')+':</b> '
    c = force_text( taxon.get_endemic() )
    if c == 'None':
        c = '-'
    t += c
    if refs.has_key( 'END' ):
        t += '<sup>' + refs['END'] + '</sup>'
    #t += '    <b>'+ugettext(u'Rare')+':</b> '
    #r = force_text( taxon.get_rare() )
    #if r == 'None':
    #    r = '-'
    #t += r
    #m = taxon.max_density
    #if m is not None:
    #    t += str(m) + ugettext(u' individuals per hectare')
    #if refs.has_key( 'RAR' ):
    #    t += '<sup>' + refs['RAR'] + '</sup>'
    Story.append( Paragraph( t, styles['Left'] ) )
    _appendLabelAndContent( Story, ugettext(u'Biome')+'/'+ugettext(u'Fitofisionomy'), taxon.get_habitats(), 'HAB' )
    conservation_recs = taxon.conservationstatus_set.all()
    if len( conservation_recs ) > 0:
        cs = ''
        for rec in conservation_recs:
            if len( cs ) > 0:
                cs += ', '
            cs += rec.status + ' (' + rec.source.acronym + ')'
        _appendLabelAndContent( Story, ugettext(u'Conservation status'), cs, '' )
    #_appendLabelAndContent( Story, ugettext(u'Special features'), taxon.get_special_features(), 'SPE' )
    _appendLabelAndContent( Story, ugettext(u'Uses'), force_text(taxon.get_use()), '' )
    _appendDetails( Story, taxon.description )
    #########################################################
    _appendSection( Story, ugettext(u'Ethnobotany')+' '+ugettext(u'and')+' '+ugettext(u'History') )
    _appendDetails( Story, taxon.ethno_notes )
    _appendLabelAndContent( Story, ugettext(u'Specific uses'), taxon.get_specific_uses(), 'USE' )
    #########################################################
    _appendSection( Story, ugettext(u'General features') )
    height = taxon.get_height()
    dbh = taxon.get_dbh()
    c = ''
    if height:
        c += ugettext(u'height') + ' ' + str(height)
    else:
        if dbh is None:
            c += '-'
    if dbh:
        if height:
            c += ' '
        c += ugettext(u'DBH') + ' ' + str(dbh)
    _appendLabelAndContent( Story, ugettext(u'Tree size')          , c                               , 'SIZ' )
    _appendLabelAndContent( Story, ugettext(u'Flowering color')    , taxon.get_fl_color_display()    , 'FLC' )
    _appendDetails( Story, taxon.fl_color_details )
    _appendLabelAndContent( Story, ugettext(u'Growth rate')        , taxon.get_growth_rate()         , 'GRO' )
    _appendDetails( Story, taxon.gr_comments )
    _appendLabelAndContent( Story, ugettext(u'Foliage persistence'), taxon.get_foliage_persistence() , 'FOL' )
    _appendLabelAndContent( Story, ugettext(u'Root system')        , taxon.get_r_type_display()      , 'ROT' )
    _appendLabelAndContent( Story, ugettext(u'Crown shape')        , taxon.get_cr_shape_display()    , 'CRS' )
    _appendLabelAndContent( Story, ugettext(u'Crown diameter')     , taxon.get_crown_diameter()      , 'CRD' )
    _appendLabelAndContent( Story, ugettext(u'Trunk alignment')    , taxon.get_trunk_alignment()     , 'TRA' )
    _appendLabelAndContent( Story, ugettext(u'Bark texture')       , taxon.get_bark_texture_display(), 'BRT' )
    _appendLabelAndContent( Story, ugettext(u'Fruit type')         , taxon.get_fruit_classification(), 'FRT' )
    #########################################################
    _appendSection( Story, ugettext(u'Care') )
    _appendLabelAndContent( Story, ugettext(u'Pruning')            , taxon.get_pruning()            , 'PRU' )
    _appendLabelAndContent( Story, ugettext(u'Pests and diseases') , taxon.pests_and_diseases       , 'PAD', 'Justify' )
    _appendLabelAndContent( Story, ugettext(u'Thorns or spines')   , taxon.get_thorns_or_spines()   , 'TOS' )
    _appendLabelAndContent( Story, ugettext(u'Toxic or allergenic'), taxon.get_toxic_or_allergenic(), 'TOA' )
    _appendLabelAndContent( Story, ugettext(u'Terrain drainage')   , taxon.get_terrain_drainage()   , 'TER' )
    _appendDetails( Story, taxon.terrain_details )
    #########################################################
    _appendSection( Story, ugettext(u'Ecology')+' '+ugettext(u'and')+' '+ugettext(u'Reproduction') )
    _appendLabelAndContent( Story, ugettext(u'Successional group')   , taxon.get_successional_group(), 'SUG' )
    _appendLabelAndContent( Story, ugettext(u'Pollinators')          , taxon.pollinators             , 'POL' )
    _appendLabelAndContent( Story, ugettext(u'Flowering period')     , taxon.get_flowering_period()  , 'FLP' )
    _appendDetails( Story, taxon.fl_details )
    _appendLabelAndContent( Story, ugettext(u'Seed dispersal')       , taxon.get_dispersal_types()   , 'SED' )
    _appendLabelAndContent( Story, ugettext(u'Dispersion agents')    , taxon.dispersers              , 'DIS' )
    _appendLabelAndContent( Story, ugettext(u'Fruiting period')      , taxon.get_fruiting_period()   , 'FRP' )
    _appendDetails( Story, taxon.fr_details )
    _appendLabelAndContent( Story, ugettext(u'Symbiotic association with roots'), taxon.get_symbiotic_assoc()   , 'SYM' )
    _appendDetails( Story, taxon.symbiotic_details )
    #########################################################
    _appendSection( Story, ugettext(u'Seedling production') )
    _appendLabelAndContent( Story, ugettext(u'Seed collection')           , taxon.get_seed_gathering()          , 'SEC' )
    _appendDetails( Story, taxon.seed_collection )
    _appendLabelAndContent( Story, ugettext(u'Seed type')                 , taxon.get_seed_type_display()       , 'SET' )
    _appendLabelAndContent( Story, ugettext(u'Pre-germination treatment') , taxon.get_pregermination_treatment(), 'PGT' )
    _appendDetails( Story, taxon.pg_details )
    _appendLabelAndContent( Story, ugettext(u'Seedling production')       , taxon.get_seedbed()                 , 'SDL' )
    _appendDetails( Story, taxon.sl_details )
    _appendLabelAndContent( Story, ugettext(u'Germination time lapse')    , taxon.get_germination_time_lapse()  , 'GET' )
    _appendLabelAndContent( Story, ugettext(u'Germination rate')          , taxon.get_germination_rate()        , 'GER' )
    c = taxon.seeds_per_weight
    if c:
        c = str(c) + '/kg'
    _appendLabelAndContent( Story, ugettext(u'Number of seeds per weight'), c                                   , 'SPW' )
    _appendLabelAndContent( Story, ugettext(u'Light requirements')        , taxon.get_light_display()           , 'LIG' )
    _appendDetails( Story, taxon.light_details )
    #########################################################
    if taxon.silviculture:
        _appendSection( Story, ugettext(u'Wood information') )
        _appendDetails( Story, taxon.wood_general_info )
        d = taxon.wood_density
        if d:
            d = str(d) + 'kg/m<sup>3</sup> '
            _appendLabelAndContent( Story, ugettext(u'Density'), d, 'WOO' )
        _appendLabelAndContent( Story, ugettext(u'Has mean annual increment curve'), taxon.get_has_mai_curve(), 'WOO' )
        _appendLabelAndContent( Story, ugettext(u'Has current annual increment curve'), taxon.get_has_cai_curve(), 'WOO' )
    #########################################################
    _appendSection( Story, ugettext(u'Bibliography') )
    for citation in citations:
        Story.append( Paragraph( '<font size="8"><sup>'+citation[0]+'</sup> '+citation[1]+'</font>', styles['Left'] ) )

    doc.build( Story, onFirstPage=myPage, onLaterPages=myPage )
    
    return response

def _to_dict(model_vocabulary):
    my_dict = {}
    for el in model_vocabulary:
        my_dict[el[0]] = ugettext(el[1])
    return my_dict

def _add_references(request, obj, key, refs):
    if request.GET.has_key('references') and refs.has_key(key) and len(refs[key]) > 0:
        obj['references'] = refs[key].split(',')

# View methods
def handler404( request ):
    "404 page"
    c = RequestContext(request, {'base_template':settings.BASE_TEMPLATE})
    possible_templates = ['my_404.html', '404.html']
    return render( request, possible_templates, context_instance=c, content_type='text/html; charset=utf-8', status=404 )

def handler500( request ):
    "500 page"
    c = RequestContext(request, {'base_template':settings.BASE_TEMPLATE} )
    possible_templates = ['my_500.html', '500.html']
    return render( request, possible_templates, context_instance=c, content_type='text/html; charset=utf-8', status=500 )

def index(request):
    'Index page'
    return show_page(request, 'main')

def show_help(request, content_id):
    'Generic method to retrieve help content stored in the database'
    _handle_language( request )
    options = StaticContent.objects.filter(code=content_id)
    if len(options) == 0:
        raise Http404
    try:
        h = options.get(lang=translation.get_language())
    except StaticContent.DoesNotExist:
        # Get first
        h = options[0]
    return HttpResponse(h.content)

def show_page(request, page_code):
    'Generic method to show a static page stored in the database'
    _handle_language( request )
    pages = StaticContent.objects.filter(code=page_code)
    if len(pages) == 0:
        raise Http404
    try:
        p = pages.get(lang=translation.get_language())
    except StaticContent.DoesNotExist:
        # Get first
        p = pages[0]
    c = {'page': p, 'base_template': settings.BASE_TEMPLATE}
    possible_templates = ['my_page.html', 'page.html']
    template = loader.select_template( possible_templates )
    return HttpResponse( template.render(c, request) )

def about(request):
    return show_page(request, 'about')

def methods(request):
    return show_page(request, 'methods')

def ethno_overview(request):
    return show_page(request, 'ethno_overview')

def ethno_results(request):
    return show_page(request, 'ethno_results')

def hist_overview(request):
    return show_page(request, 'hist_overview')

def hist_results(request):
    _handle_language( request )
    interviews = Interview.objects.all().order_by('title')
    # Fake page, in case template has some logic based on page code
    page = StaticContent(code='hist_results')
    c = {'base_template': settings.BASE_TEMPLATE, 'page': page, 'interviews': interviews}
    possible_templates = ['my_hist_results.html', 'hist_results.html']
    template = loader.select_template( possible_templates )
    return HttpResponse( template.render(c, request) )

def faq(request):
    return show_page(request, 'faq')

def show_species(request, species_id, ws=False):
    'Display data about a species'
    _handle_language( request )
    if not isinstance( species_id, int ):
        if species_id.isdigit():
            species_id = int(species_id)
        else:
            raise Http404
    try:
        taxon = Taxon.objects.get(pk=species_id)
    except Taxon.DoesNotExist:
        raise Http404
    # Bibliographic references
    #data = ('RAR','END','SPE','SUG','GRO','PRU','FLP','FLC','POL','SED','DIS','FRT','SYM','ROT','FOL','CRD','CRS','BRT','TRA','SIZ','TOS','TOA','PAD','FRP','SEC','SET','PGT','SDL','GET','GER','SPW','LIG')
    ctrl = {}      # reference_id => number
    citations = [] # list of(ref_number, citation)
    numbers = {}   # data_id => ref_numbers
    refs = taxon.taxondatareference_set.all().order_by('data')
    cnt = 1
    for ref in refs:
        if not ctrl.has_key(ref.reference_id):
            ctrl[ref.reference_id] = str(cnt)
            citations.append( (str(cnt), ref.reference.full) )
            cnt = cnt + 1
    for ref in refs:
        if request.GET.has_key('pdf') or ws:
            if numbers.has_key(ref.data):
                numbers[ref.data] = numbers[ref.data] + ',' + ctrl[ref.reference_id]
            else:
                numbers[ref.data] = ctrl[ref.reference_id]
        else:
            if numbers.has_key(ref.data):
                numbers[ref.data] = numbers[ref.data] + ',' + '<a href="#ref-'+ctrl[ref.reference_id]+'" onclick="fr_highlight(' + ctrl[ref.reference_id] + ');">' + ctrl[ref.reference_id] + '</a>'
            else:
                numbers[ref.data] = '<a href="#ref-'+ctrl[ref.reference_id]+'" onclick="fr_highlight(' + ctrl[ref.reference_id] + ');">' + ctrl[ref.reference_id] + '</a>'
    # Points
    orig_points = []
    for occ in taxon.taxonoccurrence_set.all():
        orig_points.append({'x':occ.get_decimal_long(), 'y':occ.get_decimal_lat(), 'label':occ.label})
    if request.GET.has_key('pdf'):
        if request.GET['pdf'] not in ("1", ""):
            # Someone may attempt to get server information by messing with this parameter
            return redirect('http://www.ic3.gov/about/')
        return _pdf_for_species_page( taxon, numbers, citations )
    points = _json_raw_encode( orig_points )
    # Help content
    help_entries = StaticContent.objects.filter(code__startswith='HELP-').values_list('code', flat=True)
    # Web service
    if ws:
        from json.encoder import JSONEncoder
        data = {'fullname':taxon.label}
        if taxon.family:
            data['family'] = taxon.family
        synonyms = taxon.get_synonyms().values_list('name', flat=True)
        if len(synonyms) > 0:
            synonyms_json = []
            for synonym in synonyms:
                synonyms_json.append(synonym)
            data['synonyms'] = synonyms_json
        popnames = taxon.get_popular_names().values_list('name', flat=True)
        if len(popnames) > 0:
            popnames_json = []
            for popname in popnames:
                popnames_json.append(popname)
            data['common_names'] = popnames_json
        if taxon.description:
            data['description'] = taxon.description
        if taxon.endemic is not None:
            endemism = {}
            endemism['endemic'] = taxon.endemic
            _add_references(request, endemism, 'END', numbers)
            data['endemism'] = endemism
        specific_uses = taxon.get_specific_uses()
        if len(specific_uses) > 0:
            uses = {}
            uses['specific_uses'] = specific_uses
            _add_references(request, uses, 'USE', numbers)
            data['uses'] = uses
        # Points
        # ------
        if request.GET.has_key('points'):
            data['points'] = orig_points
        # General features
        # ----------------
        if request.GET.has_key('features'):
            features = {}
            # Tree size
            if taxon.min_height or taxon.max_height or taxon.min_dbh or taxon.max_dbh:
                size = {}
                if taxon.min_height or taxon.max_height:
                    height = {}
                    if taxon.min_height:
                        height['min'] = '%.1f' % taxon.min_height
                    if taxon.max_height:
                        height['max'] = '%.1f' % taxon.max_height
                    size['height'] = height
                if taxon.min_dbh or taxon.max_dbh:
                    dbh = {}
                    if taxon.min_dbh:
                        dbh['min'] = '%.1f' % taxon.min_dbh
                    if taxon.max_height:
                        dbh['max'] = '%.1f' % taxon.max_dbh
                    size['dbh'] = dbh
                _add_references(request, size, 'SIZ', numbers)
                features['size'] = size
            # Flowering color
            if taxon.fl_color is not None or taxon.fl_color_details:
                fl_color = {}
                if taxon.fl_color is not None:
                    fl_color['color'] = taxon.fl_color
                if taxon.fl_color_details:
                    fl_color['details'] = taxon.fl_color_details
                _add_references(request, fl_color, 'FLC', numbers)
                features['flower'] = fl_color
            # Growth rate
            if taxon.gr_slow or taxon.gr_moderate or taxon.gr_fast or taxon.gr_comments:
                growth = {}
                if taxon.gr_slow or taxon.gr_moderate or taxon.gr_fast:
                    growth['rate'] = []
                    if taxon.gr_slow:
                        growth['rate'].append('S')
                    if taxon.gr_moderate:
                        growth['rate'].append('M')
                    if taxon.gr_fast:
                        growth['rate'].append('F')
                if taxon.gr_comments:
                    growth['details'] = taxon.gr_comments
                _add_references(request, growth, 'GRO', numbers)
                features['growth'] = growth
            # Foliage persistence
            if taxon.fo_evergreen or taxon.fo_semideciduous or taxon.fo_deciduous:
                fp = {}
                fp['foliage_persistence'] = []
                if taxon.fo_evergreen:
                    fp['foliage_persistence'].append('E')
                if taxon.fo_semideciduous:
                    fp['foliage_persistence'].append('S')
                if taxon.fo_deciduous:
                    fp['foliage_persistence'].append('D')
                _add_references(request, fp, 'FOL', numbers)
                features['leaves'] = fp
            # Root system
            if taxon.r_type:
                root = {}
                root['type'] = taxon.r_type
                _add_references(request, root, 'ROT', numbers)
                features['root'] = root
            # Crown shape & diameter
            if taxon.cr_shape or taxon.cr_min_diameter or taxon.cr_max_diameter:
                crown = {}
                if taxon.cr_shape:
                    shape = {}
                    shape['classification'] = taxon.cr_shape
                    _add_references(request, shape, 'CRS', numbers)
                    crown['shape'] = shape
                if taxon.cr_min_diameter or taxon.cr_max_diameter:
                    diameter = {}
                    if taxon.cr_min_diameter:
                        diameter['min'] = taxon.cr_min_diameter
                    if taxon.cr_max_diameter:
                        diameter['max'] = taxon.cr_max_diameter
                    _add_references(request, diameter, 'CRD', numbers)
                    crown['diameter'] = diameter
                features['crown'] = crown
            # Trunk alignment
            if taxon.tr_straight or taxon.tr_sl_inclined or taxon.tr_inclined or taxon.tr_sl_crooked or taxon.tr_crooked:
                trunk = {}
                trunk['alignment'] = []
                if taxon.tr_straight:
                    trunk['alignment'].append('1')
                if taxon.tr_sl_inclined:
                    trunk['alignment'].append('2')
                if taxon.tr_inclined:
                    trunk['alignment'].append('3')
                if taxon.tr_sl_crooked:
                    trunk['alignment'].append('4')
                if taxon.tr_crooked:
                    trunk['alignment'].append('5')
                _add_references(request, trunk, 'TRA', numbers)
                features['trunk'] = trunk
            # Bark texture
            if taxon.bark_texture:
                bark = {}
                bark['texture'] = taxon.bark_texture
                _add_references(request, bark, 'BRT', numbers)
                features['bark'] = bark
            # Fruit type
            if taxon.fr_type:
                fruit = {}
                fruit['type'] = taxon.fr_type
                _add_references(request, fruit, 'FRT', numbers)
                features['fruit'] = fruit
             # Add data 
            data['features'] = features
        # Care
        # ----
        if request.GET.has_key('care'):
            care = {}
            # Pruning
            if taxon.pruning is not None:
                pruning = {}
                pruning['indication'] = taxon.pruning
                _add_references(request, pruning, 'PRU', numbers)
                care['pruning'] = pruning
            # Pests and diseases
            if taxon.pests_and_diseases:
                pests_and_diseases = {}
                pests_and_diseases['information'] = taxon.pests_and_diseases
                _add_references(request, pests_and_diseases, 'PAD', numbers)
                care['pests_and_diseases'] = pests_and_diseases
            # Thorns or spines
            if taxon.thorns_or_spines is not None:
                thorns_or_spines = {}
                thorns_or_spines['presence'] = taxon.thorns_or_spines
                _add_references(request, thorns_or_spines, 'TOS', numbers)
                care['thorns_or_spines'] = thorns_or_spines
            # Toxic or allergenic
            if taxon.toxic_or_allergenic is not None:
                toxic_or_allergenic = {}
                toxic_or_allergenic['presence'] = taxon.toxic_or_allergenic
                _add_references(request, toxic_or_allergenic, 'TOA', numbers)
                care['toxic_or_allergenic'] = toxic_or_allergenic
            # Terrain drainage
            if taxon.wetland or taxon.dry or taxon.terrain_details:
                terrain = {}
                if taxon.wetland or taxon.dry:
                    terrain['type'] = []
                    if taxon.wetland       :
                        terrain['type'].append('W')
                    if taxon.dry:
                        terrain['type'].append('D')
                if taxon.terrain_details:
                    terrain['details'] = taxon.terrain_details
                _add_references(request, terrain, 'TER', numbers)
                care['terrain'] = terrain
            # Add data 
            data['care'] = care
        # Ecology & reproduction
        # ----------------------
        if request.GET.has_key('ecology'):
            ecology = {}
            # Successional group
            if taxon.sg_pioneer or taxon.sg_early_secondary or taxon.sg_late_secondary or taxon.sg_climax:
                successional_group = {}
                successional_group['classification'] = []
                if taxon.sg_pioneer:
                    successional_group['classification'].append('1')
                if taxon.sg_early_secondary:
                    successional_group['classification'].append('2')
                if taxon.sg_late_secondary:
                    successional_group['classification'].append('3')
                if taxon.sg_climax:
                    successional_group['classification'].append('4')
                _add_references(request, successional_group, 'SUG', numbers)
                ecology['successional_group'] = successional_group
            # Pollinators
            if taxon.pollinators:
                pollinators = {}
                pollinators['information'] = taxon.pollinators
                _add_references(request, pollinators, 'POL', numbers)
                ecology['pollinators'] = pollinators
            # Flowering period
            if taxon.fl_start or taxon.fl_end or taxon.fl_details:
                flowering = {}
                if taxon.fl_start or taxon.fl_end:
                    period = {}
                    if taxon.fl_start:
                        period['start'] = taxon.fl_start
                    if taxon.fl_end:
                        period['end'] = taxon.fl_end
                    flowering['period'] = period
                if taxon.fl_details:
                    flowering['details'] = taxon.fl_details
                _add_references(request, flowering, 'FLP', numbers)
                ecology['flowering'] = flowering
            # Seed dispersal
            if taxon.dt_anemochorous or taxon.dt_autochorous or taxon.dt_barochorous or taxon.dt_hydrochorous or taxon.dt_zoochorous:
                seed_dispersal = {}
                seed_dispersal['classification'] = []
                if taxon.dt_anemochorous:
                    seed_dispersal['classification'].append('1')
                if taxon.dt_autochorous:
                    seed_dispersal['classification'].append('2')
                if taxon.dt_barochorous:
                    seed_dispersal['classification'].append('3')
                if taxon.dt_hydrochorous:
                    seed_dispersal['classification'].append('4')
                if taxon.dt_zoochorous:
                    seed_dispersal['classification'].append('5')
                _add_references(request, seed_dispersal, 'SED', numbers)
                ecology['seed_dispersal'] = seed_dispersal
            # Dispersion agents
            if taxon.dispersers:
                dispersers = {}
                dispersers['information'] = taxon.dispersers
                _add_references(request, dispersers, 'DIS', numbers)
                ecology['dispersers'] = dispersers
            # Fruiting period
            if taxon.fr_start or taxon.fr_end or taxon.fr_details:
                fruiting = {}
                if taxon.fr_start or taxon.fr_end:
                    period = {}
                    if taxon.fr_start:
                        period['start'] = taxon.fr_start
                    if taxon.fr_end:
                        period['end'] = taxon.fr_end
                    fruiting['period'] = period
                if taxon.fr_details:
                    fruiting['details'] = taxon.fr_details
                _add_references(request, fruiting, 'FRP', numbers)
                ecology['fruiting'] = fruiting
            # Symbiotic association with roots
            if taxon.symbiotic_assoc is not None or taxon.symbiotic_details:
                symbio = {}
                if taxon.symbiotic_assoc is not None:
                    symbio['presence'] = taxon.symbiotic_assoc
                if taxon.symbiotic_details:
                    symbio['details'] = taxon.symbiotic_details
                _add_references(request, symbio, 'SYM', numbers)
                ecology['symbiotic_association'] = symbio
            # Add data 
            data['ecology'] = ecology
        # Seedling production
        # -------------------
        if request.GET.has_key('seedling'):
            seedling = {}
            # Seed collection
            if taxon.wetland or taxon.dry or taxon.seed_collection:
                seed_collection = {}
                if taxon.wetland or taxon.dry:
                    seed_collection['type'] = []
                    if taxon.seed_tree       :
                        seed_collection['type'].append('T')
                    if taxon.seed_soil:
                        seed_collection['type'].append('S')
                if taxon.seed_collection:
                    seed_collection['details'] = taxon.seed_collection
                _add_references(request, seed_collection, 'SEC', numbers)
                seedling['seed_collection'] = seed_collection
            # Seed type
            if taxon.seed_type:
                seed = {}
                seed['type'] = taxon.seed_type
                _add_references(request, seed, 'SET', numbers)
                seedling['seed_type'] = seed
            # Pre-germination treatment
            if taxon.pg_no_need or taxon.pg_thermal or taxon.pg_chemical or taxon.pg_water or taxon.pg_mechanical or taxon.pg_combined or taxon.pg_other or taxon.pg_details:
                pg = {}
                if taxon.pg_no_need or taxon.pg_thermal or taxon.pg_chemical or taxon.pg_water or taxon.pg_mechanical or taxon.pg_combined or taxon.pg_other:
                    treatment = []
                    if taxon.pg_no_need:
                        treatment.append('N')
                    if taxon.pg_thermal:
                        treatment.append('T')
                    if taxon.pg_chemical:
                        treatment.append('C')
                    if taxon.pg_water:
                        treatment.append('I')
                    if taxon.pg_mechanical:
                        treatment.append('M')
                    if taxon.pg_combined:
                        treatment.append('X')
                    if taxon.pg_other:
                        treatment.append('O')
                    pg['treatment'] = treatment
                if taxon.pg_details:
                    pg['details'] = taxon.pg_details
                _add_references(request, pg, 'PGT', numbers)
                seedling['pre_germination_treatment'] = pg
            # Seedling production
            if taxon.sl_seedbed or taxon.sl_containers or taxon.sl_details:
                sp = {}
                if taxon.sl_seedbed:
                    sp['seedbed'] = taxon.sl_seedbed
                if taxon.sl_containers:
                    sp['individual_containers'] = taxon.sl_containers
                if taxon.sl_details:
                    sp['details'] = taxon.sl_details
                _add_references(request, sp, 'SDL', numbers)
                seedling['seedling_production'] = sp
            # Germination time lapse and rate
            if taxon.seed_gmin_time or taxon.seed_gmax_time or taxon.seed_gmin_rate or taxon.seed_gmax_rate:
                germination = {}
                if taxon.seed_gmin_time or taxon.seed_gmax_time:
                    time_lapse = {}
                    if taxon.seed_gmin_time:
                        time_lapse['min'] = taxon.seed_gmin_time
                    if taxon.seed_gmax_time:
                        time_lapse['max'] = taxon.seed_gmax_time
                    _add_references(request, time_lapse, 'GET', numbers)
                    germination['time_lapse'] = time_lapse
                if taxon.seed_gmin_rate or taxon.seed_gmax_rate:
                    rate = {}
                    if taxon.seed_gmin_rate:
                        rate['min'] = taxon.seed_gmin_rate
                    if taxon.seed_gmax_rate:
                        rate['max'] = taxon.seed_gmax_rate
                    _add_references(request, rate, 'GER', numbers)
                    germination['rate'] = rate
                seedling['germination'] = germination
            # Number of seeds per weight
            if taxon.seeds_per_weight:
                seeds_per_weight = {'value':taxon.seeds_per_weight}
                _add_references(request, seeds_per_weight, 'SPW', numbers)
                seedling['seeds_per_weight'] = seeds_per_weight
            # Light requirements
            if taxon.light or taxon.light_details:
                light = {}
                if taxon.light:
                    light['requirements'] = taxon.light
                if taxon.light_details:
                    light['details'] = taxon.light_details
                _add_references(request, light, 'LIG', numbers)
                seedling['light'] = light
            # Add data 
            data['seedling_production'] = seedling
        # Silviculture
        # ------------
        if request.GET.has_key('silviculture'):
            silviculture = {}
            if taxon.wood_general_info or taxon.wood_density is not None or taxon.wood_has_mai_curve is not None or taxon.wood_has_cai_curve is not None:
                # General information
                if taxon.wood_general_info:
                    silviculture['wood_information'] = taxon.wood_general_info
                # Density
                if taxon.wood_density is not None:
                    silviculture['wood_density'] = taxon.wood_density
                # Mean annual increment curve
                if taxon.wood_has_mai_curve is not None:
                    silviculture['has_mai_curve'] = taxon.wood_has_mai_curve
                # Current annual increment curve
                if taxon.wood_has_cai_curve is not None:
                    silviculture['has_cai_curve'] = taxon.wood_has_cai_curve
                _add_references(request, silviculture, 'WOO', numbers)
            # Add data 
            data['silviculture'] = silviculture
        # References
        # ----------
        if request.GET.has_key('references'):
            if len(citations) > 0:
                dict_citations = {}
                for ref_num, ref_text in citations:
                    dict_citations[int(ref_num)] = ref_text
                data['references'] = dict_citations
        return HttpResponse(JSONEncoder(sort_keys=True, indent=4).encode(data))
    # Normal page rendering
    c = {'taxon': taxon, 'refs': numbers, 'citations': citations, 
         'points': points, 'base_template': settings.BASE_TEMPLATE,
         'full_path': request.get_full_path(), 'help_entries': help_entries}
    possible_templates = ['my_species_page.html', 'species_page.html']
    template = loader.select_template( possible_templates )
    return HttpResponse( template.render(c, request) )

def search_species(request, ws=False):
    _handle_language( request )
    template_params = {'base_template': settings.BASE_TEMPLATE}
    perform_query = True
    if request.GET.has_key('adv'):
        if request.GET.has_key('urban'):
            possible_templates = ['my_adv_search_species_urban.html', 'adv_search_species_urban.html']
            if request.GET.has_key('search'):
                form = UrbanForestrySearchForm(request.GET)
            else:
                form = UrbanForestrySearchForm()
            # Fake page, in case template has some logic based on page code
            page = StaticContent(code='adv_search_species_urban')
            template_params['page'] = page
        elif request.GET.has_key('silv'):
            possible_templates = ['my_adv_search_species_silviculture.html', 'adv_search_species_silviculture.html']
            if request.GET.has_key('search'):
                form = SilvicultureSearchForm(request.GET)
            else:
                form = SilvicultureSearchForm()
            # Fake page, in case template has some logic based on page code
            page = StaticContent(code='adv_search_species_silviculture')
            template_params['page'] = page
        else:
            possible_templates = ['my_adv_search_species_restoration.html', 'adv_search_species_restoration.html']
            if request.GET.has_key('search'):
                form = RestorationSearchForm(request.GET)
            else:
                form = RestorationSearchForm()
            # Fake page, in case template has some logic based on page code
            page = StaticContent(code='adv_search_species_restoration')
            template_params['page'] = page
        template_params['form'] = form
        if not request.GET.has_key('search'):
            perform_query = False
    else:
        possible_templates = ['my_search_species.html', 'search_species.html']
    # Queryset
    if perform_query:
        name = None
        if request.GET.has_key('name'):
            name = request.GET.get('name')
        if name is not None:
            template_params['name'] = name
            # First attempt
            ids = TaxonName.objects.filter(name__iexact=name).values_list('taxon_id')
            num_results = len( ids )
            if num_results == 0:
                # Second attempt
                ids = TaxonName.objects.filter(name__istartswith=name).values_list('taxon_id')
                num_results = len( ids )
                if num_results == 0:
                    # Third attempt
                    ids = TaxonName.objects.filter(name__icontains=name).values_list('taxon_id')
                    num_results = len( ids )
            elif num_results == 1:
                if not ws:
                    return show_species(request, ids[0][0])
            qs = Taxon.objects.filter(id__in=ids)
        else:
            qs = Taxon.objects.all()
        if ( request.GET.has_key('restor') ):
            qs = qs.filter(restoration=True)
        if request.GET.has_key('urban'):
            qs = qs.filter(urban_use=True)
        if request.GET.has_key('silv'):
            qs = qs.filter(silviculture=True)
        # GET params used in pagination
        get_params = ''
        for k, v in request.GET.items():
            if k in ('page', 'csrfmiddlewaretoken'):
                continue
            if len(get_params) > 0:
                get_params += '&'
            get_params += k + '=' + v
        template_params['get_params'] = get_params
        # Advanced search filters
        if request.GET.has_key('family') and request.GET['family'] != 'NULL':
            qs = qs.filter(family=request.GET['family'])
        if request.GET.has_key('endemic'):
            qs = qs.filter(endemic=True)
        if request.GET.has_key('rare'):
            qs = qs.filter(rare=True)
        # Use AND conditions for special features
        qs = _add_and_conditions(request, qs, ['h_flowers', 'h_leaves', 'h_fruits', 'h_crown', 'h_bark', 'h_seeds', 'h_wood', 'h_roots'])
        # Use OR conditions for growth rate parameters
        qs = _add_or_conditions(request, qs, ['gr_slow', 'gr_moderate', 'gr_fast'])
        # Use OR conditions for trunk alignment parameters
        qs = _add_or_conditions(request, qs, ['tr_straight', 'tr_sl_inclined', 'tr_inclined', 'tr_sl_crooked', 'tr_crooked'])
        # Use OR conditions for foliage persistence parameters
        qs = _add_or_conditions(request, qs, ['fo_evergreen', 'fo_semideciduous', 'fo_deciduous'])
        # Height
        qs = _add_interval_condition(request, qs, 'min_height', 'max_height')
        # DBH
        qs = _add_interval_condition(request, qs, 'min_dbh', 'max_dbh')
        # Crown diameter
        qs = _add_interval_condition(request, qs, 'cr_min_diameter', 'cr_max_diameter')
        # Germination rate
        qs = _add_interval_condition(request, qs, 'seed_gmin_rate', 'seed_gmax_rate')
        # Crown shape
        if request.GET.has_key('cr_shape') and request.GET['cr_shape'] != 'NULL':
            qs = qs.filter(cr_shape=request.GET['cr_shape'])
        # Flower color
        if request.GET.has_key('color') and request.GET['color'] not in ('0', 0):
            qs = qs.filter(fl_color=request.GET['color'])
        # Root system
        if request.GET.has_key('r_type') and request.GET['r_type'] != 'NULL':
            qs = qs.filter(r_type=request.GET['r_type'])
        # Seed type
        if request.GET.has_key('s_type') and request.GET['s_type'] != 'NULL':
            qs = qs.filter(seed_type=request.GET['s_type'])
        # Light requirements
        if request.GET.has_key('light') and request.GET['light'] != 'NULL':
            qs = qs.filter(light=request.GET['light'])
        # Flowering period
        if request.GET.has_key('fl_month'):
            qs = _add_month_condition(request, qs, 'fl_month', 'fl_start', 'fl_end')
        # Fruiting period
        if request.GET.has_key('fr_month'):
            qs = _add_month_condition(request, qs, 'fr_month', 'fr_start', 'fr_end')
        # Pruning
        if request.GET.has_key('pruning'):
            if request.GET['pruning'] in ('1', 1):
                qs = qs.filter(pruning=True)
            elif request.GET['pruning'] in ('0', 0):
                qs = qs.filter(pruning=False)
        # Pollinators
        if request.GET.has_key('pollinators'):
            if request.GET['pollinators'] in ('1', 1):
                qs = qs.filter(pollinators__isnull=False).exclude(pollinators='')
            elif request.GET['pollinators'] in ('0', 0):
                qs = qs.filter(Q(pollinators__isnull=True) | Q(pollinators=''))
        # Diseases
        if request.GET.has_key('diseases'):
            if request.GET['diseases'] in ('1', 1):
                qs = qs.filter(pests_and_diseases__isnull=False).exclude(pests_and_diseases='')
            elif request.GET['diseases'] in ('0', 0):
                qs = qs.filter(Q(pests_and_diseases__isnull=True) | Q(pests_and_diseases=''))
        # Thorns
        if request.GET.has_key('thorns'):
            if request.GET['thorns'] in ('1', 1):
                qs = qs.filter(thorns_or_spines__isnull=False).exclude(thorns_or_spines='')
            elif request.GET['thorns'] in ('0', 0):
                qs = qs.filter(Q(thorns_or_spines__isnull=True) | Q(thorns_or_spines=''))
        # Toxic
        if request.GET.has_key('toxic'):
            if request.GET['toxic'] in ('1', 1):
                qs = qs.filter(toxic_or_allergenic__isnull=False).exclude(toxic_or_allergenic='')
            elif request.GET['toxic'] in ('0', 0):
                qs = qs.filter(Q(toxic_or_allergenic__isnull=True) | Q(toxic_or_allergenic=''))
        # Use OR condition for successional group
        qs = _add_or_conditions(request, qs, ['sg_pioneer', 'sg_early_secondary', 'sg_late_secondary', 'sg_climax'])
        # Use OR condition for seed dispersal
        qs = _add_or_conditions(request, qs, ['dt_anemochorous', 'dt_autochorous', 'dt_barochorous', 'dt_hydrochorous', 'dt_zoochorous'])
        # Use OR condition for terrain drainage
        qs = _add_or_conditions(request, qs, ['wetland', 'dry'])
        # Use OR condition for pre-germination treatment
        qs = _add_or_conditions(request, qs, ['pg_no_need', 'pg_thermal', 'pg_chemical', 'pg_water', 'pg_mechanical', 'pg_combined', 'pg_other'])
        # Symbiotic association
        if request.GET.has_key('symb_assoc'):
            if request.GET['symb_assoc'] in ('1', 1):
                qs = qs.filter(symbiotic_assoc=True)
            elif request.GET['symb_assoc'] in ('0', 0):
                qs = qs.filter(symbiotic_assoc=False)
        # Specific uses
        if request.GET.has_key('uses'):
            my_uses = []
            for use_id in request.GET.getlist('uses'):
                try:
                    use = TypeOfUse.objects.get(pk=use_id)
                    my_uses.append( use_id )
                    for use_desc_id in use.get_descendants().values_list('id', flat=True):
                        my_uses.append(use_desc_id)
                except TypeOfUse.DoesNotExist:
                    pass
            if len(my_uses) > 0:
                taxa_ids = TaxonUse.objects.filter(use__in=my_uses).values_list('taxon__id', flat=True).distinct('taxon__id')
                qs = qs.filter(id__in=taxa_ids)
        # Habitat
        if request.GET.has_key('habitats'):
            my_habitats = []
            for habitat_id in request.GET.getlist('habitats'):
                try:
                    habitat = Habitat.objects.get(pk=habitat_id)
                    my_habitats.append( habitat_id )
                    for habitat_desc_id in habitat.get_descendants().values_list('id', flat=True):
                        my_habitats.append(habitat_desc_id)
                except Habitat.DoesNotExist:
                    pass
            if len(my_habitats) > 0:
                htaxa_ids = TaxonHabitat.objects.filter(habitat__in=my_habitats).values_list('taxon__id', flat=True).distinct('taxon__id')
                qs = qs.filter(id__in=htaxa_ids)
        # Density
        qs = _add_single_field_interval_condition(request, qs, 'wood_density', 'min_density', 'max_density')
        # Has MAI curve
        if request.GET.has_key('has_mai_curve'):
            if request.GET['has_mai_curve'] in ('1', 1):
                qs = qs.filter(wood_has_mai_curve=True)
            elif request.GET['has_mai_curve'] in ('0', 0):
                qs = qs.filter(wood_has_mai_curve=False)
        # Conservation status
        if request.GET.has_key('status') and request.GET['status'] != u'NULL':
            taxa_in_status = []
            try:
                for taxon_in_status in ConservationStatus.objects.filter(status=request.GET['status']).values_list('taxon__id', flat=True):
                    taxa_in_status.append(taxon_in_status)
                if len(taxa_in_status) > 0:
                    qs = qs.filter(id__in=taxa_in_status)
            except ConservationStatus.DoesNotExist:
                pass
        # Limit the number of fields to be returned
        qs = qs.order_by('genus', 'species').only('id', 'genus', 'species')
        if request.GET.has_key('pdf'):
            if request.GET['pdf'] not in ("1", ""):
                # Someone may attempt to get server information by messing with this parameter
                return redirect('http://www.ic3.gov/about/')
            return _pdf_for_species_list( qs )
        template_params['performed_query'] = True
        # Pagination
        per_page = settings.DEFAULT_PER_PAGE
        if request.GET.has_key('per_page'):
            per_page = request.GET.get('per_page')
            if not isinstance( per_page, int ):
                if per_page.isdigit():
                    per_page = int(per_page)
                else:
                    per_page = settings.DEFAULT_PER_PAGE
            if per_page > settings.MAX_PER_PAGE:
                per_page = settings.MAX_PER_PAGE
            elif per_page < settings.MIN_PER_PAGE:
                per_page = settings.MIN_PER_PAGE
        paginator = Paginator(qs, per_page)
        if ( request.GET.has_key('page') ):
            page = request.GET.get('page')
        else:
            page = 1
        try:
            taxa = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            taxa = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            taxa = paginator.page(paginator.num_pages)
        template_params['taxa'] = taxa
        # Web service
        if ws:
            if taxa.paginator.count == 0:
                return HttpResponse(status=404)
            from json.encoder import JSONEncoder
            from django.core.urlresolvers import reverse
            abs_uri = 'https' if request.is_secure() else 'http'
            abs_uri += '://' + request.get_host()
            abs_uri += reverse('app.views.search_species')
            sp_base_url = abs_uri[:abs_uri.index('/', 10)] + '/sp/'
            records = []
            for taxon in taxa.object_list:
                records.append({'fullname':taxon.label, 'id':taxon.id, 'link':sp_base_url+str(taxon.id)})
            resp = HttpResponse(JSONEncoder(sort_keys=True, indent=4).encode(records))
            # Pagination stuff
            if taxa.number == 1:
                resp['X-Total-Count'] = taxa.paginator.count
            link = ''
            if taxa.has_previous():
                link = _add_link(abs_uri, link, taxa.previous_page_number(), u'prev', get_params)
            if taxa.has_next():
                link = _add_link(abs_uri, link, taxa.next_page_number(), u'next', get_params)
            if taxa.number > 1:
                link = _add_link(abs_uri, link, 1, u'first', get_params)
            if taxa.number != taxa.end_index():
                link = _add_link(abs_uri, link, taxa.end_index(), u'last', get_params)
            if len(link) > 0:
                resp['Link'] = link
            return resp
    template_params['full_path'] = request.get_full_path()
    template = loader.select_template( possible_templates )
    return HttpResponse( template.render(template_params, request) )

def interview(request, interview_id):
    'Display interview page'
    _handle_language( request )
    if not isinstance( interview_id, int ):
        if interview_id.isdigit():
            interview_id = int(interview_id)
        else:
            raise Http404
    try:
        interview = Interview.objects.get(pk=interview_id)
    except Interview.DoesNotExist:
        raise Http404
    # Pagination
    from app.interview_paginator import InterviewPaginator
    paginator = InterviewPaginator(interview.content, 1, 0, True, 40) # 40 lines per page
    if ( request.GET.has_key('page') ):
        page = request.GET.get('page')
    else:
        page = 1
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)
    possible_templates = ['my_interview.html', 'interview.html']
    template_params = {'base_template':settings.BASE_TEMPLATE}
    template_params['interview'] = interview
    template_params['paginator'] = paginator
    template_params['page_obj'] = page_obj
    template_params['request'] = request
    template = loader.select_template( possible_templates )
    return HttpResponse( template.render(template_params, request) )

def ws_metadata(request):
    'Return web service metadata'
    from json.encoder import JSONEncoder
    # Gather uses
    uses = {}
    for node, info in TypeOfUse.get_annotated_list():
        parent_id = None
        parent = node.get_parent()
        if parent is not None:
            parent_id = parent.id
        uses[node.id] = {'label':node.label, 'level':info['level'], 'parent_id': str(parent_id)}
    # Gather habitats
    habitats = {}
    for node, info in Habitat.get_annotated_list():
        parent_id = None
        parent = node.get_parent()
        if parent is not None:
            parent_id = parent.id
        habitats[node.id] = {'label':node.name, 'level':info['level'], 'parent_id': str(parent_id)}
    # Conservation status
    status = ConservationStatus.objects.all().distinct('status').values_list('status', flat=True)
    # Languages
    languages = {}
    for lang in settings.LANGUAGES:
        languages[lang[0]] = lang[1]
    # Build response
    meta = {'citation': u'Sistema Flora Regional - Instituto de Pesquisas Ecológicas (IPÊ)', 'name': 'Regional Flora Web Service', 'license': 'GNU AGPLv3', 'languages':languages, 'settings': {'species_pagination': {'default_per_page':settings.DEFAULT_PER_PAGE, 'max_per_page':settings.MAX_PER_PAGE, 'min_per_page':settings.MIN_PER_PAGE}}, 'dictionaries': {'crown_shape': _to_dict(CROWN_SHAPES), 'color': _to_dict(COLORS), 'root_type': _to_dict(ROOT_SYSTEMS), 'seed_type':_to_dict(SEED_TYPES), 'light_requirement':_to_dict(LIGHT_REQUIREMENTS), 'fruit_type':_to_dict(FRUIT_TYPES), 'bark_texture':_to_dict(BARK_TEXTURES), 'growth_rate':_to_dict(GROWTH_RATE), 'foliage_persistence':_to_dict(FOLIAGE_PERSISTENCE), 'trunk_alignment':_to_dict(TRUNK_ALIGNMENT), 'soil_type':_to_dict(SOIL_TYPES), 'seed_dispersal':_to_dict(SEED_DISPERSAL_TYPE), 'seed_collection':_to_dict(SEED_COLLECTION), 'pre_germination_treatment':_to_dict(PRE_GERMINATION_TREATMENT), 'use':uses, 'habitat':habitats, 'status':list(status)}}
    return HttpResponse(JSONEncoder(sort_keys=True, indent=4).encode(meta))

def ws_info(request):
    'Web service documentation'
    _handle_language( request )
    c = {'base_template': settings.BASE_TEMPLATE}
    possible_templates = ['my_ws_info.html', 'ws_info.html']
    template = loader.select_template( possible_templates )
    return HttpResponse( template.render(c, request) )
