from fuzzylev import *
from pybliometrics.scopus import ScopusSearch, AuthorSearch, AuthorRetrieval

def dattr(obj, attrs = 'parameters'):
    '''function showing list of object's attributes and their values as pandas dataframe'''
    import pandas as pd
    # dataframe of attributes not starting with _
    dobj = pd.DataFrame([attr for attr in dir(obj) if not attr.startswith('_')], columns=['attribute'])
    # values of attributes
    dobj['value'] = dobj['attribute'].apply(lambda x: getattr(obj, x))
    # set column attribute as an index
    dobj.set_index('attribute', inplace=True)
    # dictionary for output accordung to attributes types
    case = {'all':dobj,
            'numerical':dobj[pd.to_numeric(dobj.value, errors='coerce').notnull()],
            'parameters': dobj[~dobj.value.astype(str).str.startswith('<')],
            'methods':dobj[dobj.value.astype(str).str.startswith('<')]}
    return case.get(attrs, 'invalid input')

def ScopusDocQuery(title, authorlastname=''):
    '''Scopus query for searching title and/or author's last name'''
    texttitle = f'TITLE("{title}")'
    if authorlastname!='':
        authorlastname = clean_str(authorlastname, case="lower")
        authorlastnamenounicode = clean_str(authorlastname, case="lower", unicode=False)
        textauthor = f' AND AUTHLASTNAME({authorlastnamenounicode})'# OR AUTHLASTNAME({authorlastnamenounicode})'
    else:
        textauthor = ''
    return texttitle+textauthor

def ScopusAuthQuery(authorfirstname, authorlastname, initial=False):
    '''Scopus query for searching author'''
    lastname = clean_str(authorlastname, case="lower", unicode=False)
    firstname = clean_str(authorfirstname, case="lower", unicode=False)
    nameinitial = firstname[0].lower()
    textquery = {True: f'AUTHLASTNAME("{lastname}") AND AUTHFIRST({nameinitial})',
                 False: f'AUTHLASTNAME("{lastname}") AND AUTHFIRST({firstname})'}
    return textquery[initial]

def ScopusDataShort(author):
    '''Scopus data for a searched author's'''
    data = {'scopus-id':author.identifier, 'first name':author.given_name, 'last name': author.surname,
            'full name': f'{author.given_name} {author.surname}', 'documents': author.document_count, 
            'citations': author.cited_by_count, 'h-index':author.h_index}
    return data

def ScopusDataLong(short, author):
    '''Scopus data for a searched author's'''
    data = {'scopus-id':author.identifier, 'first name':author.given_name, 'last name': author.surname,
            'full name': f'{author.given_name} {author.surname}', 'affiliation': short.affiliation, 
            'location' : f'{short.city}, {short.country}', 'areas':short.areas,
            'documents': author.document_count, 'citations': author.cited_by_count, 'h-index':author.h_index}
    return data