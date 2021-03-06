# coding=UTF-8

from app.models import StaticContent, Taxon, TaxonName, Reference, TaxonDataReference, ConservationAssessmentSource, ConservationStatus, TypeOfUse, TaxonUse, Interview, Habitat, TaxonHabitat
from django.contrib import admin
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _
from treebeard.admin import TreeAdmin

class RefForm(ModelForm):
    """
    Custom form to handle biblographic references related to taxon data.
    It must be subclassed and each subclass must define the taxondata
    attribute specifyng which piece of data it refers to.
    """

    def save(self, commit=True, *args, **kwargs):
        """
        Overloaded save method only to set the data field
        """
        m = super(RefForm, self).save(commit=False, *args, **kwargs)
        m.data = self.taxondata
        if commit:
            m.save()
        return m

    def hide_orig(self):
        """
        Custom method to avoid displaying original data in
        the inline form for each field. It is used by
        templates/admin/mytabular.html
        """
        return True

    def ref_code(self):
        """
        Method created just to help debugging reference relation.
        """
        return self.taxondata

class RefInline(admin.TabularInline):
    """
    Generic inline for bibliographic references. It needs to be subclassed
    and each subclass must indicate a form that inherits from RefForm.
    """
    
    model = TaxonDataReference
    extra = 0
    exclude = ('data',)
    verbose_name = _('reference')
    verbose_name_plural = _('references')
    template = 'admin/edit_inline/mytabular.html'

    def get_queryset(self, request):
        """
        Overloaded to avoid displaying all references related to
        the taxon in each reference combo.
        """
        qs = super(RefInline, self).get_queryset(request)
        return qs.filter(data=self.form.taxondata)

class RarityRefForm(RefForm):
    taxondata = 'RAR'
class RarityRefInline(RefInline):
    form = RarityRefForm
    #verbose_name = _('Abundance reference')
    #verbose_name_plural = _('Abundance references')

class EndemicRefForm(RefForm):
    taxondata = 'END'
class EndemicRefInline(RefInline):
    form = EndemicRefForm
    #verbose_name = _('Endemism reference')
    #verbose_name_plural = _('Endemism references')

class SpecialFeaturesRefForm(RefForm):
    taxondata = 'SPE'
class SpecialFeaturesRefInline(RefInline):
    form = SpecialFeaturesRefForm
    #verbose_name = _('Special features reference')
    #verbose_name_plural = _('Special features references')

class SuccessionalGroupRefForm(RefForm):
    taxondata = 'SUG'
class SuccessionalGroupRefInline(RefInline):
    form = SuccessionalGroupRefForm
    #verbose_name = _('successional group reference')
    #verbose_name_plural = _('successional group references')

class GrowthRateRefForm(RefForm):
    taxondata = 'GRO'
class GrowthRateRefInline(RefInline):
    form = GrowthRateRefForm
    #verbose_name = _('growth rate reference')
    #verbose_name_plural = _('growth rate references')

class RequiresPruningRefForm(RefForm):
    taxondata = 'PRU'
class RequiresPruningRefInline(RefInline):
    form = RequiresPruningRefForm
    #verbose_name = _('pruning reference')
    #verbose_name_plural = _('pruning references')

class FloweringPeriodRefForm(RefForm):
    taxondata = 'FLP'
class FloweringPeriodRefInline(RefInline):
    form = FloweringPeriodRefForm
    #verbose_name = _('flowering period reference')
    #verbose_name_plural = _('flowering period references')

class FloweringColorRefForm(RefForm):
    taxondata = 'FLC'
class FloweringColorRefInline(RefInline):
    form = FloweringColorRefForm
    #verbose_name = _('flowering color reference')
    #verbose_name_plural = _('flowering color references')

class PollinatorsRefForm(RefForm):
    taxondata = 'POL'
class PollinatorsRefInline(RefInline):
    form = PollinatorsRefForm
    #verbose_name = _('pollinators reference')
    #verbose_name_plural = _('pollinators references')

class DispersalRefForm(RefForm):
    taxondata = 'SED'
class DispersalRefInline(RefInline):
    form = DispersalRefForm
    #verbose_name = _('seed dispersal reference')
    #verbose_name_plural = _('seed dispersal references')

class DispersersRefForm(RefForm):
    taxondata = 'DIS'
class DispersersRefInline(RefInline):
    form = DispersersRefForm
    #verbose_name = _('dispersers reference')
    #verbose_name_plural = _('dispersers references')

class FruitTypeRefForm(RefForm):
    taxondata = 'FRT'
class FruitTypeRefInline(RefInline):
    form = FruitTypeRefForm
    #verbose_name = _('fruit type reference')
    #verbose_name_plural = _('fruit type references')

class SymbioticRefForm(RefForm):
    taxondata = 'SYM'
class SymbioticRefInline(RefInline):
    form = SymbioticRefForm
    #verbose_name = _('symbiotic association reference')
    #verbose_name_plural = _('symbiotic association references')

class RootSystemRefForm(RefForm):
    taxondata = 'ROT'
class RootSystemRefInline(RefInline):
    form = RootSystemRefForm
    #verbose_name = _('root system reference')
    #verbose_name_plural = _('root system references')

class FoliagePersitenceRefForm(RefForm):
    taxondata = 'FOL'
class FoliagePersitenceRefInline(RefInline):
    form = FoliagePersitenceRefForm
    #verbose_name = _('foliage persistence reference')
    #verbose_name_plural = _('foliage persistence references')

class CrownDiameterRefForm(RefForm):
    taxondata = 'CRD'
class CrownDiameterRefInline(RefInline):
    form = CrownDiameterRefForm
    #verbose_name = _('crown diameter reference')
    #verbose_name_plural = _('crown diameter references')

class CrownShapeRefForm(RefForm):
    taxondata = 'CRS'
class CrownShapeRefInline(RefInline):
    form = CrownShapeRefForm
    #verbose_name = _('crown shape reference')
    #verbose_name_plural = _('crown shape references')

class BarkTextureRefForm(RefForm):
    taxondata = 'BRT'
class BarkTextureRefInline(RefInline):
    form = BarkTextureRefForm
    #verbose_name = _('bark texture reference')
    #verbose_name_plural = _('bark texture references')

class TrunkAlignmentRefForm(RefForm):
    taxondata = 'TRA'
class TrunkAlignmentRefInline(RefInline):
    form = TrunkAlignmentRefForm
    #verbose_name = _('trunk alignment reference')
    #verbose_name_plural = _('trunk alignment references')

class SizeRefForm(RefForm):
    taxondata = 'SIZ'
class SizeRefInline(RefInline):
    form = SizeRefForm
    #verbose_name = _('tree size reference')
    #verbose_name_plural = _('tree size references')

class ThornsOrSpinesRefForm(RefForm):
    taxondata = 'TOS'
class ThornsOrSpinesRefInline(RefInline):
    form = ThornsOrSpinesRefForm
    #verbose_name = _('thorns or spines reference')
    #verbose_name_plural = _('thorns or spines references')

class ToxicOrAllegenicRefForm(RefForm):
    taxondata = 'TOA'
class ToxicOrAllegenicRefInline(RefInline):
    form = ToxicOrAllegenicRefForm
    #verbose_name = _('toxic or allergenic reference')
    #verbose_name_plural = _('toxic or allergenic references')

class PestsAndDiseasesRefForm(RefForm):
    taxondata = 'PAD'
class PestsAndDiseasesRefInline(RefInline):
    form = PestsAndDiseasesRefForm
    #verbose_name = _('pests and diseases reference')
    #verbose_name_plural = _('pests and diseases references')

class FruitingPeriodRefForm(RefForm):
    taxondata = 'FRP'
class FruitingPeriodRefInline(RefInline):
    form = FruitingPeriodRefForm
    #verbose_name = _('fruiting period reference')
    #verbose_name_plural = _('fruiting period references')

class SeedCollectionRefForm(RefForm):
    taxondata = 'SEC'
class SeedCollectionRefInline(RefInline):
    form = SeedCollectionRefForm
    #verbose_name = _('seed collection reference')
    #verbose_name_plural = _('seed collection references')

class SeedTypeRefForm(RefForm):
    taxondata = 'SET'
class SeedTypeRefInline(RefInline):
    form = SeedTypeRefForm
    #verbose_name = _('seed type reference')
    #verbose_name_plural = _('seed type references')

class PgTreatmentRefForm(RefForm):
    taxondata = 'PGT'
class PgTreatmentRefInline(RefInline):
    form = PgTreatmentRefForm
    #verbose_name = _('pre-germination treatment reference')
    #verbose_name_plural = _('pre-germination treatment references')

class SeedlingProductionRefForm(RefForm):
    taxondata = 'SDL'
class SeedlingProductionRefInline(RefInline):
    form = SeedlingProductionRefForm
    #verbose_name = _('seedling production reference')
    #verbose_name_plural = _('seedling production references')

class GerminationTimeRefForm(RefForm):
    taxondata = 'GET'
class GerminationTimeRefInline(RefInline):
    form = GerminationTimeRefForm
    #verbose_name = _('germination time lapse reference')
    #verbose_name_plural = _('germination time lapse references')

class GerminationRateRefForm(RefForm):
    taxondata = 'GER'
class GerminationRateRefInline(RefInline):
    form = GerminationRateRefForm
    #verbose_name = _('germination rate reference')
    #verbose_name_plural = _('germination rate references')

class SeedsPerWeightRefForm(RefForm):
    taxondata = 'SPW'
class SeedsPerWeightRefInline(RefInline):
    form = SeedsPerWeightRefForm
    #verbose_name = _('seeds per weight reference')
    #verbose_name_plural = _('seeds per weight references')

class LightRefForm(RefForm):
    taxondata = 'LIG'
class LightRefInline(RefInline):
    form = LightRefForm
    #verbose_name = _('light requirements reference')
    #verbose_name_plural = _('light requirements references')

class TerrainRefForm(RefForm):
    taxondata = 'TER'
class TerrainRefInline(RefInline):
    form = TerrainRefForm
    #verbose_name = _('terrain reference')
    #verbose_name_plural = _('terrain references')

class ConservationStatusInline(admin.TabularInline):
    model = ConservationStatus
    extra = 0
    verbose_name = _('conservation status')
    verbose_name_plural = _('conservation statuses')
    show_in_the_end = 1 # Custom attribute to show this in the end of the page

class UsesInline(admin.TabularInline):
    model = TaxonUse
    extra = 0
    verbose_name = _('documented use')
    verbose_name_plural = _('documented uses')
    show_in_the_end = 0 # Custom attribute to show this in the end of the page

class UseRefForm(RefForm):
    taxondata = 'USE'
class UseRefInline(RefInline):
    form = UseRefForm
    #verbose_name = _('documented use reference')
    #verbose_name_plural = _('documented use references')

class HabitatsInline(admin.TabularInline):
    model = TaxonHabitat
    extra = 0
    verbose_name = _('habitat')
    verbose_name_plural = _('habitats')
    show_in_the_end = 0 # Custom attribute to show this in the end of the page

class HabitatRefForm(RefForm):
    taxondata = 'HAB'
class HabitatRefInline(RefInline):
    form = HabitatRefForm
    #verbose_name = _('habitat')
    #verbose_name_plural = _('habitats')

class WoodRefForm(RefForm):
    taxondata = 'WOO'
class WoodRefInline(RefInline):
    form = WoodRefForm

class NameForm(ModelForm):
    """
    Custom form to handle taxon names.
    It must be subclassed and each subclass must define the nametype
    attribute.
    """

    def save(self, commit=True, *args, **kwargs):
        """
        Overloaded save method only to set the ntype field
        """
        m = super(NameForm, self).save(commit=False, *args, **kwargs)
        m.ntype = self.ntype
        if commit:
            m.save()
        return m

    def hide_orig(self):
        """
        Custom method to avoid displaying original data in
        the inline form for each field. It is used by
        templates/admin/mytabular.html
        """
        return True

class SynonymsForm(NameForm):
    ntype = 'S'

class CommonNamesForm(NameForm):
    ntype = 'P'

class NamesInline(admin.TabularInline):
    """
    Generic inline for taxon names. It needs to be subclassed
    and each subclass must indicate a form that inherits from NameForm.
    """
    model = TaxonName
    extra = 0
    exclude = ('ntype',)

    def get_queryset(self, request):
        """
        Overloaded to avoid displaying other name types.
        """
        qs = super(NamesInline, self).get_queryset(request)
        return qs.filter(ntype=self.form.ntype)

class SynonymsInline(NamesInline):
    form = SynonymsForm
    verbose_name = _('synonym')
    verbose_name_plural = _('synonyms')

class CommonNamesInline(NamesInline):
    form = CommonNamesForm
    verbose_name = _('common name')
    verbose_name_plural = _('common names')

class TaxonAdmin(admin.ModelAdmin):
    change_form_template = 'admin/taxon_change_form.html'
    list_display = ('label', 'family', 'data_completeness')
    list_max_show_all = 300
    fieldsets = (
        (_('Taxonomic data'), {                    #1
            #'classes': ('collapse',),
            'fields': (('genus', 'species'), ('subspecies', 'author'), 'family'),
        }),
        (_('General description'), {               #2
            #'classes': ('collapse',),
            'fields': ('description',),
        }),
        (_('Ethnobotany description'), {           #3
            #'classes': ('collapse',),
            'fields': ('ethno_notes',),
        }),
        (_('Uses'), {                              #4
            #'classes': ('collapse',),
            'fields': (('restoration', 'urban_use', 'silviculture'),),
        }),
        (_('Abundance'), {                         #5
            #'classes': ('collapse',),
            'fields': (('rare', 'max_density'),),
        }),
        (_('Endemism'), {                          #6
            #'classes': ('collapse',),
            'fields': ('endemic',),
        }),
        (_('Special features'), {                  #7
            #'classes': ('collapse',),
            'fields': (('h_flowers', 'h_leaves', 'h_fruits', 'h_crown', 'h_bark', 'h_seeds', 'h_wood', 'h_roots'),),
        }),
        (_('Successional group'), {                #8
            #'classes': ('collapse',),
            'fields': (('sg_pioneer', 'sg_early_secondary', 'sg_late_secondary', 'sg_climax'),),
        }),
        (_('Growth rate'), {                       #9
            #'classes': ('collapse',),
            'fields': (('gr_slow', 'gr_moderate', 'gr_fast'), 'gr_comments',),
        }),
        (_('Pruning'), {                           #10
            #'classes': ('collapse',),
            'fields': ('pruning',),
        }),
        (_('Flowering period'), {                  #11
            #'classes': ('collapse',),
            'fields': (('fl_start', 'fl_end'),'fl_details',),
        }),
        (_('Flowering color'), {                   #12
            #'classes': ('collapse',),
            'fields': ('fl_color','fl_color_details',),
        }),
        (_('Pollination'), {                       #13
            #'classes': ('collapse',),
            'fields': ('pollinators',),
        }),
        (_('Seed dispersal'), {                    #14
            #'classes': ('collapse',),
            'fields': (('dt_anemochorous', 'dt_autochorous', 'dt_barochorous', 'dt_hydrochorous', 'dt_zoochorous'),),
        }),
        (_('Dispersion agents'), {                 #15
            #'classes': ('collapse',),
            'fields': ('dispersers',),
        }),
        (_('Fruits'), {                            #16
            #'classes': ('collapse',),
            'fields': (('fr_class','fr_type'),),
        }),
        (_('Symbiotic association with roots'), {  #17
            #'classes': ('collapse',),
            'fields': ('symbiotic_assoc','symbiotic_details',),
        }),
        (_('Roots'), {                             #18
            #'classes': ('collapse',),
            'fields': ('r_type',),
        }),
        (_('Foliage persistence'), {               #19
            #'classes': ('collapse',),
            'fields': (('fo_evergreen', 'fo_semideciduous', 'fo_deciduous'),),
        }),
        (_('Crown diameter'), {                    #20
            #'classes': ('collapse',),
            'fields': (('cr_min_diameter', 'cr_max_diameter'),),
        }),
        (_('Crown shape'), {                       #21
            #'classes': ('collapse',),
            'fields': ('cr_shape',),
        }),
        (_('Bark texture'), {                      #22
            #'classes': ('collapse',),
            'fields': ('bark_texture',),
        }),
        (_('Trunk alignment'), {                   #23
            #'classes': ('collapse',),
            'fields': (('tr_straight', 'tr_sl_inclined', 'tr_inclined', 'tr_sl_crooked', 'tr_crooked'),),
        }),
        (_('Tree size'), {                         #24
            #'classes': ('collapse',),
            'fields': (('min_height', 'max_height'),('min_dbh', 'max_dbh'),),
        }),
        (_('Thorns or spines'), {                  #25
            #'classes': ('collapse',),
            'fields': ('thorns_or_spines',),
        }),
        (_('Toxic or allergenic'), {               #26
            #'classes': ('collapse',),
            'fields': ('toxic_or_allergenic',),
        }),
        (_('Pests and diseases'), {                #27
            #'classes': ('collapse',),
            'fields': ('pests_and_diseases',),
        }),
        (_('Fruiting period'), {                   #28
            #'classes': ('collapse',),
            'fields': (('fr_start', 'fr_end'),'fr_details',),
        }),
        (_('Seed collection'), {                   #29
            #'classes': ('collapse',),
            'fields': (('seed_tree','seed_soil'), 'seed_collection',),
        }),
        (_('Seed type'), {                         #30
            #'classes': ('collapse',),
            'fields': ('seed_type',),
        }),
        (_('Pre-germination treatment'), {         #31
            #'classes': ('collapse',),
            'fields': (('pg_no_need', 'pg_thermal', 'pg_chemical', 'pg_water', 'pg_mechanical', 'pg_combined', 'pg_other'),('pg_details'),),
        }),
        (_('Seedling production'), {               #32
            #'classes': ('collapse',),
            'fields': (('sl_seedbed','sl_containers'), 'sl_details',),
        }),
        (_('Germination time lapse'), {            #33
            #'classes': ('collapse',),
            'fields': (('seed_gmin_time','seed_gmax_time'),),
        }),
        (_('Germination rate'), {                  #34
            #'classes': ('collapse',),
            'fields': (('seed_gmin_rate','seed_gmax_rate'),),
        }),
        (_('Seeds per weight'), {                  #35
            #'classes': ('collapse',),
            'fields': (('seeds_per_weight'),),
        }),
        (_('Light requirements'), {                #36
            #'classes': ('collapse',),
            'fields': ('light','light_details',),
        }),
        (_('Terrain drainage'), {                  #37
            #'classes': ('collapse',),
            'fields': (('wetland', 'dry'),'terrain_details',),
        }),
        (_('Wood information'), {                  #38
            #'classes': ('collapse',),
            'fields': ('wood_general_info','wood_density', ('wood_has_mai_curve', 'wood_has_cai_curve', 'wood_has_biomass_equation')),
        }),
    )
    inlines = [
        SynonymsInline,               #0
        CommonNamesInline,            #1
        UsesInline,                   #2
        UseRefInline,                 #3
        HabitatsInline,               #4
        HabitatRefInline,             #5
        RarityRefInline,              #6
        EndemicRefInline,             #7
        SpecialFeaturesRefInline,     #8
        SuccessionalGroupRefInline,   #9
        GrowthRateRefInline,          #10
        RequiresPruningRefInline,     #11
        FloweringPeriodRefInline,     #12
        FloweringColorRefInline,      #13
        PollinatorsRefInline,         #14
        DispersalRefInline,           #15
        DispersersRefInline,          #16
        FruitTypeRefInline,           #17
        SymbioticRefInline,           #18
        RootSystemRefInline,          #19
        FoliagePersitenceRefInline,   #20
        CrownDiameterRefInline,       #21
        CrownShapeRefInline,          #22
        BarkTextureRefInline,         #23
        TrunkAlignmentRefInline,      #24
        SizeRefInline,                #25
        ThornsOrSpinesRefInline,      #26
        ToxicOrAllegenicRefInline,    #27
        PestsAndDiseasesRefInline,    #28
        FruitingPeriodRefInline,      #29
        SeedCollectionRefInline,      #30
        SeedTypeRefInline,            #31
        PgTreatmentRefInline,         #32
        SeedlingProductionRefInline,  #33
        GerminationTimeRefInline,     #34
        GerminationRateRefInline,     #35
        SeedsPerWeightRefInline,      #36
        LightRefInline,               #37
        TerrainRefInline,             #38
        WoodRefInline,                #39
        ConservationStatusInline,     #40
    ]

class ReferenceAdmin(admin.ModelAdmin):
    list_max_show_all = 1000

class TypeOfUseAdmin(TreeAdmin):
    fields = ['label',] # Hide tree-related fields
    def save_model(self, request, obj, form, change):
        if change:
            # Just save
            obj.save()
        else:
            # Add new record as a root node
            TypeOfUse.add_root(label=obj.label)

class StaticContentAdmin(admin.ModelAdmin):
    list_display = ('description', 'lang')

class HabitatAdmin(TreeAdmin):
    fields = ['name','htype'] # Hide tree-related fields
    def save_model(self, request, obj, form, change):
        if change:
            # Just save
            obj.save()
        else:
            # Add new record as a root node
            Habitat.add_root(name=obj.name)

admin.site.register(StaticContent, StaticContentAdmin)
admin.site.register(Taxon, TaxonAdmin)
admin.site.register(Reference, ReferenceAdmin)
admin.site.register(TypeOfUse, TypeOfUseAdmin)
admin.site.register(ConservationAssessmentSource)
admin.site.register(Interview)
admin.site.register(Habitat, HabitatAdmin)

