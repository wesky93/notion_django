# Create your views here.
from django.http import Http404
from django.shortcuts import _get_queryset
from rest_framework import viewsets

from .models import Collection, LayoutPage, Page
from .serializers import CollectionPageSerializer, LayoutPageSerializer, PageListSerializer


def get_subclass_object_or_404(klass, *args, **kwargs):
    """
    Use get() to return an object, or raise a Http404 exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'get_subclass'):
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        result = queryset.get_subclass(*args, **kwargs)
        print(result)
        return result
    except queryset.model.DoesNotExist:
        raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    queryset = Page.objects.all()
    serializer_class = PageListSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        obj = get_subclass_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_serializer(self, *args, **kwargs):
        if isinstance(args[0], LayoutPage):
            serializer_class = LayoutPageSerializer
        elif isinstance(args[0], Collection):
            serializer_class = CollectionPageSerializer
        else:
            return super(PageViewSet, self).get_serializer(*args, **kwargs)

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)
