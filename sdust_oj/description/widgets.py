# coding=UTF8

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms.util import ErrorList

class ItemRelationCombinationWidget(forms.MultiWidget):

    def __init__(self, attrs=None):
        widgets = (
            forms.CheckboxInput(attrs={'class':'check_box'}),
            forms.TextInput(attrs={'class':'combination_number_filed'}),
            forms.TextInput(attrs={'class':'show_number_filed'}),            

            )
        super(ItemRelationCombinationWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(',')
        return [None, None, None]
    
    def format_output(self, rendered_widgets):
        output_string = u''
        output_string += "<td class='check_box_td'>%s</td>" % (rendered_widgets[0])
        output_string += "<td class='combination_number_td'>%s</td>" % (rendered_widgets[1])
        output_string += "<td class='show_number_td'>%s</td>" % (rendered_widgets[2])
        

        return output_string

class ItemRelationCombinationField(forms.MultiValueField):

    widget = ItemRelationCombinationWidget

    def __init__(self, *args, **kwargs):
        fields = (
            forms.BooleanField(required=False),
            forms.IntegerField(label=u'组和中的个数',required=False),
            forms.IntegerField(label=u'组合时显示的顺序',required=False),            

            )
        super(ItemRelationCombinationField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):

        return str(data_list[0]) + ',' + str(data_list[1]) + ',' + str(data_list[2])
           
class DescriptionTypeItemRelationCombinationWidget(forms.MultiWidget):

    def __init__(self, attrs=None):
        widgets = (
            forms.CheckboxInput(attrs={'class':'check_box'}),
            forms.TextInput(attrs={'class':'multi_number_td'}),            
            forms.TextInput(attrs={'class':'show_number_filed'}),            

            )
        super(DescriptionTypeItemRelationCombinationWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(',')
        return [None, None,None]
    
    def format_output(self, rendered_widgets):
        output_string = u''
        output_string += "<td class='check_box_td'>%s</td>" % (rendered_widgets[0])
        output_string += "<td class='multi_number_td'>%s</td>" % (rendered_widgets[1])
        output_string += "<td class='show_number_td'>%s</td>" % (rendered_widgets[2])
                

        return output_string

class DescriptionTypeItemRelationCombinationField(forms.MultiValueField):

    widget = DescriptionTypeItemRelationCombinationWidget

    def __init__(self, *args, **kwargs):
        fields = (
            forms.BooleanField(required=False),
            forms.IntegerField(label=u'多选个数',required=False),            
            forms.IntegerField(label=u'组合时显示的顺序',required=False),            

            )
        super(DescriptionTypeItemRelationCombinationField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):

        return str(data_list[0]) + ',' + str(data_list[1]) + ',' + str(data_list[2]) 
