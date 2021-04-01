from rest_framework.relations import HyperlinkedIdentityField,HyperlinkedRelatedField
from planB_backend.urls import Apps

class CustomHyperlinkedRelatedField(HyperlinkedRelatedField):

    def get_url(self, obj, view_name, request, format):
        if hasattr(obj, 'pk') and obj.pk in (None, ''):
            return None
        lookup_value = getattr(obj, self.lookup_field)
        kwargs = {self.lookup_url_kwarg: lookup_value}
        return self.reverse(view_name, kwargs=kwargs,format=format).replace(Apps.DASHBORAD.value,'')

class CustomHyperlinkedIdentityField(HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        if hasattr(obj, 'pk') and obj.pk in (None, ''):
            return None
        lookup_value = getattr(obj, self.lookup_field)
        kwargs = {self.lookup_url_kwarg: lookup_value}
        return self.reverse(view_name, kwargs=kwargs,format=format).replace(Apps.DASHBORAD.value,'')