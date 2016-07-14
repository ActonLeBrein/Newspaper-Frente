# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Delegacion'
        db.create_table(u'app_delegacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion_Delegacion', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'app', ['Delegacion'])

        # Adding model 'Colonia'
        db.create_table(u'app_colonia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion_Colonia', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('delegacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Delegacion'])),
        ))
        db.send_create_signal(u'app', ['Colonia'])

        # Adding model 'Delegacion_frente'
        db.create_table(u'app_delegacion_frente', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion_Delegacion', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'app', ['Delegacion_frente'])

        # Adding model 'Colonia_frente'
        db.create_table(u'app_colonia_frente', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion_Colonia', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('delegacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Delegacion_frente'])),
        ))
        db.send_create_signal(u'app', ['Colonia_frente'])

        # Adding model 'Ruta'
        db.create_table(u'app_ruta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('numero_Ruta', self.gf('django.db.models.fields.IntegerField')()),
            ('descripcion_Ruta', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Ruta'])

        # Adding model 'Repartidor'
        db.create_table(u'app_repartidor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('apellido_Paterno', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('apellido_Materno', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Repartidor'])

        # Adding M2M table for field rutas on 'Repartidor'
        m2m_table_name = db.shorten_name(u'app_repartidor_rutas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('repartidor', models.ForeignKey(orm[u'app.repartidor'], null=False)),
            ('ruta', models.ForeignKey(orm[u'app.ruta'], null=False))
        ))
        db.create_unique(m2m_table_name, ['repartidor_id', 'ruta_id'])

        # Adding model 'Categoria'
        db.create_table(u'app_categoria', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion_Categoria', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Categoria'])

        # Adding model 'Canal_distribucion'
        db.create_table(u'app_canal_distribucion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion_Distribucion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Canal_distribucion'])

        # Adding model 'Subcategoria1'
        db.create_table(u'app_subcategoria1', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion_SubCategoria1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Subcategoria1'])

        # Adding model 'Subcategoria2'
        db.create_table(u'app_subcategoria2', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion_SubCategoria2', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Subcategoria2'])

        # Adding model 'Subcategoria3'
        db.create_table(u'app_subcategoria3', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion_SubCategoria3', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Subcategoria3'])

        # Adding model 'Cliente'
        db.create_table(u'app_cliente', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('apellido_Materno', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('apellido_Paterno', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('puesto', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('telefono', self.gf('django.db.models.fields.IntegerField')(unique=True, max_length=10)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Cliente'])

        # Adding model 'Empresa'
        db.create_table(u'app_empresa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombreEmpresa', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('calle', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('numero_Exterior', self.gf('django.db.models.fields.IntegerField')()),
            ('numero_Interior', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('Colonia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Colonia'])),
            ('delegacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Delegacion'])),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Cliente'])),
            ('categoria', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Categoria'], null=True)),
            ('subcategoria1', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Subcategoria1'], null=True)),
            ('subcategoria2', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Subcategoria2'], null=True)),
            ('subcategoria3', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Subcategoria3'], null=True)),
            ('position', self.gf('geoposition.fields.GeopositionField')(default='0,0', max_length=42, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Empresa'])

        # Adding M2M table for field rutas on 'Empresa'
        m2m_table_name = db.shorten_name(u'app_empresa_rutas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('empresa', models.ForeignKey(orm[u'app.empresa'], null=False)),
            ('ruta', models.ForeignKey(orm[u'app.ruta'], null=False))
        ))
        db.create_unique(m2m_table_name, ['empresa_id', 'ruta_id'])

        # Adding model 'Membresia'
        db.create_table(u'app_membresia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('duracion', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
        ))
        db.send_create_signal(u'app', ['Membresia'])

        # Adding model 'Cupon'
        db.create_table(u'app_cupon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cupon', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('cantidad', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('cuponusado', self.gf('django.db.models.fields.IntegerField')(max_length=50, null=True, blank=True)),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('fechafinal', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('usuariogen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('membresia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Membresia'], null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Cupon'])

        # Adding model 'Cuponera'
        db.create_table(u'app_cuponera', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fechainicio', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('fechafinal', self.gf('django.db.models.fields.DateField')()),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Cliente'])),
            ('cupon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Cupon'])),
        ))
        db.send_create_signal(u'app', ['Cuponera'])

        # Adding model 'ClienteFrente'
        db.create_table(u'app_clientefrente', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('apellido_Materno', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('apellido_Paterno', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('cumpleanos', self.gf('django.db.models.fields.DateField')()),
            ('telefono', self.gf('django.db.models.fields.IntegerField')(max_length=15, null=True, blank=True)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('calle', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('cp', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('numero_Exterior', self.gf('django.db.models.fields.IntegerField')(max_length=10000)),
            ('numero_Interior', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('Colonia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Colonia_frente'])),
            ('delegacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Delegacion_frente'])),
            ('entregas', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('cupon', self.gf('django.db.models.fields.CharField')(max_length=4, null=True)),
            ('fvencimiento', self.gf('django.db.models.fields.DateField')(null=True)),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('categoria', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Categoria'], null=True)),
            ('subcategoria1', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Subcategoria1'], null=True)),
            ('subcategoria2', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Subcategoria2'], null=True)),
            ('subcategoria3', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Subcategoria3'], null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['ClienteFrente'])

        # Adding M2M table for field rutas on 'ClienteFrente'
        m2m_table_name = db.shorten_name(u'app_clientefrente_rutas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('clientefrente', models.ForeignKey(orm[u'app.clientefrente'], null=False)),
            ('ruta', models.ForeignKey(orm[u'app.ruta'], null=False))
        ))
        db.create_unique(m2m_table_name, ['clientefrente_id', 'ruta_id'])


    def backwards(self, orm):
        # Deleting model 'Delegacion'
        db.delete_table(u'app_delegacion')

        # Deleting model 'Colonia'
        db.delete_table(u'app_colonia')

        # Deleting model 'Delegacion_frente'
        db.delete_table(u'app_delegacion_frente')

        # Deleting model 'Colonia_frente'
        db.delete_table(u'app_colonia_frente')

        # Deleting model 'Ruta'
        db.delete_table(u'app_ruta')

        # Deleting model 'Repartidor'
        db.delete_table(u'app_repartidor')

        # Removing M2M table for field rutas on 'Repartidor'
        db.delete_table(db.shorten_name(u'app_repartidor_rutas'))

        # Deleting model 'Categoria'
        db.delete_table(u'app_categoria')

        # Deleting model 'Canal_distribucion'
        db.delete_table(u'app_canal_distribucion')

        # Deleting model 'Subcategoria1'
        db.delete_table(u'app_subcategoria1')

        # Deleting model 'Subcategoria2'
        db.delete_table(u'app_subcategoria2')

        # Deleting model 'Subcategoria3'
        db.delete_table(u'app_subcategoria3')

        # Deleting model 'Cliente'
        db.delete_table(u'app_cliente')

        # Deleting model 'Empresa'
        db.delete_table(u'app_empresa')

        # Removing M2M table for field rutas on 'Empresa'
        db.delete_table(db.shorten_name(u'app_empresa_rutas'))

        # Deleting model 'Membresia'
        db.delete_table(u'app_membresia')

        # Deleting model 'Cupon'
        db.delete_table(u'app_cupon')

        # Deleting model 'Cuponera'
        db.delete_table(u'app_cuponera')

        # Deleting model 'ClienteFrente'
        db.delete_table(u'app_clientefrente')

        # Removing M2M table for field rutas on 'ClienteFrente'
        db.delete_table(db.shorten_name(u'app_clientefrente_rutas'))


    models = {
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
            'cantidad': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cupon': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'cuponusado': ('django.db.models.fields.IntegerField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'fechafinal': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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