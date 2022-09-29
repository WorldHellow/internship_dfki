import pandas as pd 

def difference(A,B):
    A = set(A.split())
    B = set(B.split())
    
    C = A-B
    #print(C)
    return list(C)


df = pd.read_csv('common_wiki.csv',sep='\t')


x = list(df['text_x'])
y = list(df['text_y'])

diff = list()

for i, j in zip(x,y):
    if isinstance(i,str) and isinstance(j,str):
        diff.append(' '.join(difference(i, j)))
    elif isinstance(i,str) and isinstance(j,float):
        diff.append(' '.join(difference(i,str(j))))
    elif isinstance(i,float) and isinstance(j,str):
        diff.append(' '.join(difference(str(i),j)))
    else:
        diff.append(' '.join(difference(str(i),str(j))))


df['text_diff'] =  diff

df = df.drop(['text_x', 'ns_y', 'revision_id_y', 'author_y', 'author_id_y', 'text_y'], axis=1)

df.to_csv('difference_wikipedia_authors_recent.csv', sep='\t', index=False)

print(df.columns)
