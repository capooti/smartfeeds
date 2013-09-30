import floppyforms as forms

class GMapPointWidget(forms.gis.PointWidget, forms.gis.BaseGMapWidget):
    map_width = 700
    map_height = 300
    template_name = 'forms/place_detail.html'
    
class PlaceForm(forms.ModelForm):
    geometry = forms.gis.PointField(widget=GMapPointWidget)

