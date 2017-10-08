""".. Ignore pydocstyle D400.

============
Flow Filters
============

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import rest_framework_filters as filters
from django_filters.filters import BaseCSVFilter

from .models import Collection, Data, DescriptorSchema, Entity, Process


class BaseResolweFilter(filters.FilterSet):
    """Base filter for Resolwe's endpoints."""

    id = filters.AllLookupsFilter()  # pylint: disable=invalid-name
    slug = filters.AllLookupsFilter()
    name = filters.AllLookupsFilter()
    contributor = filters.NumberFilter()
    created = filters.AllLookupsFilter()
    modified = filters.AllLookupsFilter()

    class Meta:
        """Filter configuration."""

        fields = ['id', 'slug', 'name', 'contributor', 'created', 'modified']


class DescriptorSchemaFilter(BaseResolweFilter):
    """Filter the DescriptorSchema endpoint."""

    class Meta(BaseResolweFilter.Meta):
        """Filter configuration."""

        model = DescriptorSchema


class CollectionFilter(BaseResolweFilter):
    """Filter the Collection endpoint."""

    data = filters.ModelChoiceFilter(queryset=Data.objects.all())
    entity = filters.ModelChoiceFilter(queryset=Entity.objects.all())
    descriptor_schema = filters.RelatedFilter(
        DescriptorSchemaFilter, name='descriptor_schema', queryset=DescriptorSchema.objects.all()
    )
    description = filters.AllLookupsFilter()

    class Meta(BaseResolweFilter.Meta):
        """Filter configuration."""

        model = Collection
        fields = BaseResolweFilter.Meta.fields + ['data', 'entity', 'descriptor_schema', 'description']


class TagsFilter(BaseCSVFilter, filters.CharFilter):
    """Filter for tags."""

    def __init__(self, *args, **kwargs):
        """Construct tags filter."""
        kwargs.setdefault('lookup_expr', 'contains')
        super(TagsFilter, self).__init__(*args, **kwargs)


class EntityFilter(CollectionFilter):
    """Filter the Entity endpoint."""

    collection = filters.ModelChoiceFilter(queryset=Collection.objects.all())
    tags = TagsFilter()

    class Meta(BaseResolweFilter.Meta):
        """Filter configuration."""

        model = Entity
        fields = BaseResolweFilter.Meta.fields + ['collection', 'tags']


class ProcessFilter(BaseResolweFilter):
    """Filter the Process endpoint."""

    category = filters.CharFilter(name='category', lookup_expr='startswith')

    class Meta(BaseResolweFilter.Meta):
        """Filter configuration."""

        model = Process
        fields = BaseResolweFilter.Meta.fields + ['category']


class DataFilter(BaseResolweFilter):
    """Filter the Data endpoint."""

    collection = filters.RelatedFilter(CollectionFilter, queryset=Collection.objects.all())
    entity = filters.ModelChoiceFilter(queryset=Entity.objects.all())
    type = filters.CharFilter(name='process__type', lookup_expr='startswith')
    status = filters.CharFilter(lookup_expr='iexact')
    finished = filters.AllLookupsFilter()
    started = filters.AllLookupsFilter()
    process = filters.RelatedFilter(ProcessFilter, queryset=Process.objects.all())
    tags = TagsFilter()

    class Meta(BaseResolweFilter.Meta):
        """Filter configuration."""

        model = Data
        fields = BaseResolweFilter.Meta.fields + [
            'collection', 'entity', 'type', 'status', 'finished', 'started', 'process', 'tags'
        ]
