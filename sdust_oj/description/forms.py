# coding=UTF8
from django import forms
from sdust_oj.sa_conn import Session
from django.utils.translation import ugettext_lazy as _
from sdust_oj.description.models import (Item,ItemRelation,ItemRelationCombination,
                                         DescriptionMeta,DescriptionMetaItemRelationCombination,
                                         DescriptionType,DescriptionTypeItemRelationCombination,
                                         DescriptionDetail
                                         )

class ItemForm(forms.Form):
    title = forms.CharField(label=_('title'), max_length = 254)

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Item

    def save(self, commit=True, update=False,item_id=None):
        session = Session()
        
        if update:
            item = session.query(Item).get(item_id)
        else:
            item = Item()

        item.title = self.cleaned_data['title']        
        
        if not update:
            session.add(item)
        session.commit()        
        item.id = item.id
        #新建一个item 自动新建一个关系 和一个组合
        item_relation = ItemRelation(title = item.title)
        session.add(item_relation)
        session.commit()       

        item_relation.id = item_relation.id
        item_relation_combination = ItemRelationCombination(item_id =item.id,                                                                      
                                                            item_relation_id = item_relation.id,
                                                            combination_number = 1,
                                                            show_order = 1,
                                                            )
        session.add(item_relation_combination)
        session.commit()
        session.close()
        
        return item

class ItemRelationForm(forms.Form):
    title = forms.CharField(label=_('title'), max_length = 254)

    def __init__(self, *args, **kwargs):
        super(ItemRelationForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = ItemRelation

    def save(self, commit=True, update=False,item_relation_id=None):
        session = Session()
        
        if update:
            item_relation = session.query(ItemRelation).get(item_relation_id)
        else:
            item_relation = ItemRelation()

        item_relation.title = self.cleaned_data['title']        
        
        if not update:
            session.add(item_relation)
        session.commit()        
        item_relation.id = item_relation.id
        session.close()
        
        return item_relation

from sdust_oj.description.widgets import ItemRelationCombinationField 
class ItemRelationCombinationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ItemRelationCombinationForm, self).__init__(*args, **kwargs)
        
        self.item_info_list = kwargs["initial"]["item_info_list"]
        for item_info in self.item_info_list:
            self.fields[item_info.title_field_name] = ItemRelationCombinationField(label=_(item_info.item_title),required=False)

        
    class Meta:
        model = ItemRelationCombination

    def save(self, commit=True, update=False,item_relation_combination_id=None,item_relation_id=None,):

        item_relation_combination_objects = []
        choice_list = []
        
        for item_info in self.item_info_list:
            field_info_list = self.cleaned_data[item_info.title_field_name].split(',')
            choice_list.append(field_info_list[0])
            if field_info_list[0] == 'True' :
                if field_info_list[1] != 'None' and field_info_list[2] != 'None':
                    item_relation_combination = ItemRelationCombination(item_id = item_info.item_id,
                                                                        item_relation_id = item_relation_id,
                                                                        combination_number = int(field_info_list[1]),
                                                                        show_order = int(field_info_list[2]),
                                                                        )

                    item_relation_combination_objects.append(item_relation_combination)
                else:
                    return None

        if not 'True' in choice_list:
            return None
        
        session = Session()
        session.add_all(item_relation_combination_objects)
        session.commit()
        session.close()

        return item_relation_id  

class DescriptionMetaForm(forms.Form):
    title = forms.CharField(label=_('title'), max_length = 254)

    def __init__(self, *args, **kwargs):
        super(DescriptionMetaForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = DescriptionMeta

    def save(self, commit=True, update=False,description_meta_id=None):
        session = Session()
        
        if update:
            description_meta = session.query(DescriptionMeta).get(description_meta_id)
        else:
            description_meta = DescriptionMeta()

        description_meta.title = self.cleaned_data['title']        
        
        if not update:
            session.add(description_meta)
        session.commit()        
        description_meta.id = description_meta.id
        session.close()
        
        return description_meta


class DescriptionMetaItemRelationCombinationForm(forms.Form):
    item_relations = forms.MultipleChoiceField(label=_(u'可选的组合'), choices=())

    def __init__(self, *args, **kwargs):
        super(DescriptionMetaItemRelationCombinationForm, self).__init__(*args, **kwargs)
        
        item_relation_choice = kwargs["initial"]["item_relation_choice"]
        self.fields['item_relations'].choices = item_relation_choice

        
    class Meta:
        model = DescriptionMetaItemRelationCombination

    def save(self, commit=True, update=False,
             description_meta_item_relation_combination_id=None,description_meta_id=None,):

        description_meta_item_relation_combination_objects = []
        
        for item_relation_id in self.cleaned_data['item_relations']:
            obj_dmitrc = DescriptionMetaItemRelationCombination(description_meta_id = description_meta_id,
                                                                item_relation_id = item_relation_id,
                                                                )

            description_meta_item_relation_combination_objects.append(obj_dmitrc)
                       
        session = Session()
        session.add_all(description_meta_item_relation_combination_objects)
        session.commit()
        session.close()

        return description_meta_id  
    
class DescriptionTypeForm(forms.Form):
    title = forms.CharField(label=_(u'描述类型'), max_length = 254)

    def __init__(self, *args, **kwargs):
        super(DescriptionTypeForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = DescriptionType

    def save(self, commit=True, update=False, description_type_id=None,description_meta_id=None):
        session = Session()
        
        if update:
            description_type = session.query(DescriptionType).get(description_type_id)
        else:
            description_type = DescriptionType()

        description_type.title = self.cleaned_data['title']        
        description_type.description_meta_id = description_meta_id
        
        if not update:
            session.add(description_type)
        session.commit()        
        description_type.id = description_type.id
        session.close()
        
        return description_type

from sdust_oj.description.widgets import DescriptionTypeItemRelationCombinationField    
class DescriptionTypeItemRelationCombinationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(DescriptionTypeItemRelationCombinationForm, self).__init__(*args, **kwargs)
        
        self.form_info_list = kwargs["initial"]["form_info_list"]
        for obj in self.form_info_list:
            self.fields[obj.title_field_name] = DescriptionTypeItemRelationCombinationField(label=_(obj.item_relation_title),required=False)

        
    class Meta:
        model = DescriptionTypeItemRelationCombination

    def save(self, commit=True, update=False,description_type_id=None,):

        description_type_item_relation_combination_objects = []
        choice_list = []
        
        for obj in self.form_info_list:
            field_info_list = self.cleaned_data[obj.title_field_name].split(',')
            choice_list.append(field_info_list[0])
            if field_info_list[0] == 'True' :
                if field_info_list[1] != 'None' and field_info_list[2] != 'None':
#                    description_type_item_relation_combination --> obj_dtitrc
                    obj_dtitrc = DescriptionTypeItemRelationCombination(description_type_id = description_type_id,
                                                                        item_relation_id = obj.item_relation_id,
                                                                        multi_number = int(field_info_list[1]),
                                                                        show_order = int(field_info_list[2]),
                                                                        relation_items_number = obj.relation_items_number,
                                                                        )

                    description_type_item_relation_combination_objects.append(obj_dtitrc)
                else:
                    return None

        if not 'True' in choice_list:
            return None
        
        session = Session()
        session.add_all(description_type_item_relation_combination_objects)
        session.commit()
        session.close()

        return description_type_id  
    
class DescriptionDetailForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(DescriptionDetailForm, self).__init__(*args, **kwargs)
        
        self.description_detail_info_list = kwargs["initial"]["description_detail_info_list"]
        for obj in self.description_detail_info_list:
            self.fields[obj.title_field_name] = content = forms.CharField(label=_(obj.item_title), max_length = 3000) 

        
    class Meta:
        model = DescriptionDetail