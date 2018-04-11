# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 20:06:22 2018

@author: nandinir940
"""


import json
import pymysql
import collections

rds_host  = 'auroradiaasdb.ciqjohdmf01w.us-east-1.rds.amazonaws.com'
db_name = 'auroradiaasdb'
name = 'diaasmaster'
password = 'dbpwddiaas678'


def getListWorkspaceByUser(event,context):
    try:
        connection = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10);
        cursor = connection.cursor();
        print("Connected");
        user_id=event['user_id'];
        flag=event['flag'];
        objects_list = [];
        
        #workspace details list
        if flag=="1":
            #sql_command='select ID,WORKSPACE_TITLE from docDD_Workspace_Master_Table where ID in (select WORKSPACE_ID from docDD_User_Workspace_Mapping_Table where USER_ID = '+str(user_id)+' )';
            #sql_command ='select * from docDD_User_Workspace_Mapping_Table'
            #cursor.execute(sql_command);
            args = [1];
            cursor.callproc('spWorkSpaceDetails',args);
            connection.commit();
            results=cursor.fetchall();
            for row in results:
                #for row in results:
                d = collections.OrderedDict();
                d['id'] = row[0];
                d['workspaceTile'] = row[1];
                objects_list.append(d); 
        
        #list of workspace details        
        elif flag=="2":
            print("flag:"+flag);
            workspace_id=event['workspace_id'];
            sql_command ='select a.ID, a.DOCUMENT_NAME, b.STATUS_NAME, c.DOCUMENT_TYPE_NAME,d.WORKSPACE_TITLE, a.CREATION_DATETIME from docDD_Document_Master_Table a inner join docDD_Document_Status_Master_Table b on b.id = a.STATUS_ID inner join docDD_Document_Type_Master_Table c on c.id = a.DOCUMENT_TYPE_ID inner join docDD_Workspace_Master_Table d on d.id=a.WORKSPACE_ID where a.WORKSPACE_ID='+str(workspace_id);
            cursor.execute(sql_command);
            connection.commit();
            results=cursor.fetchall();
            for row in results:
                d = collections.OrderedDict();
                d['id'] = row[0];
                d['DOCUMENT_NAME'] = row[1];
                d['STATUS_NAME'] = row[2];
                d['DOCUMENT_TYPE_NAME'] = row[3];
                d['WORKSPACE_TITLE'] = row[4];
                d['CREATION_DATETIME'] = str(row[5]);
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
        return(data);

    except Exception as e:
        raise e;
        