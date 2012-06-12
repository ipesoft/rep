# coding=UTF-8

from app.models import Page, Taxon, TaxonName, TaxonDataReference, COLORS, MONTHS, ROOT_SYSTEMS, CROWN_SHAPES, ConservationStatus
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from django.db.models import Q, F

# General definitions
no_matter_str = _(u'indifferent')
null_boolean_choices = (( -1, no_matter_str ),( 1 , _(u'yes') ),( 0 , _(u'no') ))

# Form classes
class CommonSearchForm(forms.Form):
    month_choices = [(0, no_matter_str)] + list(MONTHS)
    root_system_choices = [('NULL', no_matter_str)] + list(ROOT_SYSTEMS)
    status_choices = [('NULL', no_matter_str)] + [(c['status'], c['status']) for c in ConservationStatus.objects.values('status').order_by('status').distinct()]
    rare        = forms.BooleanField(label=_(u'Rare'))
    endemic     = forms.BooleanField(label=_(u'Endemic'))
    # Growth rate
    gr_slow     = forms.BooleanField(label=_(u'Slow'))
    gr_moderate = forms.BooleanField(label=_(u'Moderate'))
    gr_fast     = forms.BooleanField(label=_(u'Fast'))
    pruning     = forms.ChoiceField(label=_(u'Requires pruning'), initial=-1, choices=null_boolean_choices)
    fl_month    = forms.ChoiceField(label=_(u'With flower in month'), initial=0, choices=month_choices)
    fr_month    = forms.ChoiceField(label=_(u'With fruits in month'), initial=0, choices=month_choices)
    r_type      = forms.ChoiceField(label=_(u'Root system'), initial='NULL', choices=root_system_choices)
    # Foliage persistence
    fo_evergreen     = forms.BooleanField(label=_(u'Evergreen'))
    fo_semideciduous = forms.BooleanField(label=_(u'Semi-deciduous'))
    fo_deciduous     = forms.BooleanField(label=_(u'Deciduous'))
    min_height   = forms.IntegerField(initial=None, widget=forms.TextInput(attrs={'size':'3'}))
    max_height   = forms.IntegerField(initial=None, widget=forms.TextInput(attrs={'size':'3'}))
    cr_min_diameter = forms.IntegerField(initial=None, widget=forms.TextInput(attrs={'size':'3'}))
    cr_max_diameter = forms.IntegerField(initial=None, widget=forms.TextInput(attrs={'size':'3'}))
    status         = forms.ChoiceField(label=_(u'conservation status'), initial='NULL', choices=status_choices)

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
    # Trunk alignement
    tr_straight    = forms.BooleanField(label=_(u'Straight'))
    tr_sl_inclined = forms.BooleanField(label=_(u'Slightly inclined'))
    tr_inclined    = forms.BooleanField(label=_(u'Inclined'))
    tr_sl_crooked  = forms.BooleanField(label=_(u'Slightly crooked'))
    tr_crooked     = forms.BooleanField(label=_(u'Crooked'))

class RestorationSearchForm(CommonSearchForm):
    symb_assoc = forms.ChoiceField(label=_(u'Symbiotic association'), initial=-1, choices=null_boolean_choices)
    # Successional group
    sg_pioneer         = forms.BooleanField(label=_(u'Pioneer'))
    sg_early_secondary = forms.BooleanField(label=_(u'Early secondary'))
    sg_late_secondary  = forms.BooleanField(label=_(u'Late secondary'))
    sg_climax          = forms.BooleanField(label=_(u'Climax'))
    # Type of dispersion
    dt_anemochorous = forms.BooleanField(label=_(u'Anemochorous'))
    dt_autochorous  = forms.BooleanField(label=_(u'Autochorous'))
    dt_hydrochorous = forms.BooleanField(label=_(u'Hydrochorous'))
    dt_zoochorous   = forms.BooleanField(label=_(u'Zoochorous'))

# Internal methods
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

# View methods
def index(request):
    'Index page'
    c = RequestContext(request, {'base_template':settings.BASE_TEMPLATE})
    possible_templates = ['my_index.html', 'index.html']
    return render_to_response( possible_templates, c )

def show_page(request, page_code):
    'Generic method to show a page stored in the database'
    pages = Page.objects.filter(code=page_code)
    if len(pages) == 0:
        raise Http404
    try:
        p = pages.get(lang=request.LANGUAGE_CODE)
    except Page.DoesNotExist:
        # Get first
        p = pages[0]
    c = RequestContext(request, {'page': p,
                                 'base_template':settings.BASE_TEMPLATE})
    possible_templates = ['my_page.html', 'page.html']
    return render_to_response( possible_templates, c )

def show_species(request, species_id):
    'Display data about a species'
    if not isinstance( species_id, int ):
        if species_id.isdigit():
            species_id = int(species_id)
        else:
            raise Http404
    try:
        taxon = Taxon.objects.get(pk=species_id)
    except Taxon.DoesNotExist:
        raise Http404
    #data = ('RAR','END','SPE','SUG','GRO','PRU','FLP','FLC','POL','SED','DIS','FRT','SYM','ROT','FOL','CRD','CRS','BRT','TRA','SIZ','TOS','TOA','PAD','FRP','SEC','SET','PGT','SDL','GET','GER','LIG')
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
        if numbers.has_key(ref.data):
            numbers[ref.data] = numbers[ref.data] + ',' + ctrl[ref.reference_id]
        else:
            numbers[ref.data] = ctrl[ref.reference_id]
    c = RequestContext(request, {'taxon': taxon, 'refs': numbers, 'citations': citations, 
                                 'base_template':settings.BASE_TEMPLATE})
    possible_templates = ['my_species_page.html', 'species_page.html']
    return render_to_response( possible_templates, c )

def search_species(request):
    template_params = {'base_template':settings.BASE_TEMPLATE}
    perform_query = True
    if ( request.GET.has_key('adv') ):
        if ( request.GET.has_key('urban') ):
            possible_templates = ['my_adv_search_species_urban.html', 'adv_search_species_urban.html']
            if ( request.GET.has_key('search') ):
                form = UrbanForestrySearchForm(request.GET)
            else:
                form = UrbanForestrySearchForm()
        else:
            possible_templates = ['my_adv_search_species_restoration.html', 'adv_search_species_restoration.html']
            if ( request.GET.has_key('search') ):
                form = RestorationSearchForm(request.GET)
            else:
                form = RestorationSearchForm()
        template_params['form'] = form
        if ( not request.GET.has_key('search') ):
            perform_query = False
    else:
        possible_templates = ['my_search_species.html', 'search_species.html']
    # Queryset
    if perform_query:
        name = None
        if ( request.GET.has_key('name') ):
            name = request.GET.get('name')
        if ( name is not None ):
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
                return show_species(request, ids[0][0])
            qs = Taxon.objects.filter(id__in=ids)
        else:
            qs = Taxon.objects.all()
        if ( request.GET.has_key('restor') ):
            qs = qs.filter(restoration=True)
        if ( request.GET.has_key('urban') ):
            qs = qs.filter(urban_use=True)
        # GET params used in pagination
        get_params = ''
        for k, v in request.GET.items():
            if k in ('page', 'csrfmiddlewaretoken'):
                continue
            get_params = get_params + '&' + k + '=' + v
        template_params['get_params'] = get_params
        # Advanced search filters
        if ( request.GET.has_key('endemic')):
            qs = qs.filter(endemic=True)
        if ( request.GET.has_key('rare')):
            qs = qs.filter(endemic=True)
        # Use AND conditions for special features
        qs = _add_and_conditions(request, qs, ['h_flowers', 'h_leaves', 'h_fruits', 'h_crown', 'h_bark'])
        # Use OR conditions for growth rate parameters
        qs = _add_or_conditions(request, qs, ['gr_slow', 'gr_moderate', 'gr_fast'])
        # Use OR conditions for trunk alignment parameters
        qs = _add_or_conditions(request, qs, ['tr_straight', 'tr_sl_inclined', 'tr_inclined', 'tr_sl_crooked', 'tr_crooked'])
        # Use OR conditions for foliage persistence parameters
        qs = _add_or_conditions(request, qs, ['fo_evergreen', 'fo_semideciduous', 'fo_deciduous'])
        # Height
        qs = _add_interval_condition(request, qs, 'min_height', 'max_height')
        # Crown diameter
        qs = _add_interval_condition(request, qs, 'cr_min_diameter', 'cr_max_diameter')
        # Crown shape
        if ( request.GET.has_key('cr_shape') and request.GET['cr_shape'] != 'NULL'):
            qs = qs.filter(cr_shape=request.GET['cr_shape'])
        # Flower color
        if ( request.GET.has_key('color') and request.GET['color'] not in ('0', 0)):
            qs = qs.filter(fl_color=request.GET['color'])
        # Root system
        if ( request.GET.has_key('r_type') and request.GET['r_type'] != 'NULL'):
            qs = qs.filter(r_type=request.GET['r_type'])
        # Flowering period
        if ( request.GET.has_key('fl_month') ):
            qs = _add_month_condition(request, qs, 'fl_month', 'fl_start', 'fl_end')
        # Fruiting period
        if ( request.GET.has_key('fr_month') ):
            qs = _add_month_condition(request, qs, 'fr_month', 'fr_start', 'fr_end')
        # Pruning
        if ( request.GET.has_key('pruning') ):
            if request.GET['pruning'] in ('1', 1):
                qs = qs.filter(pruning=True)
            elif request.GET['pruning'] in ('0', 0):
                qs = qs.filter(pruning=False)
        # Thorns
        if ( request.GET.has_key('thorns') ):
            if request.GET['thorns'] in ('1', 1):
                qs = qs.filter(thorns_or_spines__isnull=False).exclude(thorns_or_spines='')
            elif request.GET['thorns'] in ('0', 0):
                qs = qs.filter(Q(thorns_or_spines__isnull=True) | Q(thorns_or_spines=''))
        # Toxic
        if ( request.GET.has_key('toxic') ):
            if request.GET['toxic'] in ('1', 1):
                qs = qs.filter(toxic_or_allergenic__isnull=False).exclude(toxic_or_allergenic='')
            elif request.GET['toxic'] in ('0', 0):
                qs = qs.filter(Q(toxic_or_allergenic__isnull=True) | Q(toxic_or_allergenic=''))
        # Use OR condition for successional group
        qs = _add_or_conditions(request, qs, ['sg_pioneer', 'sg_early_secondary', 'sg_late_secondary', 'sg_climax'])
        # Use OR condition for seed dispersal
        qs = _add_or_conditions(request, qs, ['dt_anemochorous', 'dt_autochorous', 'dt_hydrochorous', 'dt_zoochorous'])
        # Symbiotic association
        if ( request.GET.has_key('symb_assoc') ):
            if request.GET['symb_assoc'] in ('1', 1):
                qs = qs.filter(symbiotic_assoc=True)
            elif request.GET['symb_assoc'] in ('0', 0):
                qs = qs.filter(symbiotic_assoc=False)
        # Limit the number of fields to be returned
        qs = qs.order_by('genus', 'species').only('id', 'genus', 'species')
        template_params['performed_query'] = True
        # Pagination
        paginator = Paginator(qs, 25) # Show 25 items per page
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
    c = RequestContext(request, template_params)
    return render_to_response( possible_templates, c )
