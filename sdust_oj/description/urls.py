from django.conf.urls.defaults import patterns, url
from sdust_oj.description.models import (Item,ItemRelation,
                                         DescriptionMeta)
from sdust_oj.description.views import (show_list,item_add,item_relation_add,
                                        item_relation_combine_add,item_relation_detail,
                                        description_meta_add,description_meta_detail,
                                        description_meta_item_relation_combine_add)

urlpatterns = patterns('',
    url(r'^item_list/(?P<page>\d{,10})/$',
                     show_list,
                    {'template':'description/item_list.html',
                     'ItemClass':Item},
                     name="item_list"),
    url(r'^item_add/$', item_add,name="item_add"),
    
    url(r'^item_relation_list/(?P<page>\d{,10})/$',
                     show_list,
                    {'template':'description/item_relation_list.html',
                     'ItemClass':ItemRelation},
                     name="item_relation_list"),
    url(r'^item_relation_add/$', item_relation_add,name="item_relation_add"),
    url(r'^item_relation_combine_add/(?P<item_relation_id>\d{,10})/$', item_relation_combine_add,name="item_relation_combine_add"),
    url(r'^item_relation_detail/(?P<item_relation_id>\d{,10})/$', item_relation_detail,name="item_relation_detail"),

    url(r'^description_meta_list/(?P<page>\d{,10})/$',
                     show_list,
                    {'template':'description/description_meta_list.html',
                     'ItemClass':DescriptionMeta},
                     name="description_meta_list"),
    url(r'^description_meta_add/$', description_meta_add,name="description_meta_add"),
    url(r'^description_meta_item_relation_combine_add/(?P<description_meta_id>\d{,10})/$', 
        description_meta_item_relation_combine_add,name="description_meta_item_relation_combine_add"),
    url(r'^description_meta_detail/(?P<description_meta_id>\d{,10})/$', description_meta_detail,name="description_meta_detail"),

)