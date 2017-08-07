from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from nfbr.core.models import Tbusuario, Tbcontribuinte, Tbcfop, Tbcst, TbentradaNf, Tbproduto


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Tbusuario
        fields = ('email', 'nome')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Tbusuario
        fields = ('email', 'password', 'nome')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class TbcontribuinteForm(forms.ModelForm):
    class Meta:
        model = Tbcontribuinte
        fields = '__all__'


class TbcfopForm(forms.ModelForm):
    class Meta:
        model = Tbcfop
        fields = '__all__'


class TbcstForm(forms.ModelForm):
    class Meta:
        model = Tbcst
        fields = '__all__'


class TbentradaNfForm(forms.ModelForm):
    class Meta:
        model = TbentradaNf
        fields = '__all__'


class TbprodutoForm(forms.ModelForm):
    class Meta:
        model = Tbproduto
        fields = '__all__'
