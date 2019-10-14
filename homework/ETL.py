#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 20:37:27 2019

@author: keyvanamini
"""
import pandas as pd
import dataset
import datetime
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres@localhost:5432/ordersdb')

#return Pandas df's from Postgres SQL Query
empl2 = pd.read_sql_query('select * from "employees"',con=engine)
cust2 = pd.read_sql_query('select * from "customers"',con=engine)
ord2 = pd.read_sql_query('select * from "order_details"',con=engine)
prod2 = pd.read_sql_query('select * from "products"',con=engine)
off2 = pd.read_sql_query('select * from "offices"',con=engine) 
prodord = pd.read_sql_query('select * from "products_ordered"',con=engine)

#Creating the joins
join1 = pd.merge(prodord, ord2, how= 'left', on='order_number', sort=False)
join2 = pd.merge(join1, prod2, how='left', on='product_code', sort=False)
join3 = pd.merge(join2, cust2, how='left',on='customer_number', sort=False)
join4 = pd.merge(join3, empl2, how='left', left_on='sales_rep_employee_number', right_on='employee_number', sort=False) 
join5 = pd.merge(join4, off2, how='left',on='office_code', sort=False)

#Creating the measure table
measures = join5[['order_number', 'product_code', 'quantity_ordered', 'price_each', 'order_line_number', 'quantity_in_stock', 'buy_price', '_m_s_r_p', 'order_date', 'customer_number', 'sales_rep_employee_number', 'credit_limit', 'office_code']]
measures['revenue']=measures['quantity_ordered']*measures['price_each']
measures['cost']=measures['quantity_ordered']*measures['buy_price']
measures['profit']=measures['revenue']-measures['cost']
measures['margin']=measures['profit']/measures['cost']
measures['order_date'] = pd.to_datetime(measures['order_date'])

#Creating additional dimension order_date_time incl. quarter
dto = ord2[['order_date']]
dto['order_date'] = pd.to_datetime(dto['order_date'])
L = ['year', 'month', 'day']
dto = dto.join(pd.concat([getattr(dto['order_date'].dt, i).rename(i) for i in L], axis=1))
dto = dto.drop_duplicates()
dto['quarter']= pd.to_datetime(dto.order_date).dt.quarter


#Uploading data to new database snowdb
db2 = dataset.connect('postgresql://postgres@localhost:5432/snowdb')

off3 = db2['offices']
empl3 = db2['employees']
cust3 = db2['customers']
ord3 = db2['orders']
prod3 = db2['products']
prodord2 = db2['products_ordered']
mea = db2['measures']
dto2 = db2['order_date_time']


off3.insert_many(off2.to_dict('records'))
empl3.insert_many(empl2.to_dict('records'))
cust3.insert_many(cust2.to_dict('records'))
ord3.insert_many(ord2.to_dict('records'))
prod3.insert_many(prod2.to_dict('records'))
prodord2.insert_many(prodord.to_dict('records'))
dto2.insert_many(dto.to_dict('records'))
mea.insert_many(measures.to_dict('records'))

#use disconnect