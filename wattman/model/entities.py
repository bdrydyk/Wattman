from elixir import *

class Page(Entity):
    """docstring for Page"""
    title = Field(Unicode(100))
    path = Field(Unicode(100))
    content = Field(UnicodeText)
    created_on = Field(Date)
        
class Author(Entity):
    """docstring for Page"""
    name = Field(Unicode(100))
    email = Field(Unicode(100))
    label = Field(Unicode(100))
        
class Post(Entity):
    """docstring for Page"""
    title = Field(Unicode(100))
    path = Field(Unicode(100))
    content = Field(UnicodeText)
    created_on = Field(Date)
    comments_allowed = Field(Boolean)
    draft = Field(Boolean)
    posted_on = Field(Date)
    comments = OneToMany('Comment')
    tags = ManyToMany('Tag', tablename="page_tag")


class Comment(Entity):
    """docstring for comment"""
    """docstring for Page"""
    name = Field(Unicode(100))
    email = Field(Unicode(100))
    content = Field(UnicodeText)
    created_on = Field(Date)
    approved = Field(Boolean)
    url = Field(Unicode(100))
    post = ManyToOne('Post')
    
  
        

class Tag(Entity):
    """docstring for tag"""
    """docstring for Page"""
    name = Field(Unicode(20), primary_key=True)
    path = Field(Unicode(100))
    posts = ManyToMany('Post', tablename="page_tag")



class Movie(Entity):
    title = Field(String(100))
    description = Field(Text)
    year = Field(Integer)
    genera = Field(String(100))
    release_date = Field(Date)





def now():
    return datetime.datetime.now()