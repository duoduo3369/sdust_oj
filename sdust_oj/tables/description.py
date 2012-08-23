from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, \
    DateTime, Text
from sqlalchemy.orm import mapper, relationship
from datetime import datetime

from sdust_oj.sa_conn import metadata

item = Table("Item", metadata,
                Column("id", Integer, primary_key=True),
                Column("title", String(200), nullable=False, default=""),
                extend_existing=True     
               )

item_relation = Table("ItemRelation", metadata,
                        Column("id", Integer, primary_key=True),
                        Column("title", String(200), nullable=False, default=""),
                        extend_existing=True
                        )

item_relation_combination = Table("ItemRelationCombination", metadata,
                                  Column("id", Integer, primary_key=True),
                                  Column("item_id", Integer, ForeignKey('Item.id')),
                                  Column("item_relation_id", Integer, ForeignKey('ItemRelation.id')),
                                  Column("combination_number", Integer, nullable=False, default=1),
                                  Column("show_order", Integer, nullable=False, default=1),
                                  extend_existing=True
               )

description_meta = Table("DescriptionMeta", metadata,
                Column("id", Integer, primary_key=True),
                Column("title", String(200), nullable=False, default=""),
                extend_existing=True     
               )

description_meta_item_relation_combination = Table("DescriptionMetaItemRelationCombination", metadata,
                                  Column("id", Integer, primary_key=True),
                                  Column("description_meta_id", Integer, ForeignKey('DescriptionMeta.id')),
                                  Column("item_relation_id", Integer, ForeignKey('ItemRelation.id')),                                 
                                  extend_existing=True
               )

description_type = Table("DescriptionType", metadata,
                Column("id", Integer, primary_key=True),
                Column("description_meta_id", Integer, ForeignKey('DescriptionMeta.id')),
                Column("title", String(200), nullable=False, default=""),
                extend_existing=True  
               )

description_type_item_relation_combination = Table("DescriptionTypeItemRelationCombination", metadata,
                                  Column("id", Integer, primary_key=True),
                                  Column("description_type_id", Integer, ForeignKey('DescriptionType.id')),
                                  Column("item_relation_id", Integer, ForeignKey('ItemRelation.id')),
                                  Column("relation_items_number", Integer,nullable=False, default=1),
                                  Column("multi_number", Integer, nullable=False, default=0),
                                  Column("show_order", Integer, nullable=False, default=1),
                                  extend_existing=True
               )
description_detail = Table("DescriptionDetail", metadata,
                                  Column("id", Integer, primary_key=True),
                                  Column("description_type_id", Integer, ForeignKey('DescriptionType.id')),
                                  Column("description_id", Integer, ForeignKey('Description.id')),
                                  Column("item_relation_id", Integer, ForeignKey('ItemRelation.id')),
                                  Column("items_id", Integer, ForeignKey('Item.id')),
                                  Column("relation_show_order", Integer, nullable=False, default=1),
                                  Column("show_order", Integer, nullable=False, default=1),
                                  Column("content", Text, nullable=False, default=""),
                                  extend_existing=True
               )

metadata.create_all()

from sdust_oj.models.description import (Item, ItemRelation, ItemRelationCombination,
                                         DescriptionMeta,DescriptionMetaItemRelationCombination,
                                         DescriptionType,DescriptionTypeItemRelationCombination,
                                         DescriptionDetail
                                         )

mapper(Item, item)

mapper(ItemRelation, item_relation)

mapper(ItemRelationCombination, item_relation_combination)

mapper(DescriptionMeta, description_meta)

mapper(DescriptionMetaItemRelationCombination, description_meta_item_relation_combination)

mapper(DescriptionType, description_type)

mapper(DescriptionTypeItemRelationCombination, description_type_item_relation_combination)

mapper(DescriptionDetail, description_detail)
