from django import forms
from django.utils.translation import ugettext_lazy as _

from groups.models import Group

class CreateGroupForm(forms.ModelForm):
    
    slug = forms.SlugField(max_length=20,
        help_text = _("a short version of the name consisting only of letters, numbers, underscores and hyphens."),
        error_message = _("This value must contain only letters, numbers, underscores and hyphens."))
            
    def clean_slug(self):
        reserved_slugs = [] #= ["your_groups"]
        if self.cleaned_data["slug"] in reserved_slugs:
            raise forms.ValidationError(_("The slug you've chosen is reserved for internal use."))
        if Group.objects.filter(slug__iexact=self.cleaned_data["slug"]).count() > 0:
            raise forms.ValidationError(_("A group already exists with that slug."))
        return self.cleaned_data["slug"].lower()
    
    class Meta:
        model = Group
        fields = ('name', 'slug', 'description') # @@@ tags

