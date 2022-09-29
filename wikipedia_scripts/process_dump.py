#!/usr/bin/env python
# coding: utf-8

# In[54]:


import pandas as pd
import xml.etree.ElementTree as ET


# In[2]:


def strip_tag_name(t):
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t


def parse_wiki(filename):
    events = ("start", "end")
    list_of_tup = list()

    for event, elem in ET.iterparse(filename, events=events):
        tname = strip_tag_name(elem.tag)
        
        if event == 'start':
            if tname == 'page':
                flag_revision = False
                flag_contributor = False
                title = ''
                title_id = ''
                ns = ''
                revision = ''
                author = ''
                author_id = ''
                timestamp = ''
                text = ''
            
            elif tname == 'title':
                title = elem.text
            
            elif tname == 'ns':
                ns = elem.text
                
            elif tname == 'id' and flag_revision==False and flag_contributor==False:
                title_id = elem.text
            
            elif tname == 'id' and flag_revision == True and flag_contributor==False:
                revision = elem.text
                flag_revision = False
                
            
            elif tname == 'id' and flag_contributor == True and flag_revision==False:
                author_id = elem.text
            
            elif tname == 'revision':
                flag_revision = True
            
            elif tname =='contributor':
                flag_contributor = True
            
            elif tname == 'timestamp':
                timestamp = elem.text
            
            elif tname == 'contributor':
                flag_revision = True
            
            elif tname == 'username':
                author = elem.text
            
            
            elif tname == 'text':
                text = elem.text
                
        if event == 'end':
            if tname == 'page':
                list_of_tup.append((title, title_id, ns, revision, author, author_id, text))
        
        elem.clear()
        
        
    return list_of_tup           
            
            


# In[98]:

files = ['eswiki-20220601-pages-articles-multistream.xml', 'eswiki-20220901-pages-articles-multistream.xml']
tup = parse_wiki(files[1])
print('Done with parsing wikipedia file.')
df = pd.DataFrame(tup, columns =['title', 'title_ID', 'ns','revision_id','author','author_id','text'])
print('Done with building dataframe')

df1 = df.loc[df['ns'] == '0']

print('Done with remove irrelevant namespaces.')

# In[101]:
print('Writing to csv file...')

df1.to_csv('recent_wiki.csv', sep='\t', index=False)
print('Done writing to csv file')
