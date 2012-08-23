# coding=UTF8

class Item(object):
    
    def __init__(self,title=""):
        self.title = title
        
class ItemRelation(object):
    
    def __init__(self,title=""):
        self.title = title
        
class ItemRelationCombination(object):

    def __init__(self, item_id=None,item_relation_id=None, 
                 combination_number=1, show_order=1):
        self.item_id = item_id
        self.item_relation_id = item_relation_id        
        self.combination_number = combination_number
        self.show_order = show_order

class ItemRelationViewDetail(object):
    
    def __init__(self,item_id=None,item_title='',combination_number=None, show_order=None):
        """
        在显示组合详情时，因为ItemRelationCombination是用的Item，ItemRelation的两个外键，需要查询两次，
        第一次用ItemRelatio.id,filter的出联系的结果，第二次用这些结果查出具体item的title。
        因为最终显示时需要显示id，title，combination_number，show_order，为了方便操作，添加这个类。
        用在view和template中。
        """
        self.item_id = item_id
        self.item_title = item_title
        self.combination_number = combination_number
        self.show_order = show_order
                
class ItemRelationCombinationFormInfo(object):
    """
    添加组合时，使用了自定义的widget，由于对象的个数是根据查询结果来的，不固定，导致field的名字不固定，
    添加一个类，来是init和save时field的名字统一，同时记录item的id和title，方便操作。
    用在view和form中。
    """
    
    def __init__(self,item_id=None,item_title=''):
        self.item_id = item_id
        self.item_title = item_title
        self.title_field_name = str(item_id) + '_' + item_title

class DescriptionMeta(object):
    
    def __init__(self,title=""):
        self.title = title      

class DescriptionMetaItemRelationCombination(object):

    def __init__(self, description_meta_id=None,item_relation_id=None, 
                 multi_number=None,):
        self.description_meta_id = description_meta_id
        self.item_relation_id = item_relation_id        

class DescriptionMetaItemRelationCombinationFormInfo(object):

    def __init__(self, item_relation_id=None, item_relation_title='',relation_items_number=None):
        self.item_relation_id = item_relation_id
        self.item_relation_title = item_relation_title
        self.title_field_name = str(item_relation_id) + '_' + item_relation_title
        self.relation_items_number = relation_items_number
        
class DescriptionTypeItemRelationViewDetail(object):
    
    def __init__(self,item_relation_id=None,item_relation_title='',multi_number=None, show_order=None):

        self.item_relation_id = item_relation_id
        self.item_relation_title = item_relation_title
        self.multi_number = multi_number
        self.show_order = show_order
        
class DescriptionType(object):
    
    def __init__(self,description_meta_id=None,title=""):
        self.description_meta_id = description_meta_id
        self.title = title 

class DescriptionTypeItemRelationCombination(object):

    def __init__(self, description_type_id=None,item_relation_id=None, 
                 relation_items_number=None,
                 multi_number=None,show_order=None):
        self.description_type_id = description_type_id
        self.item_relation_id = item_relation_id    
        self.relation_items_number = relation_items_number    
        self.multi_number = multi_number
        self.show_order = show_order

class DescriptionDetail(object):
    def __init__(self, description_type_id=None,description_id=None,
                 item_relation_id=None, items_id=None,
                 relation_show_order=None,show_order=None,content=None):
        self.description_type_id = description_type_id
        self.description_id = description_id
        self.item_relation_id = item_relation_id
        self.items_id = items_id
        self.relation_show_order = relation_show_order
        self.show_order = show_order
        self.content = content
  
class DescriptionDetailFormInfo(ItemRelationCombinationFormInfo):
    
    def __init__(self,item_id=None,item_title='',relation_title='',relation_show_order=None,item_show_order=None):
        self.relation_show_order = relation_show_order
        self.item_show_order = item_show_order
        self.item_id = item_id
        self.relation_title = relation_title
        self.item_title = item_title
        self.title_field_name = str(relation_show_order) + '_' + str(item_show_order) + '_' + str(item_id) + '_' + item_title
        