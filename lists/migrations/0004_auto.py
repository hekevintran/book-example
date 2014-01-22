# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field shared_with on 'List'
        m2m_table_name = db.shorten_name('lists_list_shared_with')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('list', models.ForeignKey(orm['lists.list'], null=False)),
            ('user', models.ForeignKey(orm['accounts.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['list_id', 'user_id'])


    def backwards(self, orm):
        # Removing M2M table for field shared_with on 'List'
        db.delete_table(db.shorten_name('lists_list_shared_with'))


    models = {
        'accounts.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'lists.item': {
            'Meta': {'unique_together': "(('list', 'text'),)", 'ordering': "('id',)", 'object_name': 'Item'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lists.List']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'lists.list': {
            'Meta': {'object_name': 'List'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['accounts.User']", 'null': 'True'}),
            'shared_with': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['accounts.User']", 'related_name': "'shared_lists'"})
        }
    }

    complete_apps = ['lists']