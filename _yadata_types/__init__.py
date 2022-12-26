
from yadata.record import Record,AddManyToMany,AddOneToMany
import unicodedata
import re
from urllib.request import Request,urlopen

try:
    from pybtex.bibtex.names import format as format_name
except ImportError:
    from pybtex.bibtex.names import format_name

w_pattern = re.compile('[\W_]+')

def just_alnum(x):
    return w_pattern.sub('',x)

def clean_string(x):
    try:
        return just_alnum(str(x).lower())
    except:
        print(type(x),x)
        raise

def _exists_and_is_almost_same(d1,d2,fieldname):
    if (fieldname in d1) and \
        (fieldname in d2):
        if d1[fieldname] == d2[fieldname]:
            return True
        l1,l2 = (x[:] if type(x) is list else [x] for x in (d1[fieldname],d2[fieldname]))
        if len(l1) != len(l2):
            return False
        for l in l1,l2:
            for i,x in enumerate(l):
                l[i]=clean_string(x)
        l1.sort()
        l2.sort()
        return l1 == l2
    return False

class Year(Record):

    yadata_tag='!Year'

    def __init__(self,d):

        if 'year' not in d:
            raise ValueError(f'year missing in {d}')
        Record.__init__(self,d)

    def get_key_prefix(self):
        
        return f'{self["year"]}'

    subdir='years'
    
    def __eq__(self,other):
        
        return self['year']==other['year']

class Tag(Record):

    yadata_tag = '!Tag'

    def __init__(self,d):

        if 'tag' not in d:
            raise ValueError(f'tag missing in {d}')
        Record.__init__(self,d)

    def get_key_prefix(self):

        return f'{self["tag"]}'

    subdir='tags'
    
    def __eq__(self,other):
        
        return self['tag']==other['tag']

class Grant(Record):

    yadata_tag='!Grant'

    def __init__(self,d):

        if 'id' not in d:
            raise ValueError(f'id missing in {d}')
        Record.__init__(self,d)

    def get_key_prefix(self):
        
        return f'{self["id"]}'

    subdir='grants'
    
    def __eq__(self,other):
        
        return self['id']==other['id']

    def grantrok(self,rok):

        return GrantRok({'grant':self['_key'],'year':rok,'prijmy':0.0,'vydavky':0.0})

@AddOneToMany(fieldname='grant',inverse_type=Grant,inverse_fieldname='grantyears',inverse_sort_by=('year',))
@AddOneToMany(fieldname='year',inverse_type=Year,inverse_fieldname='grants',forward=False)
class GrantRok(Record):
    
    yadata_tag='!GrantRok'


    def __init__(self,d):

        for key in ('year','grant','prijmy','vydavky'):
            if key not in d:
                raise ValueError(f'{key} missing in {d}')
        Record.__init__(self,d)
    
    def get_key_prefix(self):
        
        return f'{self["grant"]}:{self["year"]}'
    
    @property
    def subdir(self):
        
        return f'grants/{self["grant"]}'
    
    def __eq__(self,other):
        
        return self['year']==other['year'] and \
            self['grant']==other['grant']

class BibRecord(Record):

    top_fields=['authors','title']

    @classmethod
    def is_my_type(cls,d):
        return all(name in d for name in ('authors','title','year'))


    def _same_position(self,other):

        for k1 in ('article-number','art_number','article_number'):
            for k2 in ('article-number','art_number','article_number'):
                if k1 in self and k2 in other and self[k1]==other[k2] and \
                    (_exists_and_is_almost_same(self,other,'volume') \
                        or ('volume' not in self and 'volume' not in other)) and \
                    (_exists_and_is_almost_same(self,other,'number') \
                        or ('number' not in self and 'number' not in other)):
                    return True

        if all(_exists_and_is_almost_same(self,other,key) \
            for key in ('volume','startpage')):
                return True

        return False

    def _same_source(self,other):

        return any(_exists_and_is_almost_same(self,other,key) \
            for key in ('journal','series'))

    def _same_authors(self,other,preprocess=lambda x: x):

        def _surname(author):
            return ''.join(author.split(',')[0].lower().split())

        if 'authors' in self and 'authors' in other:
            if len(self['authors'])!=len(other['authors']):
                return False
            l1=[_surname(preprocess(author)) for author in self['authors']]
            l2=[_surname(preprocess(author)) for author in other['authors']]
            l1.sort()
            l2.sort()
            return l1==l2
        return False

    def __eq__(self,other):

        # if keys are present, it is trivial
        if '_key' in self and '_key' in other:
            return self['_key']==other['_key']
        # a distinct startpage, both greater than 1
        # means no match
        if 'startpage' in self and 'startpage' in other and \
            (type(self['startpage']) is not int or self['startpage']>1) and \
            (type(self['startpage']) is not int or self['startpage']>1) and \
            self['startpage']!=other['startpage']:
            return False

        # distinct length (not too short) means no match
        try:
            self_l=self['endpage']-self['startpage']
            other_l=other['endpage']-other['startpage']
            if self_l>2 and other_l>2 and self_l!=other_l:
                return False
        except:
            # non numeric page numbers
            pass

        if self._same_authors(other) and all(_exists_and_is_almost_same(self,other,key) \
            for key in ('title','year')):
            return True

        same_position=self._same_position(other)

        if same_position and _exists_and_is_almost_same(self,other,'title'):
            return True

        if same_position and self._same_source(other):
            return True

        return False

    def get_key_prefix(self):

        if any(name not in self for name in ('title','year','authors')):
            raise ValueError('Cannot create key without title, year and authors')
        author=''.join(self['authors'][0].split(',')[0].lower().split())
        title=''
        for w in self['title'].split():
            w=just_alnum(w)
            title=title+w.lower()
            if len(title)>=4:
                break
        year='%s' % self['year']
        keyprefix='%s%s%s' % (author,year,title)
        keyprefix=unicodedata.normalize('NFKD',keyprefix).encode('ascii','ignore').decode('ascii')
        return keyprefix

    def authors_format(self,bst_format):

        return [format_name(auth,bst_format).replace('~',' ') for auth in self['authors']]

@AddOneToMany(fieldname='year',inverse_type=Year,inverse_fieldname='myowns',forward=False)
@AddManyToMany(fieldname='grants',inverse_type=Grant,inverse_fieldname='myowns',inverse_sort_by=('year',))
@AddManyToMany(fieldname='tags',inverse_type=Tag,inverse_fieldname='myowns',inverse_sort_by=('year',),forward=False)
class MyOwn(BibRecord):

    yadata_tag='!MyOwn'
    
    @property
    def subdir(self):
        
        return f'myown/{self["year"]}'

@AddOneToMany(fieldname='year',inverse_type=Year,inverse_fieldname='citations',forward=False)
@AddManyToMany(fieldname='cites',inverse_type=MyOwn,inverse_fieldname='citedby',inverse_sort_by=('year',))
@AddManyToMany(fieldname='tags',inverse_type=Tag,inverse_fieldname='citations',inverse_sort_by=('year',),forward=False)
class Citation(BibRecord):

    yadata_tag='!Citation'

    @property
    def subdir(self):
        
        return f'citation/{self["year"]}'

class Review(Record):

    yadata_tag='!Review'
   
    def __init__(self,d):

        for key in ('authors','journal','year','id'):
            if key not in d:
                raise ValueError(f'{key} missing in {d}')
        Record.__init__(self,d)

    def get_key_prefix(self):
        
        jrnl="".join(word[0] for word in self['journal'].strip().split())
        return f'Review:{jrnl}:{self["year"]}:{self["id"]}'
    
    @property
    def subdir(self):
        
        return f'reviews/{self["year"]}'
   
    def __eq__(self,other):
        
        if '_key' in self and '_key' in other:
            return self['_key']==other['_key']
        return self['journal']==other['journal'] and \
            self['year']==other['year'] and \
            self['id']==other['id']

