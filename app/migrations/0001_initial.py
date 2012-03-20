# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Page'
        db.create_table('app_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('app', ['Page'])

        # Adding unique constraint on 'Page', fields ['code', 'lang']
        db.create_unique('app_page', ['code', 'lang'])

        # Adding model 'Reference'
        db.create_table('app_reference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('citation', self.gf('django.db.models.fields.TextField')(unique=True)),
            ('full', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('app', ['Reference'])

        # Adding model 'Taxon'
        db.create_table('app_taxon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('genus', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('species', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('subspecies', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('family', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('restoration', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('urban_use', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('h_flowers', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('h_leaves', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('h_fruits', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('h_crown', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rare', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('max_density', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('endemic', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('sg_pioneer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sg_early_secondary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sg_late_secondary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sg_climax', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gr_slow', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gr_moderate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gr_fast', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gr_comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pruning', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('fl_start', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('fl_end', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('fl_color', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('pollinators', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dt_anemochorous', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dt_autochorous', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dt_hydrochorous', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dt_zoochorous', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dispersers', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fr_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('symbiotic_assoc', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('symbiotic_details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('r_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('fo_evergreen', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fo_semideciduous', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fo_deciduous', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cr_min_diameter', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cr_max_diameter', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cr_shape', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('bark_texture', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('tr_straight', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tr_sl_inclined', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tr_inclined', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tr_sl_crooked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tr_crooked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('min_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('min_dbh', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_dbh', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('thorns_or_spines', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('toxic_or_allergenic', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('pests_and_diseases', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fr_start', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('fr_end', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('seed_tree', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('seed_soil', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('seed_collection', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('seed_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('pg_treatment', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('pg_details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sl_seedbed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sl_containers', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sl_details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('seed_gmin_time', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('seed_gmax_time', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('seed_gmin_rate', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('seed_gmax_rate', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('light', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('app', ['Taxon'])

        # Adding model 'TaxonName'
        db.create_table('app_taxonname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taxon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Taxon'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('ntype', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('app', ['TaxonName'])

        # Adding model 'ConservationAssessmentSource'
        db.create_table('app_conservationassessmentsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('acronym', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('app', ['ConservationAssessmentSource'])

        # Adding model 'ConservationStatus'
        db.create_table('app_conservationstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taxon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Taxon'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.ConservationAssessmentSource'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('app', ['ConservationStatus'])

        # Adding model 'TaxonDataReference'
        db.create_table('app_taxondatareference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taxon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Taxon'])),
            ('reference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Reference'])),
            ('data', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
        ))
        db.send_create_signal('app', ['TaxonDataReference'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Page', fields ['code', 'lang']
        db.delete_unique('app_page', ['code', 'lang'])

        # Deleting model 'Page'
        db.delete_table('app_page')

        # Deleting model 'Reference'
        db.delete_table('app_reference')

        # Deleting model 'Taxon'
        db.delete_table('app_taxon')

        # Deleting model 'TaxonName'
        db.delete_table('app_taxonname')

        # Deleting model 'ConservationAssessmentSource'
        db.delete_table('app_conservationassessmentsource')

        # Deleting model 'ConservationStatus'
        db.delete_table('app_conservationstatus')

        # Deleting model 'TaxonDataReference'
        db.delete_table('app_taxondatareference')


    models = {
        'app.conservationassessmentsource': {
            'Meta': {'object_name': 'ConservationAssessmentSource'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'app.conservationstatus': {
            'Meta': {'object_name': 'ConservationStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.ConservationAssessmentSource']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Taxon']"})
        },
        'app.page': {
            'Meta': {'ordering': "[u'title']", 'unique_together': "((u'code', u'lang'),)", 'object_name': 'Page'},
            'code': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        'app.reference': {
            'Meta': {'ordering': "[u'citation']", 'object_name': 'Reference'},
            'citation': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'full': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'app.taxon': {
            'Meta': {'ordering': "[u'label']", 'object_name': 'Taxon'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'bark_texture': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'cr_max_diameter': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cr_min_diameter': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cr_shape': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'dispersers': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dt_anemochorous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dt_autochorous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dt_hydrochorous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dt_zoochorous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'endemic': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'family': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'fl_color': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fl_end': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fl_start': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fo_deciduous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fo_evergreen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fo_semideciduous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fr_end': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fr_start': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fr_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gr_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gr_fast': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gr_moderate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gr_slow': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'h_crown': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'h_flowers': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'h_fruits': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'h_leaves': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'light': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'max_dbh': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_density': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_dbh': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pests_and_diseases': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pg_details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pg_treatment': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'pollinators': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pruning': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'r_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'rare': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'references': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Reference']", 'through': "orm['app.TaxonDataReference']", 'symmetrical': 'False'}),
            'restoration': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'seed_collection': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'seed_gmax_rate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seed_gmax_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seed_gmin_rate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seed_gmin_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seed_soil': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'seed_tree': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'seed_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'sg_climax': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sg_early_secondary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sg_late_secondary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sg_pioneer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sl_containers': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sl_details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sl_seedbed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'subspecies': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'symbiotic_assoc': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'symbiotic_details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'thorns_or_spines': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'toxic_or_allergenic': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'tr_crooked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tr_inclined': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tr_sl_crooked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tr_sl_inclined': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tr_straight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'urban_use': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'app.taxondatareference': {
            'Meta': {'object_name': 'TaxonDataReference'},
            'data': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Reference']"}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Taxon']"})
        },
        'app.taxonname': {
            'Meta': {'object_name': 'TaxonName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'ntype': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Taxon']"})
        }
    }

    complete_apps = ['app']
