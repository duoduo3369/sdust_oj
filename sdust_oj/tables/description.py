from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, \
    DateTime, Text
from sqlalchemy.orm import mapper, relationship
from datetime import datetime

from sdust_oj.sa_conn import metadata

item = Table("Item", metadata,
                Column("id", Integer, primary_key=True),
                Column("title", String(200), nullable=False, default=""),
                     
               )

item_relation = Table("ItemRelation", metadata,
                        Column("id", Integer, primary_key=True),
                        Column("title", String(200), nullable=False, default=""),
                
                        )

item_relation_combination = Table("ItemRelationCombination", metadata,
                                  Column("id", Integer, primary_key=True),
                                  Column("item_id", Integer, ForeignKey('Item.id')),
                                  Column("item_relation_id", Integer, ForeignKey('ItemRelation.id')),
                                  Column("combination_number", Integer, nullable=False, default=1),
                                  Column("show_order", Integer, nullable=False, default=1),

               )

description_meta = Table("DescriptionMeta", metadata,
                Column("id", Integer, primary_key=True),
                Column("title", String(200), nullable=False, default=""),
                     
               )

description_meta_item_relation_combination = Table("DescriptionMetaItemRelationCombination", metadata,
                                  Column("id", Integer, primary_key=True),
                                  Column("description_meta_id", Integer, ForeignKey('DescriptionMeta.id')),
                                  Column("item_relation_id", Integer, ForeignKey('ItemRelation.id')),
                                  Column("multi_number", Integer, nullable=False, default=0),
                                  

               )

description_type = Table("DescriptionType", metadata,
                Column("id", Integer, primary_key=True),
                Column("description_meta_id", Integer, ForeignKey('DescriptionMeta.id')),
                Column("title", String(200), nullable=False, default=""),
                     
               )

description_type_item_relation_combination = Table("DescriptionTypeItemRelationCombination", metadata,
                                  Column("id", Integer, primary_key=True),
                                  Column("description_meta_id", Integer, ForeignKey('DescriptionMeta.id')),
                                  Column("item_relation_id", Integer, ForeignKey('ItemRelation.id')),
                                  Column("multi_number", Integer, nullable=False, default=0),
                                  

               )

metadata.create_all()

from sdust_oj.models.description import (Item, ItemRelation, ItemRelationCombination,
                                         DescriptionMeta,DescriptionMetaItemRelationCombination,
                                         DescriptionType,DescriptionTypeItemRelationCombination
                                         )

mapper(Item, item)

mapper(ItemRelation, item_relation)

mapper(ItemRelationCombination, item_relation_combination)

mapper(DescriptionMeta, description_meta)

mapper(DescriptionMetaItemRelationCombination, description_meta_item_relation_combination)

mapper(DescriptionType, description_type)

mapper(DescriptionTypeItemRelationCombination, description_type_item_relation_combination)
