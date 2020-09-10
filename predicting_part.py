import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split,GridSearchCV,StratifiedKFold
from sklearn.preprocessing import LabelEncoder,label
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score,classification_report
import string
import re
import pickle
import config
import time
import en_core_web_sm


def predictionsOnEachTicket(df):

    # df.dropna(inplace=True)
    # df.drop_duplicates(inplace=True)
    
    df2=df.copy()
    try:
        config.logger.info('Removing Contractions from dataframe part 1')
        def removeContractions1(incident):
            words=str(incident).lower().split()
            joined=''
            for word in words:
                uncontracted=config.contractions.get(word)
                if uncontracted:
                    joined=joined+uncontracted+' '
                else:
                    joined=joined+word+' '
            return joined.strip()
        
        df['Description_Uncontracted']=df['Description'].apply(removeContractions1)
    except Exception as e:
        
        config.logger.exception('Error in removing contractions part 1 '+str(e))
    
    def removeContractions2(complaint):
        try:
            config.logger.info('Removing Contractions from dataframe part 2')
            words=complaint.lower()
            words=re.sub("'ll",' will',words)
            words=re.sub("'s",' is',words)
            words=re.sub("'nt",' not',words)
            words=re.sub("'d",' would',words)
            words=re.sub("won\'t", "will not", words)
            words=re.sub("can\'t", "can not", words)
            words=re.sub("n't", " not", words)
            words=re.sub("'re", " are", words)
            words=re.sub("\'s", " is", words)
            words=re.sub("'d", " would", words)
            words=re.sub("'ll", " will", words)
            words=re.sub("'t", " not", words)
            words=re.sub("'ve", " have", words)
            words=re.sub("'m", " am", words)
            return words
        
        except Exception as e:
            
            config.logger.exception('Removing Contractions from dataframe part 2')
            
    df['Description_Uncontracted']=df['Description_Uncontracted'].apply(removeContractions2)
    
    remove_textin_brackets_pattern=r'(\(|{|\[).*?(\)|}|\])'
    
    remove_url_pattern = r'((http|ftp|https):\/\/)?[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    
    remove_html_tags=r'<.*?>'
    
    df['Description_Cleaned']=df['Description_Uncontracted'].apply(lambda x:re.sub(remove_textin_brackets_pattern,'',
                                                                                   str(x)).lower().strip())
    
    df['Description_Cleaned']=df['Description_Cleaned'].apply(lambda x:re.sub(remove_url_pattern,'',str(x)).strip())
    
    df['Description_Cleaned']=df['Description_Cleaned'].replace(remove_html_tags,'',regex=True)
    
    nlp = en_core_web_sm.load()
    stop_words=set(nlp.Defaults.stop_words)
    
    for negate_stop_word in config.negate_stop_words:
        stop_words.discard(negate_stop_word)
        
    stop_words.update(config.stopwords_to_add)
    
    try:
        
        config.logger.info('Lemmatizing tickets')
    
        def lemmatizeword(incident):
            words=nlp(str(incident))
            joined=''
            for word in words: 
                if (word.ent_type_ !='PERSON') and (word.ent_type_ !='DATE') and (word.lemma_ not in stop_words) :
                    joined=joined+word.lemma_+' '
            return joined.strip()  
    
    except Exception as e:
        
        config.logger.exception('Error in lemmatizing tickets '+str(e))
        
    
    df['Description_Lemmatized']=df['Description_Cleaned'].apply(lemmatizeword)
    
    df['Description_Puncatation_Removed']=df['Description_Lemmatized'].replace('[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n\d]+?','')
      
    X=df['Description_Puncatation_Removed']
    
    config.logger.info('Loading Tfidf Vectorizor')
    tfidf = pickle.load(open('tfIdfVectorizer.sav','rb'))
    
    config.logger.info('Loading Xgboost model')
    
    xg= pickle.load(open('xgboost.sav','rb'))
    
    X=tfidf.transform(X)
    
    pred_y=xg.predict(X)
    
    pred_df=pd.DataFrame(pred_y,columns=['predicted_class_num'])
    
    df=pd.concat([df2,pred_df],axis=1)
    
    return df
   