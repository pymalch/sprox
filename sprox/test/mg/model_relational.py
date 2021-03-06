
#
# This schema is adapted from turbogear's default template.
# The implementation retains the original relational style,
# i.e. the collections are flat files
#

from ming import Document, Field, schema as S, Session
from ming.orm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.orm.ormsession import ThreadLocalORMSession
from ming.orm.declarative import MappedClass
from datetime import datetime, timedelta
from decimal import Decimal
from ming.orm.property import ORMProperty, LazyProperty, OneToManyJoin

try:
    from ming.orm.mapper import Mapper
except:
    from ming.odm.mapper import Mapper

#Took from turbogears-ming package to test many-to-many relationships
#on turbogears2 with ming backend.
class ProgrammaticRelationProperty(RelationProperty):
    include_in_repr = False

    def __init__(self, related, getter, setter=None, relation_field=None):
        super(ProgrammaticRelationProperty, self).__init__(related)
        self.relation_field = relation_field
        self.getter = getter
        self.setter = setter

    def __get__(self, instance, cls=None):
        if not instance:
            return self
        return self.getter(instance)

    def __set__(self, instance, value):
        if not self.setter:
            raise TypeError('read-only property')
        else:
            self.setter(instance, value)

    @LazyProperty
    def join(self):
        return OneToManyJoin(self.mapper.mapped_class, self.related, self.relation_field)

class SproxTestClass(MappedClass):
    class __mongometa__:
        session = ThreadLocalORMSession(Session.by_name('sprox_tests'))

# auth model

class GroupPermission(SproxTestClass):
    """This is the association table for the many-to-many relationship between
    groups and permissions.
    """
    class __mongometa__:
        name = 'tg_group_permission_rs'
        unique_indexes = (
          ('group_id', 'permission_id'),
        )
    
    _id = FieldProperty(S.ObjectId)
    group_id = ForeignIdProperty("Group")
    group = RelationProperty("Group")
    permission_id = ForeignIdProperty("Permission")
    permission = RelationProperty("Permission")


class Group(SproxTestClass):
    """An ultra-simple group definition. (Relational-style)
    """
    class __mongometa__:
        name = 'tg_group_rs'
        unique_indexes = [
          ('group_name',)
        ]

    _id = FieldProperty(S.ObjectId)
    group_name = FieldProperty(str)		# unique
    display_name = FieldProperty(str)
    created = FieldProperty(datetime, if_missing=datetime.now)
    
    users = RelationProperty('User')


class Town(SproxTestClass):
    class __mongometa__:
        name = 'town_rs'
    
    _id = FieldProperty(S.ObjectId)
    name = FieldProperty(str)

    users = RelationProperty('User')

class User(SproxTestClass):
    """Reasonably basic User definition. Probably would want additional
    attributes. (Relational-style)
    """
    class __mongometa__:
        name = 'tg_user_rs'
        unique_indexes = [
          ('user_name',),
          ('email_address',)
        ]
        
    _id = FieldProperty(S.ObjectId)
    user_name = FieldProperty(str)		# unique 1
    email_address = FieldProperty(str)		# unique 2
    display_name = FieldProperty(str)
    display_name.sprox_meta = {'title': True}
    
    _password = FieldProperty(str)
    _password.sprox_meta = {'password': True}
    
    created = FieldProperty(datetime, if_missing=datetime.now)
    town_id = ForeignIdProperty(Town)
    town = RelationProperty(Town)

    groups = RelationProperty(Group)
    _groups = ForeignIdProperty(Group, uselist=True)
    
    @property
    def permissions(self):
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

    @classmethod
    def by_email_address(cls, email):
        """A class method that can be used to search users
        based on their email addresses since it is unique.
        """
        raise NotImplementedError

    @classmethod
    def by_user_name(cls, username):
        """A class method that permits to search users
        based on their user_name attribute.
        """
        raise NotImplementedError


    def _set_password(self, password):
        """encrypts password on the fly using the encryption
        algo defined in the configuration
        """
        #unfortunately, this causes coverage not to work
        #self._password = self._encrypt_password(algorithm, password)

    def _get_password(self):
        """returns password
        """
        return self._password

    password = property(_get_password, _set_password)


class Permission(SproxTestClass):
    class __mongometa__:
        name = 'tg_permission_rs'
        unique_indexes = (
            ('permission_name',),
        )
        
    _id = FieldProperty(S.ObjectId)
    permission_name = FieldProperty(str)	# unique
    description = FieldProperty(str)
    groups = RelationProperty(GroupPermission)
    

class Example(SproxTestClass):
    class __mongometa__:
        name = 'example_rs'

    _id = FieldProperty(S.ObjectId)
    created = FieldProperty(datetime, if_missing=datetime.now)
    blob = FieldProperty(S.Binary)		# XXX BLOB?
    binary = FieldProperty(S.Binary)
    boolean = FieldProperty(bool)
    char = FieldProperty(str)
    cLOB = FieldProperty(str)			# XXX CLOB?
    date_ = FieldProperty(datetime)		# XXX date?
    datetime_ = FieldProperty(datetime)
    decimal = FieldProperty(Decimal)
    date = FieldProperty(datetime)		# XXX date?
    datetime = FieldProperty(datetime)
    float__ = FieldProperty(float)
    float_ = FieldProperty(float)
    int_ = FieldProperty(int)
    integer = FieldProperty(int, if_missing=10)
    interval = FieldProperty(timedelta)
    numeric = FieldProperty(Decimal)
    pickletype = FieldProperty(str)		# XXX pickle
    smallint = FieldProperty(int)
    smalliunteger = FieldProperty(int)
    string = FieldProperty(str)
    text = FieldProperty(str)
    time_ = FieldProperty(datetime)		# XXX time
    timestamp = FieldProperty(datetime)
    unicode_ = FieldProperty(str)
    varchar = FieldProperty(str)
    password = FieldProperty(str)
    oneof = FieldProperty(S.OneOf("one", "two", "three"))
    

class Department(SproxTestClass):
    class __mongometa__:
        name = 'department_rs'
        
    _id = FieldProperty(int)
    name = FieldProperty(str)
    

class DocumentCategory(SproxTestClass):
    class __mongometa__:
        name = 'document_category_rs'

    _id = FieldProperty(int)
    document_category_id = FieldProperty(int)
    department_id = ForeignIdProperty(Department)
    department = RelationProperty(Department)
    name = FieldProperty(str)
    

class DocumentCategoryTagAssignment(SproxTestClass):
    class __mongometa__:
        name = 'document_category_tag_assignment_rs'
    
    _id = FieldProperty(S.ObjectId)
    document_category_id = ForeignIdProperty(DocumentCategory)
    document_category = RelationProperty(DocumentCategory)
    department_id = ForeignIdProperty(Department)
    department = RelationProperty(Department)
    document_category_tag_id = ForeignIdProperty("DocumentCategoryTag")
    document_category_tag = RelationProperty("DocumentCategoryTag")

class DocumentCategoryTag(SproxTestClass):
    class __mongometa__:
        name = 'document_category_tag_rs'
    
    _id = FieldProperty(S.ObjectId)
    categories = RelationProperty(DocumentCategoryTagAssignment)
    
    
class DocumentCategoryReference(SproxTestClass):
    class __mongometa__:
        name = 'document_category_reference_rs'
    
    _id = FieldProperty(S.ObjectId)
    document_category_id = ForeignIdProperty(DocumentCategory)
    category = RelationProperty(DocumentCategory)


class Document(SproxTestClass):
    class __mongometa__:
        name = 'document_rs'
    
    _id = FieldProperty(S.ObjectId)
    created = FieldProperty(datetime, if_missing=datetime.now)
    edited = FieldProperty(S.DateTime, if_missing=datetime.now)
    blob = FieldProperty(S.Binary)
    owner = ForeignIdProperty(User)
    url = FieldProperty(S.String)
    document_category_id = ForeignIdProperty(DocumentCategory)

    metadata = FieldProperty([{'name': S.String,
                               'value': S.String}])
    
    def _get_address(self):
        return self.url

    def _set_address(self, value):
        self.url = value

    category = RelationProperty(DocumentCategory)
    

class File(SproxTestClass):
    class __mongometa__:
        name = 'attachments_rs'
        
    _id = FieldProperty(S.ObjectId)
    data = FieldProperty(S.Binary)
    
    @property
    def content(self):
        return self.data

class UnrelatedDocument(SproxTestClass):
    class __mongometa__:
        name = 'document_unrelated'
    
    _id = FieldProperty(S.ObjectId)
    number = FieldProperty(S.Int)
    enabled = FieldProperty(S.Bool)
    password = FieldProperty(str)

    @property
    def something(self):
        return self.enabled

class TGMMUser(SproxTestClass):
    class __mongometa__:
        name = 'tg_mm_users'

    _id = FieldProperty(S.ObjectId)
    user_name = FieldProperty(S.String)
    _groups = FieldProperty(S.Array(str))

    def _get_groups(self):
        return Group.query.find(dict(group_name={'$in':self._groups})).all()
    def _set_groups(self, groups):
        self._groups = [group.group_name for group in groups]
    groups = ProgrammaticRelationProperty(Group, _get_groups, _set_groups)

class ModelWithRequired(SproxTestClass):
    class __mongometa__:
        name = 'model_with_required'

    _id = FieldProperty(S.ObjectId)
    value = FieldProperty(S.String, required=True)

Mapper.compile_all()


