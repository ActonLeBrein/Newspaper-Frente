# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Campania'
        db.create_table(u'app_campania', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Campania'])

        # Adding model 'Aliados'
        db.create_table(u'app_aliados', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Aliados'])

        # Adding M2M table for field campania on 'Aliados'
        m2m_table_name = db.shorten_name(u'app_aliados_campania')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aliados', models.ForeignKey(orm[u'app.aliados'], null=False)),
            ('campania', models.ForeignKey(orm[u'app.campania'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aliados_id', 'campania_id'])

        # Adding field 'Cupon.mail_cliente'
        db.add_column(u'app_cupon', 'mail_cliente',
                      self.gf('django.db.models.fields.EmailField')(max_length=50, null=True),
                      keep_default=False)

        # Adding field 'Cupon.campania'
        db.add_column(u'app_cupon', 'campania',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Campania'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Campania'
        db.delete_table(u'app_campania')

        # Deleting model 'Aliados'
        db.delete_table(u'app_aliados')

        # Removing M2M table for field campania on 'Aliados'
        db.delete_table(db.shorten_name(u'app_aliados_campania'))

        # Deleting field 'Cupon.mail_cliente'
        db.delete_column(u'app_cupon', 'mail_cliente')

        # Deleting field 'Cupon.campania'
        db.delete_column(u'app_cupon', 'campania_id')


    models = {
        u'app.aliados': {
            'Meta': {'object_name': 'Aliados'},
            'campania': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Campania']", 'symmetrical': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app.campania': {
            'Meta': {'object_name': 'Campania'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app.canal_distribucion': {
            'Meta': {'object_name': 'Canal_distribucion'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descripcion_Distribucion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app.categoria': {
            'Meta': {'object_name': 'Categoria'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descripcion_Categoria': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app.cliente': {
            'Meta': {'object_name': 'Cliente'},
            'apellido_Materno': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'apellido_Paterno': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'puesto': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'telefono': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'max_length': '10'})
        },
        u'app.clientefrente': {
            'Colonia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Colonia_frente']"}),
            'Meta': {'object_name': 'ClienteFrente'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'apellido_Materno': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'apellido_Paterno': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'calle': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'categoria': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Categoria']", 'null': 'True'}),
            'cp': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cumpleanos': ('django.db.models.fields.DateField', [], {}),
            'cupon': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'delegacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Delegacion_frente']"}),
            'entregas': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'fvencimiento': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numero_Exterior': ('django.db.models.fields.IntegerField', [], {'max_length': '10000'}),
            'numero_Interior': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'rutas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Ruta']", 'null': 'True', 'symmetrical': 'False'}),
            'subcategoria1': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Subcategoria1']", 'null': 'True'}),
            'subcategoria2': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Subcategoria2']", 'null': 'True'}),
            'subcategoria3': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Subcategoria3']", 'null': 'True'}),
            'telefono': ('django.db.models.fields.IntegerField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        u'app.colonia': {
            'Meta': {'object_name': 'Colonia'},
            'delegacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Delegacion']"}),
            'descripcion_Colonia': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app.colonia_frente': {
            'Meta': {'object_name': 'Colonia_frente'},
            'delegacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Delegacion_frente']"}),
            'descripcion_Colonia': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app.cupon': {
            'Meta': {'object_name': 'Cupon'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'campania': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Campania']", 'null': 'True'}),
            'cantidad': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cupon': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'cuponusado': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'fechafinal': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_cliente': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'null': 'True'}),
            'membresia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Membresia']", 'null': 'True'}),
            'usuariogen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'app.cuponera': {
            'Meta': {'object_name': 'Cuponera'},
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Cliente']"}),
            'cupon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Cupon']"}),
            'fechafinal': ('django.db.models.fields.DateField', [], {}),
            'fechainicio': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app.delegacion': {
            'Meta': {'object_name': 'Delegacion'},
            'descripcion_Delegacion': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app.delegacion_frente': {
            'Meta': {'object_name': 'Delegacion_frente'},
            'descripcion_Delegacion': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app.empresa': {
            'Colonia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Colonia']"}),
            'Meta': {'object_name': 'Empresa'},
            'calle': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'categoria': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Categoria']", 'null': 'True'}),
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Cliente']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delegacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Delegacion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombreEmpresa': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numero_Exterior': ('django.db.models.fields.IntegerField', [], {}),
            'numero_Interior': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'position': ('geoposition.fields.GeopositionField', [], {'default': "'0,0'", 'max_length': '42', 'null': 'True'}),
            'rutas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Ruta']", 'symmetrical': 'False'}),
            'subcategoria1': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Subcategoria1']", 'null': 'True'}),
            'subcategoria2': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Subcategoria2']", 'null': 'True'}),
            'subcategoria3': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Subcategoria3']", 'null': 'True'})
        },
        u'app.membresia': {
            'Meta': {'object_name': 'Membresia'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'duracion': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app.repartidor': {
            'Meta': {'object_name': 'Repartidor'},
            'apellido_Materno': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'apellido_Paterno': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rutas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Ruta']", 'symmetrical': 'False'})
        },
        u'app.ruta': {
            'Meta': {'object_name': 'Ruta'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descripcion_Ruta': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_Ruta': ('django.db.models.fields.IntegerField', [], {})
        },
        u'app.subcategoria1': {
            'Meta': {'object_name': 'Subcategoria1'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descripcion_SubCategoria1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app.subcategoria2': {
            'Meta': {'object_name': 'Subcategoria2'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descripcion_SubCategoria2': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'app.subcategoria3': {
            'Meta': {'object_name': 'Subcategoria3'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descripcion_SubCategoria3': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']