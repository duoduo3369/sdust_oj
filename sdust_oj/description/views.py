# coding=UTF8
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import Http404
from sdust_oj.sa_conn import Session
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import settings
from sdust_oj.problem.models import Description
from sdust_oj.description.forms import (ItemForm,ItemRelationForm,ItemRelationCombinationForm,
                                        DescriptionMetaForm,DescriptionMetaItemRelationCombinationForm,
                                        DescriptionTypeForm,DescriptionTypeItemRelationCombinationForm,
                                        DescriptionDetailForm
                                        )
from sdust_oj.description.models import (Item,ItemRelation,ItemRelationCombination,
                                         ItemRelationViewDetail,ItemRelationCombinationFormInfo,
                                         DescriptionMeta,DescriptionMetaItemRelationCombination,
                                         DescriptionMetaItemRelationCombinationFormInfo,
                                         DescriptionTypeItemRelationViewDetail,
                                         DescriptionType,DescriptionTypeItemRelationCombination,
                                         DescriptionDetailFormInfo
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
    
    item_relation_choice = [(obj.id,obj.title) for obj in item_relation_objects]  
   
    initial={"item_relation_choice":item_relation_choice,}
        
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
        
    data = {'form': form,'description_meta_object':description_meta_object}
    
    return render_to_response("description/description_meta_item_relation_combine_add.html", data, context_instance=RequestContext(request)) 


def description_meta_detail(request,description_meta_id):
    session = Session() 
    
    description_meta_object = session.query(DescriptionMeta).get(description_meta_id)
    objs_in_relation = session.query(DescriptionMetaItemRelationCombination).filter(DescriptionMetaItemRelationCombination.description_meta_id == description_meta_id)

    description_meta_item_relation_detail_object_list = []
    for obj in objs_in_relation:
        item_relation_object = session.query(ItemRelation).get(obj.item_relation_id)
        item_relation_detail_object = DescriptionTypeItemRelationViewDetail(item_relation_id = item_relation_object.id,                                                            
                                                             item_relation_title = item_relation_object.title,
                                                             )
        description_meta_item_relation_detail_object_list.append(item_relation_detail_object)
    session.close()
    
    if description_meta_object is None:
        raise Http404
        
    data = {'description_meta_object':description_meta_object,'detail_list':description_meta_item_relation_detail_object_list}
    return render_to_response("description/description_meta_detail.html", data, context_instance=RequestContext(request)) 

def description_type_list(request, description_meta_id, page=1):
    session = Session()
    description_meta_object = session.query(DescriptionMeta).get(description_meta_id)
    session.close()
    if description_meta_object is None:
        raise Http404 
    description_type_objects = session.query(DescriptionType).filter(DescriptionType.description_meta_id == description_meta_id)

    paginator = Paginator(description_type_objects, settings.METAS_PER_PAGE)
    
    try:
        objects = paginator.page(description_type_objects)
    except (EmptyPage, InvalidPage):
        objects = paginator.page(paginator.num_pages)
    data = {"objects": objects,"description_meta_object":description_meta_object}
    return render_to_response("description/description_type_list.html", data,
                              context_instance=RequestContext(request))

def description_type_add(request, description_meta_id):
    session = Session()
    description_meta_object = session.query(DescriptionMeta).get(description_meta_id)
    session.close()

    if description_meta_object is None:
        raise Http404 
    if request.method == 'POST':
        form = DescriptionTypeForm(request.POST)
        
        if form.is_valid():
            description_type = form.save(description_meta_id=description_meta_id)
            data = {'description_type_id':description_type.id, }
            return HttpResponseRedirect(reverse('description_type_item_relation_combine_add', kwargs=data))
    else:
        form = DescriptionTypeForm()
    
   
    data = {'form': form, 'description_meta_id':description_meta_id}
    return render_to_response("description/description_type_add.html", data, context_instance=RequestContext(request)) 


def description_type_item_relation_combine_add(request,description_type_id):
    session = Session()
    description_type_object = session.query(DescriptionType).get(description_type_id)
    
    if description_type_object is None:
        raise Http404
    description_meta_id = description_type_object.description_meta_id
    
    description_meta_object = session.query(DescriptionMeta).get(description_meta_id)
    if description_meta_object is None:
        raise Http404
    
    objs_in_relation = session.query(DescriptionMetaItemRelationCombination).filter(DescriptionMetaItemRelationCombination.description_meta_id == description_meta_id)

    form_info_list = []
    for obj in objs_in_relation:
        item_relation_object = session.query(ItemRelation).get(obj.item_relation_id)
        objs_in_relation_combination = session.query(ItemRelationCombination).filter(ItemRelationCombination.item_relation_id == item_relation_object.id)
        relation_items_number = 0
        for o in objs_in_relation_combination:
            relation_items_number += o.combination_number
        form_info_obj = DescriptionMetaItemRelationCombinationFormInfo(item_relation_id = item_relation_object.id,                                                            
                                                             item_relation_title = item_relation_object.title,
                                                             relation_items_number = relation_items_number
                                                             )
        form_info_list.append(form_info_obj)
    session.close()    

     
   
    initial={"form_info_list":form_info_list,}
        
    if request.method == 'POST':
        form = DescriptionTypeItemRelationCombinationForm(request.POST,initial=initial,auto_id=False)
        if form.is_valid():
            id = form.save(description_type_id = description_type_id)
            if id is not None:
                 
                data = {'description_meta_id':description_meta_id,'page':1}
                return HttpResponseRedirect(reverse('description_type_list', kwargs=data)) 
    else:
        form = DescriptionTypeItemRelationCombinationForm(initial=initial,auto_id=False)
        
    data = {'form': form,'description_type_id':description_type_id}
    
    return render_to_response("description/description_type_item_relation_combine_add.html", data, context_instance=RequestContext(request)) 

def description_type_detail(request,description_type_id):
    session = Session() 
    
    description_type_object = session.query(DescriptionType).get(description_type_id)
    description_meta_object = session.query(DescriptionMeta).get(description_type_object.description_meta_id)

    if description_type_object is None or description_meta_object is None:
        raise Http404
    objs_in_relation = session.query(DescriptionTypeItemRelationCombination).\
    filter(DescriptionTypeItemRelationCombination.description_type_id == description_type_id).\
    order_by(DescriptionTypeItemRelationCombination.show_order)

    description_type_item_relation_detail_object_list = []
    for obj in objs_in_relation:
        item_relation_object = session.query(ItemRelation).get(obj.item_relation_id)
        item_relation_detail_object = DescriptionTypeItemRelationViewDetail(item_relation_id = item_relation_object.id,                                                            
                                                             item_relation_title = item_relation_object.title,
                                                             multi_number = obj.multi_number, 
                                                             show_order = obj.show_order,
                                                             )
        description_type_item_relation_detail_object_list.append(item_relation_detail_object)
    session.close()
    

        
    data = {'description_type_object':description_type_object,
            'description_meta_object':description_meta_object,
            'detail_list':description_type_item_relation_detail_object_list}
    return render_to_response("description/description_type_detail.html", data, context_instance=RequestContext(request)) 

def description_detail_add(request, description_type_id,description_id):
    session = Session()
    description_type_object = session.query(DescriptionType).get(description_type_id)
    description_object = session.query(Description).get(description_id)
    if description_type_object is None or description_object is None:
        raise Http404
    #查询出这个描述类型下的所有组合
    objs_in_relation = session.query(DescriptionTypeItemRelationCombination).\
    filter(DescriptionTypeItemRelationCombination.description_type_id == description_type_id).\
    order_by(DescriptionTypeItemRelationCombination.show_order)
    
    description_detail_info_list = []
    item_show_number = 1
    relation_show_number = 1
    
    for obj in objs_in_relation:
        #得到这个描述中的一条组合，已经按照show_order排序
        item_relation_object = session.query(ItemRelation).get(obj.item_relation_id)
        
        #得到这条组合的详细信息，按show_order排序,包括item，item个数等
        item_relation_combination = session.query(ItemRelationCombination).\
    filter(ItemRelationCombination.item_relation_id == item_relation_object.id).\
    order_by(ItemRelationCombination.show_order)
        
        #遍历，因为组合最终是要多选的，所以根据组合多选个数增加前缀，
        for i in xrange(obj.multi_number):
            #此处遍历是遍历组合中的item项
            for item_in_combitition in item_relation_combination:            
                item = session.query(Item).get(item_in_combitition.item_id)
                
                #由于在一个组合里面，item是可以多个的，因此根据item个数，添加item，和最终具体item的显示顺序
                for j in xrange(item_in_combitition.combination_number):
                    detail_object = DescriptionDetailFormInfo(relation_show_order=relation_show_number,
                                                      item_show_order= item_show_number,
                                                      item_id=item.id,
                                                      relation_title=item_relation_object.title,
                                                      item_title=item.title,
                                                      )
                    item_show_number += 1
                    description_detail_info_list.append(detail_object)
            #一组组合结束，组合显示顺序加1
            relation_show_number += 1
    session.close()
    
    initial={"description_detail_info_list":description_detail_info_list,}
        
    if request.method == 'POST':
        form = DescriptionDetailForm(request.POST,initial=initial,auto_id=False)
        if form.is_valid():
            id = form.save(description_type_id = description_type_id)
            if id is not None:
                pass
                #data = {'description_meta_id':description_meta_id,'page':1}
                #return HttpResponseRedirect(reverse('description_type_list', kwargs=data)) 
    else:
        form = DescriptionDetailForm(initial=initial,auto_id=False)
    
    
    data = {'form': form,
            'description_type_id':description_type_id,
            'description_id':description_id,
            
            }
    
    return render_to_response("description/description_detail_add.html", data, context_instance=RequestContext(request)) 
