import tw.forms as twf
from tw.forms.validators import UnicodeString, Email, URL, Int, Number, Set, String, OneOf
from tw.forms.validators import NotEmpty, MaxLength, MinLength, Regex, PlainText, StringBool
from tw.forms.validators import DateValidator, DateConverter, TimeConverter, Invalid
import wattman.lib.helpers as h
#from formencode import Schema, NoDefault
from tw.forms.validators import Schema, NoDefault, FancyValidator, ForEach
import re
from wattman.model import *
from pylons import request

class UniquePath(FancyValidator):
    messages = {
        'invalid': 'Path must be unique'
    }
    def _to_python(self, value, state):
        # Ensure we have a valid string
        value = UnicodeString(max=30).to_python(value, state)
        # validate that path only contains letters, numbers, and dashes
        result = re.compile("[^\w-]").search(value)
        if result:
            raise Invalid("Path can only contain letters, numbers, and dashes", value, state)
        
        # Ensure path is unique
        page_q = Session.query(model.Page).filter_by(path=value)
        if request.urlvars['action'] == 'save':
            # we're editing an existing post.
            page_q = page_q.filter(model.Page.id != int(request.urlvars['id']))
            
        # Check if the path exists
        path = page_q.first()
        if path is not None:
            raise Invalid(
                self.message('invalid', state),
                value, state)
        
        return value


#TAG##
class ConstructPath(FancyValidator):
    def _to_python(self, value, state):
        if value['path'] in ['', u'', None]:
            tag_name = value['name'].lower()
            value['path'] = re.compile(r'[^\w-]+', re.U).sub('-', tag_name).strip('-')
        return value


class UniqueName(FancyValidator):
    messages = {
        'invalid': 'Tag name must be unique'
    }
    def _to_python(self, value, state):
        # Ensure we have a valid string
        value = UnicodeString(max=30).to_python(value, state)
        # validate that tag only contains letters, numbers, and spaces
        result = re.compile("[^a-zA-Z0-9 ]").search(value)
        if result:
            raise Invalid("Tag name can only contain letters, numbers, and spaces", value, state)
        
        # Ensure tag name is unique
        tag_q = Session.query(model.Tag).filter_by(name=value)
        if request.urlvars['action'] == 'save':
            # we're editing an existing tag
            tag_q = tag_q.filter(model.Tag.id != int(request.urlvars['id']))
            
        # Check if the tag name exists
        name = tag_q.first()
        if name is not None:
            raise Invalid(
                self.message('invalid', state),
                value, state)
        
        return value
    
class UniquePath(FancyValidator):
    messages = {
        'invalid': 'Tag path must be unique'
    }
    def _to_python(self, value, state):
        # Ensure we have a valid string
        value = UnicodeString(max=30).to_python(value, state)
        # validate that path only contains letters, numbers, and dashes
        result = re.compile("[^\w-]").search(value)
        if result:
            raise Invalid("Path can only contain letters, numbers, and dashes", value, state)
        
        # Ensure tag path is unique
        tag_q = Session.query(Tag).filter_by(path=value)
        if request.urlvars['action'] == 'save':
            # we're editing an existing post.
            tag_q = tag_q.filter(Tag.id != int(request.urlvars['id']))
            
        # Check if the path exists
        path = tag_q.first()
        if path is not None:
            raise Invalid(
                self.message('invalid', state),
                value, state)
        
        return value


####Comments

class AkismetSpamCheck(FancyValidator):
    messages = {
        'invalid-akismet': 'Your comment has been identified as spam.  Are you a spammer?'
    }
    def _to_python(self, values, state):
        # we're in the administrator
        if request.urlvars['action'] == 'save':
            return values
        
        if h.wurdig_use_akismet():
            from wurdig.lib.akismet import Akismet
            # Thanks for the help from http://soyrex.com/blog/akismet-django-stop-comment-spam/
            a = Akismet(h.wurdig_get_akismet_key(), wurdig_url=request.server_name)
            akismet_data = {}
            akismet_data['user_ip'] = request.remote_addr
            akismet_data['user_agent'] = request.user_agent
            akismet_data['comment_author'] = values['name']
            akismet_data['comment_author_email'] = values['email']
            akismet_data['comment_author_url'] = values['url']
            akismet_data['comment_type'] = 'comment'
            spam = a.comment_check(values['content'], akismet_data)
            if spam:
                raise Invalid(
                    self.message('invalid-akismet', state),
                    values, state
                )
        return values
    
class PrimitiveSpamCheck(FancyValidator):
    def _to_python(self, value, state):        
        # Ensure we have a valid string
        value = UnicodeString(max=10).to_python(value, state)
        eq = h.wurdig_spamword().lower() == value.lower()
        if not eq:
            raise Invalid("Double check your answer to the spam prevention question and resubmit.", value, state)
        return value



class NewPageForm(Schema):
    #    pre_validators = [ConstructPath(), Cleanup()]
    allow_extra_fields = True
    filter_extra_fields = True
    title = UnicodeString(
        not_empty=True,
        max=100, 
        messages={'empty':'Enter a page title'},
        strip=True
    )
    path = UniquePath(not_empty=True, max=100, strip=True)
    content = UnicodeString(
        not_empty=True,
        messages={'empty':'Enter some post content.'},
        strip=True)

page_form = twf.TableForm('page_form', action='save', validator = NewPageForm, children=[
    twf.HiddenField('id'),
    twf.TextField('title'),
    twf.TextField('path'),
    #twf.TextField('tags'),
    #twf.Spacer(),
    #twf.TextField('year', size=4, label_text='Year of Fuck'),
    #twf.CalendarDatePicker('release_date'),
    #twf.Label(text='Hello', suppress_label=True),
    #twf.CheckBox('draft'),
    twf.TextArea('content'),

])
        
class NewPostForm(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    title = UnicodeString(
        not_empty=True,
        max=100, 
        messages={'empty':'Enter a post title'},
        strip=True)
    path = UniquePath(not_empty=True, max=100, strip=True)
    content = UnicodeString(
        not_empty=True,
        messages={'empty':'Enter some post content.'},
        strip=True)
    draft = StringBool(if_missing=False)
    comments_allowed = StringBool(if_missing=False)
    #tags = ForEach(Int())
    #chained_validators = [ValidTags()]
post_form = twf.TableForm('page_form', action='save', validator = NewPostForm, children=[
    twf.HiddenField('id'),
    twf.TextField('title'),
    twf.TextField('path'),
    twf.TextField('tags'),
    #twf.Spacer(),
    #twf.TextField('year', size=4, label_text='Year of Fuck'),
    #twf.CalendarDatePicker('release_date'),
    #twf.Label(text='Hello', suppress_label=True),
    twf.CheckBox('draft'),
    twf.TextArea('content'),

])
    
class NewTagForm(Schema):
    pre_validators = [ConstructPath()]
    allow_extra_fields = True
    filter_extra_fields = True
    name = UniqueName(not_empty=True, max=30, strip=True)
    path = UniquePath(not_empty=True, max=30, strip=True)
    
    
tag_form = twf.TableForm('page_form', action='save', validator = NewTagForm, children=[
    twf.HiddenField('id'),
    twf.TextField('name'),
    twf.Spacer(),
    twf.TextField('path', size=4, label_text='Year of Fuck')
])
    
class NewCommentForm(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    name = UnicodeString(not_empty=True, max=100, strip=True)
    email = Email(not_empty=True, max=50, strip=True)
    url = URL(not_empty=False, check_exists=True, max=125, strip=True)
    content = UnicodeString(
        not_empty=True,
        strip=True,
        messages={'empty':'Please enter a comment.'})
    approved = StringBool(if_missing=False)
    if not h.auth.authorized(h.auth.is_valid_user):
        if h.wurdig_use_akismet():
            chained_validators = [AkismetSpamCheck()]
        else:
            wurdig_comment_question = PrimitiveSpamCheck(not_empty=True, max=10, strip=True)
            
comment_form = twf.TableForm('page_form', action='save', validator = NewCommentForm, children=[
    twf.HiddenField('id'),
    twf.TextField('name'),
    twf.TextField('email'),
    twf.TextField('url'),
    twf.Spacer(),
    twf.TextArea('content'),])



#${post_form(action=h.url_for(controller='tutorial', action='save'))}

