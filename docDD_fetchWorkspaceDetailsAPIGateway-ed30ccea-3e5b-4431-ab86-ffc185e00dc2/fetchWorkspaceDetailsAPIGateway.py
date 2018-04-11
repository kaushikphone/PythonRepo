# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 20:06:22 2018

"""


import json
import pymysql
import collections

rds_host  = 'auroradiaasdb.ciqjohdmf01w.us-east-1.rds.amazonaws.com'
db_name = 'auroradiaasdb'
name = 'diaasmaster'
password = 'dbpwddiaas678'


def getListWorkspaceByUser(event,context):
    connection = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10);
    cursor = connection.cursor();
     
    print("Connected");
     
    user_id=event['user_id'];
     
    objects_list = [];
     
    sql_command='select ID,WORKSPACE_TITLE from docDD_Workspace_Master_Table where ID in (select WORKSPACE_ID from docDD_User_Workspace_Mapping_Table where USER_ID = '+str(user_id)+' )';
    #sql_command ='select * from docDD_User_Workspace_Mapping_Table'
    cursor.execute(sql_command);
    connection.commit();
     
    results=cursor.fetchall();

    for row in results:
        d = collections.OrderedDict();
        d['id'] = row[0];
        d['workspaceTile'] = row[1];
    
        objects_list.append(d);            
    
    cursor.close();
    connection.close();
    data=objects_list;
         
    #return ({
    #    #'isBase64Encoded':False,
    #    'statusCode':200,
    #    'headers':{'Content-Type':'application/json','Access-Control-Allow-Origin': '*' },
    #    'body':json.dumps(data)
    #});
    return (data)