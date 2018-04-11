
import json
import pymysql
import collections
import datetime
from datetime import datetime

rds_host  = 'auroradiaasdb.ciqjohdmf01w.us-east-1.rds.amazonaws.com'
db_name = 'auroradiaasdb'
name = 'diaasmaster'
password = 'dbpwddiaas678'


def testFunction(event,context):
    
 connection = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10);
 cursor = connection.cursor();
 
 print("Connected");
 print('event:',event);
 
 objects_list = [];
 object_list_op_5=[];
 
 if (event['option']=="1"):
     #sql_command='describe docDD_Document_Page_Text_Table';
     
     sql_command='select b.CATEGORY,b.count_KEYWORD,d.AVG_SCORE from (select CATEGORY,KEYWORD,count(KEYWORD) as count_KEYWORD from (select distinct docDD_Sentence_Scores_Table.CATEGORY,docDD_Sentence_Scores_Table.KEYWORD from docDD_Sentence_Scores_Table inner join docDD_Page_Sentence_Text_Details_Table on docDD_Page_Sentence_Text_Details_Table.ID=docDD_Sentence_Scores_Table.DOC_PAGE_SENTENCE_ID inner join docDD_Document_Page_Text_Table on docDD_Document_Page_Text_Table.ID=docDD_Page_Sentence_Text_Details_Table.DOCUMENT_PAGE_ID inner join docDD_Document_Master_Table on docDD_Document_Master_Table.ID=docDD_Document_Page_Text_Table.DOCUMENT_ID where docDD_Document_Master_Table.ID= '+str(event['document_id'])+' ) a  group by CATEGORY)b inner join (select CATEGORY,avg(SCORE) as AVG_SCORE from (select  docDD_Sentence_Scores_Table.CATEGORY,docDD_Sentence_Scores_Table.SCORE from docDD_Sentence_Scores_Table inner join docDD_Page_Sentence_Text_Details_Table on docDD_Page_Sentence_Text_Details_Table.ID=docDD_Sentence_Scores_Table.DOC_PAGE_SENTENCE_ID inner join docDD_Document_Page_Text_Table on docDD_Document_Page_Text_Table.ID=docDD_Page_Sentence_Text_Details_Table.DOCUMENT_PAGE_ID inner join docDD_Document_Master_Table on docDD_Document_Master_Table.ID=docDD_Document_Page_Text_Table.DOCUMENT_ID where docDD_Document_Master_Table.ID= '+str(event['document_id'])+' ) c  group by CATEGORY) d on b.CATEGORY=d.CATEGORY';
    
     cursor.execute(sql_command);
     connection.commit();
     
     results=cursor.fetchall();
     for row in results:
        print(row);
        
     for row in results:
        d = collections.OrderedDict();
        d['category'] = row[0];
        d['count'] = row[1];
        d['avg_score']=str(round(row[2],2) if row[2]!=None else 0.00) ;
        
        objects_list.append(d);
        
 elif (event['option']=="2"):
     category_name=event['category'];
     
     sql_command='select SENTENCE_TEXT,KEYWORD,SCORE as cnt from docDD_Page_Sentence_Text_Details_Table  inner join docDD_Sentence_Scores_Table on docDD_Sentence_Scores_Table.DOC_PAGE_SENTENCE_ID=docDD_Page_Sentence_Text_Details_Table.ID inner join docDD_Document_Page_Text_Table on docDD_Document_Page_Text_Table.ID=docDD_Page_Sentence_Text_Details_Table.DOCUMENT_PAGE_ID inner join docDD_Document_Master_Table on docDD_Document_Master_Table.ID=docDD_Document_Page_Text_Table.DOCUMENT_ID where docDD_Document_Master_Table.ID= '+str(event['document_id'])+' and docDD_Sentence_Scores_Table.CATEGORY='+'"'+str(category_name)+'" order by docDD_Sentence_Scores_Table.KEYWORD asc,SCORE desc ';
     
     cursor.execute(sql_command);
     connection.commit();
     
     results=cursor.fetchall();
     for row in results:
        print(row);
        
     for row in results:
        d = collections.OrderedDict();
        d['sentence_text'] = row[0];
        d['keyword'] = row[1];
        d['score'] = str(round(row[2],2) if row[2]!=None else 0.00) ;
        #d['count_KEYWORD'] = row[3];
        objects_list.append(d);
        
 elif (event['option']=="3"):
     
     #sql_command='select ID,document_name from docDD_Document_Master_Table order by docDD_Document_Master_Table.ID desc ;'

     print('select docDD_Document_Master_Table.ID,avg(docDD_Sentence_Scores_Table.SCORE) from docDD_Sentence_Scores_Table  inner join docDD_Page_Sentence_Text_Details_Table on docDD_Sentence_Scores_Table.DOC_PAGE_SENTENCE_ID=docDD_Page_Sentence_Text_Details_Table.ID inner join docDD_Document_Page_Text_Table on docDD_Document_Page_Text_Table.ID=docDD_Page_Sentence_Text_Details_Table.DOCUMENT_PAGE_ID right join docDD_Document_Master_Table on docDD_Document_Master_Table.ID=docDD_Document_Page_Text_Table.DOCUMENT_ID group by docDD_Document_Master_Table.ID');
     sql_command='select a.*,docDD_Document_Master_Table.document_name,docDD_Document_Master_Table.CREATION_DATETIME from (select docDD_Document_Master_Table.ID,avg(docDD_Sentence_Scores_Table.SCORE) as AVG_DOC_SCORE from docDD_Sentence_Scores_Table  inner join docDD_Page_Sentence_Text_Details_Table on docDD_Sentence_Scores_Table.DOC_PAGE_SENTENCE_ID=docDD_Page_Sentence_Text_Details_Table.ID inner join docDD_Document_Page_Text_Table on docDD_Document_Page_Text_Table.ID=docDD_Page_Sentence_Text_Details_Table.DOCUMENT_PAGE_ID right join docDD_Document_Master_Table on docDD_Document_Master_Table.ID=docDD_Document_Page_Text_Table.DOCUMENT_ID group by docDD_Document_Master_Table.ID) a inner join docDD_Document_Master_Table on  a.ID=docDD_Document_Master_Table.ID order by a.ID desc '
     cursor.execute(sql_command);
     connection.commit();
     
     results=cursor.fetchall();
     for row in results:
        print(row);
        
     for row in results:
        print(row);
        
        d = collections.OrderedDict();
        
        d['doc_id'] = row[0];
        d['avg_doc_score']=str(round(row[1],2) if row[1]!=None else-1);
        d['document_name'] = row[2];
        d['uploadedDateTime']=str(row[3]);
        
        #d['document_name'] = row[1].split("/")[len(row[1].split("/"))-1];
        
        objects_list.append(d);
        
 elif (event['option']=="4"):
     
     sql_command='select  avg(AVG_SCORE) from (select AVG_SCORE  from (select b.CATEGORY,d.AVG_SCORE from (select CATEGORY,KEYWORD,count(KEYWORD) as count_KEYWORD from (select distinct docDD_Sentence_Scores_Table.CATEGORY,docDD_Sentence_Scores_Table.KEYWORD from docDD_Sentence_Scores_Table inner join docDD_Page_Sentence_Text_Details_Table on docDD_Page_Sentence_Text_Details_Table.ID=docDD_Sentence_Scores_Table.DOC_PAGE_SENTENCE_ID inner join docDD_Document_Page_Text_Table on docDD_Document_Page_Text_Table.ID=docDD_Page_Sentence_Text_Details_Table.DOCUMENT_PAGE_ID inner join docDD_Document_Master_Table on docDD_Document_Master_Table.ID=docDD_Document_Page_Text_Table.DOCUMENT_ID where docDD_Document_Master_Table.ID= '+str(event['document_id'])+' ) a  group by CATEGORY)b inner join (select CATEGORY,avg(SCORE) as AVG_SCORE from (select  docDD_Sentence_Scores_Table.CATEGORY,docDD_Sentence_Scores_Table.SCORE from docDD_Sentence_Scores_Table inner join docDD_Page_Sentence_Text_Details_Table on docDD_Page_Sentence_Text_Details_Table.ID=docDD_Sentence_Scores_Table.DOC_PAGE_SENTENCE_ID inner join docDD_Document_Page_Text_Table on docDD_Document_Page_Text_Table.ID=docDD_Page_Sentence_Text_Details_Table.DOCUMENT_PAGE_ID inner join docDD_Document_Master_Table on docDD_Document_Master_Table.ID=docDD_Document_Page_Text_Table.DOCUMENT_ID where docDD_Document_Master_Table.ID= '+str(event['document_id'])+' ) c  group by CATEGORY) d on b.CATEGORY=d.CATEGORY)e )f';
     cursor.execute(sql_command);
     connection.commit();
     
     results=cursor.fetchone();
     
     for row in results:
        print(row);
        
     for row in results:
        d = collections.OrderedDict();
        
        d['doc_avg_score'] = str(round(row,2) if row!=None else -1) ;
        
        objects_list.append(d);
        
 elif (event['option']=="5"):
     
     sql_command='select b.CATEGORY,b.count_KEYWORD,d.AVG_SCORE from (select CATEGORY,KEYWORD,count(KEYWORD) as count_KEYWORD from (select distinct docDD_Sentence_Scores_Table.CATEGORY,docDD_Sentence_Scores_Table.KEYWORD from docDD_Sentence_Scores_Table inner join docDD_Page_Sentence_Text_Details_Table on docDD_Page_Sentence_Text_Details_Table.ID=docDD_Sentence_Scores_Table.DOC_PAGE_SENTENCE_ID inner join docDD_Document_Page_Text_Table on docDD_Document_Page_Text_Table.ID=docDD_Page_Sentence_Text_Details_Table.DOCUMENT_PAGE_ID inner join docDD_Document_Master_Table on docDD_Document_Master_Table.ID=docDD_Document_Page_Text_Table.DOCUMENT_ID where docDD_Document_Master_Table.ID= '+str(event['document_id'])+' ) a  group by CATEGORY)b inner join (select CATEGORY,avg(SCORE) as AVG_SCORE from (select  docDD_Sentence_Scores_Table.CATEGORY,docDD_Sentence_Scores_Table.SCORE from docDD_Sentence_Scores_Table inner join docDD_Page_Sentence_Text_Details_Table on docDD_Page_Sentence_Text_Details_Table.ID=docDD_Sentence_Scores_Table.DOC_PAGE_SENTENCE_ID inner join docDD_Document_Page_Text_Table on docDD_Document_Page_Text_Table.ID=docDD_Page_Sentence_Text_Details_Table.DOCUMENT_PAGE_ID inner join docDD_Document_Master_Table on docDD_Document_Master_Table.ID=docDD_Document_Page_Text_Table.DOCUMENT_ID where docDD_Document_Master_Table.ID= '+str(event['document_id'])+' ) c  group by CATEGORY) d on b.CATEGORY=d.CATEGORY';
    
     cursor.execute(sql_command);
     connection.commit();
     
     results=cursor.fetchall();
     for row in results:
        print(row);
        
     for row in results:
        d = collections.OrderedDict();
        d['category'] = row[0];
        d['count'] = row[1];
        d['avg_score']=str(round(row[2],2) if row[2]!=None else 0.00) ;
        objects_list.append(d);
       
     object_list_op_5.append(objects_list) 
       
     sql_command='select  avg(AVG_SCORE) from (select AVG_SCORE  from (select b.CATEGORY,d.AVG_SCORE from (select CATEGORY,KEYWORD,count(KEYWORD) as count_KEYWORD from (select distinct docDD_Sentence_Scores_Table.CATEGORY,docDD_Sentence_Scores_Table.KEYWORD from docDD_Sentence_Scores_Table inner join docDD_Page_Sentence_Text_Details_Table on docDD_Page_Sentence_Text_Details_Table.ID=docDD_Sentence_Scores_Table.DOC_PAGE_SENTENCE_ID inner join docDD_Document_Page_Text_Table on docDD_Document_Page_Text_Table.ID=docDD_Page_Sentence_Text_Details_Table.DOCUMENT_PAGE_ID inner join docDD_Document_Master_Table on docDD_Document_Master_Table.ID=docDD_Document_Page_Text_Table.DOCUMENT_ID where docDD_Document_Master_Table.ID= '+str(event['document_id'])+' ) a  group by CATEGORY)b inner join (select CATEGORY,avg(SCORE) as AVG_SCORE from (select  docDD_Sentence_Scores_Table.CATEGORY,docDD_Sentence_Scores_Table.SCORE from docDD_Sentence_Scores_Table inner join docDD_Page_Sentence_Text_Details_Table on docDD_Page_Sentence_Text_Details_Table.ID=docDD_Sentence_Scores_Table.DOC_PAGE_SENTENCE_ID inner join docDD_Document_Page_Text_Table on docDD_Document_Page_Text_Table.ID=docDD_Page_Sentence_Text_Details_Table.DOCUMENT_PAGE_ID inner join docDD_Document_Master_Table on docDD_Document_Master_Table.ID=docDD_Document_Page_Text_Table.DOCUMENT_ID where docDD_Document_Master_Table.ID= '+str(event['document_id'])+' ) c  group by CATEGORY) d on b.CATEGORY=d.CATEGORY)e )f';
     cursor.execute(sql_command);
     connection.commit();
     
     results=cursor.fetchone();
     
     for row in results:
        print(row);
     
     d1=[] ;  
     for row in results:
        d1 = collections.OrderedDict();
        d1['doc_avg_score'] = str(round(row,2) if row!=None else -1) ;
        
     object_list_op_5.append(d1);
     
 elif (event['option']=="6"):
     
     sql_command='select docDD_User_Clause_Comments_Mapping_Table.USER_COMMENTS,docDD_User_Clause_Comments_Mapping_Table.CREATION_DATETIME from  docDD_User_Clause_Comments_Mapping_Table inner join docDD_Page_Sentence_Text_Details_Table on docDD_Page_Sentence_Text_Details_Table.ID=docDD_User_Clause_Comments_Mapping_Table.CLAUSE_ID inner join docDD_Document_Page_Text_Table on docDD_Document_Page_Text_Table.ID=docDD_Page_Sentence_Text_Details_Table.DOCUMENT_PAGE_ID inner join docDD_Document_Master_Table on docDD_Document_Master_Table.ID=docDD_Document_Page_Text_Table.DOCUMENT_ID where docDD_Document_Master_Table.ID='+str(event["document_id"]);
     cursor.execute(sql_command);
     connection.commit();
     
     results=cursor.fetchall();
     for row in results:
        print(row);
        
     for row in results:
        d = collections.OrderedDict();
        d['user_comments'] = row[0];
        d['comments_datetime'] = str(row[1]);
        objects_list.append(d);
 
 elif (event['option']=="7"):
     
     sql_command='INSERT INTO docDD_User_Clause_Comments_Mapping_Table (CLAUSE_ID,USER_ID,USER_COMMENTS,STATUS_ID,CREATED_BY_USER_ID,CREATION_DATETIME) VALUES(%s,%s,%s,%s,%s,%s)';
     cursor.execute(sql_command,(int(event["clause_id"]),int(event["user_id"]),str(event["user_comments"]),1,int(event["user_id"]),datetime.now()));
     connection.commit();
      
 else:
     print('none');
     
 cursor.close();
 connection.close();

 data={}
 
 if(event['option']=="5"):
  data['data']=object_list_op_5;
 else:
  data['data']=objects_list;
 
 #return ({'isBase64Encoded':False,'statusCode':200,'headers':{'Content-Type':'application/json','Access-Control-Allow-Origin': '*' },'body':json.dumps(data)});
 return (data)
     
     
     