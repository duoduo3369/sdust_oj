from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import Http404
from sdust_oj.sa_conn import Session
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import settings
from sdust_oj.description.forms import (ItemForm,ItemRelationForm,ItemRelationCombinationForm,
                                        DescriptionMetaForm,DescriptionMetaItemRelationCombinationForm,
                                        )
from sdust_oj.description.models import (Item,ItemRelation,ItemRelationCombination,
                                         ItemRelationViewDetail,ItemRelationCombinationFormInfo,
                                         DescriptionMeta,DescriptionMetaItemRelationCombination,
                                         DescriptionMetaItemRelationCombinationFormInfo,
                                         DescriptionMetaItemRelationViewDetail,
                                         DescriptionType,
                                         )

def show_list(request, template, ItemClass, page=1):
    session = Session()
    objects_all = session.query(ItemClass).all()
    session.close()
    
    paginator = Paginator(objects_all, settings.METAS_PER_PAGE)
    
    try:
        objects = paginator.page(objects_all)
    except (EmptyPage, InvalidPage):
        objects = paginator.page(paginator.num_pages)
    data = {"objects": objects}
    return render_to_response(template, data,
                              context_instance=RequestContext(request))

def item_add(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            data = {'template':'description/item_list.html',
                     'ItemClass':Item,
                     'page':1,
                     }
            return HttpResponseRedirect(reverse('item_list', kwargs=data)) 

    else:
        form = ItemForm()
        
    data = {'form': form}
    return render_to_response("description/item_add.html", data, context_instance=RequestContext(request)) 

def item_relation_add(request):
    if request.method == 'POST':
        form = ItemRelationForm(request.POST)
        if form.is_valid():
            item_relation = form.save()
            data = {'item_relation_id':item_relation.id,}
            return HttpResponseRedirect(reverse('item_relation_combine_add', kwargs=data)) 

    else:
        form = ItemRelationForm()
        
    data = {'form': form}
    return render_to_response("description/item_relation_add.html", data, context_instance=RequestContext(request)) 

def item_relation_detail(request,item_relation_id):
    session = Session() 
    
    item_relation_object = session.query(ItemRelation).get(item_relation_id)
    items_in_relation = session.query(ItemRelationCombination).filter(ItemRelationCombination.item_relation_id == item_relation_id)
    item_relation_detail_object_list = []
    for i_in_relation in items_in_relation:
        item_object = session.query(Item).get(i_in_relation.item_id)
        item_relation_detail_object = ItemRelationViewDetail(item_id = item_object.id,                                                            
                                                             item_title=item_object.title,
                                                             combination_number = i_in_relation.combination_number, 
                                                             show_order = i_in_relation.show_order,
                                                             )
        item_relation_detail_object_list.append(item_relation_detail_object)
    session.close()
    if item_relation_object is None:
        raise Http404
     
    data = {'item_relation_object':item_relation_object,'detail_list':item_relation_detail_object_list}
    return render_to_response("description/item_relation_detail.html", data, context_instance=RequestContext(request)) 

    
def item_relation_combine_add(request,item_relation_id):
    session = Session()
    item_objects = session.query(Item).all()
    item_relation_object = session.query(ItemRelation).get(item_relation_id)
    session.close()
    
    if item_relation_object is None:
        raise Http404
    item_info_list = []
    for item in item_objects:
        item_info_object = ItemRelationCombinationFormInfo(item_id=item.id,item_title=item.title)
        item_info_list.append(item_info_object)
    
    initial={"item_info_list":item_info_list,}    
    if request.method == 'POST':
        form = ItemRelationCombinationForm(request.POST,initial=initial,auto_id=False)
        if form.is_valid():
            id = form.save(item_relation_id = item_relation_id)
            if id is not None:
                data = {'template':'description/item_relation_list.html',
                     'ItemClass':ItemRelation,
                     'page':1,
                     }
                return HttpResponseRedirect(reverse('item_relation_list', kwargs=data)) 
    else:
        form = ItemRelationCombinationForm(initial=initial,auto_id=False)
        
    data = {'form': form,'item_relation_id':item_relation_id}
    
    return render_to_response("description/item_relation_combine_add.html", data, context_instance=RequestContext(request)) 


def description_meta_add(request):
    if request.method == 'POST':
        form = DescriptionMetaForm(request.POST)
        if form.is_valid():
            description_meta = form.save()
            data = {'description_meta_id':description_meta.id,}
            return HttpResponseRedirect(reverse('description_meta_item_relation_combine_add', kwargs=data)) 

    else:
        form = DescriptionMetaForm()
        
    data = {'form': form}
    return render_to_response("description/description_meta_add.html", data, context_instance=RequestContext(request)) 

def description_meta_item_relation_combine_add(request,description_meta_id):
    session = Session()
    item_relation_objects = session.query(ItemRelation).all()
    description_meta_object = session.query(DescriptionMeta).get(description_meta_id)
    session.close()
    
    if description_meta_object is None:
        raise Http404
    
    description_meta_item_relation_info_list = []
    for item_relation in item_relation_objects:
        description_meta_item_relation_info_object = DescriptionMetaItemRelationCombinationFormInfo(item_relation_id=item_relation.id,item_relation_title=item_relation.title)
        description_meta_item_relation_info_list.append(description_meta_item_relation_info_object)
    
    initial={"description_meta_item_relation_info_list":description_meta_item_relation_info_list,}
        
    if request.method == 'POST':
        form = DescriptionMetaItemRelationCombinationForm(request.POST,initial=initial,auto_id=False)
        if form.is_valid():
            id = form.save(description_meta_id = description_meta_id)
            if id is not None:
                data = {'template':'description/description_meta_list.html',
                     'ItemClass':DescriptionMeta,
                     'page':1,
                     }
                return HttpResponseRedirect(reverse('description_meta_list', kwargs=data)) 
    else:
        form = DescriptionMetaItemRelationCombinationForm(initial=initial,auto_id=False)
        
    data = {'form': form,'description_meta_id':description_meta_id}
    
    return render_to_response("description/description_meta_item_relation_combine_add.html", data, context_instance=RequestContext(request)) 


def description_meta_detail(request,description_meta_id):
    session = Session() 
    
    description_meta_object = session.query(DescriptionMeta).get(description_meta_id)
    objs_in_relation = session.query(DescriptionMetaItemRelationCombination).filter(DescriptionMetaItemRelationCombination.description_meta_id == description_meta_id)

    description_meta_item_relation_detail_object_list = []
    for obj in objs_in_relation:
        item_relation_object = session.query(ItemRelation).get(obj.item_relation_id)
        item_relation_detail_object = DescriptionMetaItemRelationViewDetail(item_relation_id = item_relation_object.id,                                                            
                                                             item_relation_title = item_relation_object.title,
                                                             multi_number = obj.multi_number, 
                                                             )
        description_meta_item_relation_detail_object_list.append(item_relation_detail_object)
    session.close()
    
    if description_meta_object is None:
        raise Http404
        
    data = {'description_meta_object':description_meta_object,'detail_list':description_meta_item_relation_detail_object_list}
    return render_to_response("description/description_meta_detail.html", data, context_instance=RequestContext(request)) 
