from rest_framework import serializers

from repository.models import *


class ProjectSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='project-detail')

    class Meta:
        model = Project
        fields = ('id', 'project_name', 'project_desc', 'url')


class SampleParameterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name', read_only=True)

    class Meta:
        model = SampleParameterMap
        fields = ('id', 'fcs_text', 'fcs_number', 'name')
        depth = 1


class SampleSerializer(serializers.ModelSerializer):
    sampleparameters = SampleParameterSerializer(source='sampleparametermap_set')
    url = serializers.HyperlinkedIdentityField(view_name='sample-detail')
    project = serializers.IntegerField(source='subject.project.id', read_only=True)

    class Meta:
        model = Sample
        fields = ('id', 'url', 'visit', 'subject', 'site', 'project', 'original_filename', 'sampleparameters')
        read_only_fields = ('original_filename', 'visit')


class SamplePOSTSerializer(serializers.ModelSerializer):
    sampleparameters = SampleParameterSerializer(source='sampleparametermap_set')
    url = serializers.HyperlinkedIdentityField(view_name='sample-detail')
    project = serializers.IntegerField(source='subject.project.id', read_only=True)

    class Meta:
        model = Sample
        fields = ('id', 'url', 'visit', 'subject', 'site', 'project', 'original_filename', 'sampleparameters', 'sample_file')
        read_only_fields = ('original_filename', 'visit')
