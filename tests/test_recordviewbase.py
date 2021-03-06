from sprox.recordviewbase import RecordViewBase
from sprox.widgets import RecordFieldWidget
from sprox.fillerbase import RecordFiller
from sprox.test.base import setup_database, setup_records
from sprox.test.model import User
from sprox.sa.widgetselector import SAWidgetSelector
from nose.tools import raises, eq_

from sieve.operators import in_xml as in_xhtml

from sprox.widgets import TextField, HiddenField, Widget

session = None
engine  = None
connection = None
trans = None
def setup():
    global session, engine, metadata, trans
    session, engine, metadata = setup_database()
    user = setup_records(session)

class DummyWidgetSelector(object):
    def select(self, *args, **kw):
        return TextField

class DummyMetadata(object):

    def __init__(self, provider, entity):
        self.entity = entity
        self.provider = provider

    def keys(self):
        return self.provider.get_fields(self.entity)

    def __getitem__(self, name):
        return self.provider.get_field(self.entity, name)

class DummyWidget(Widget):
    params = ['test_param']


class UserRecordFiller(RecordFiller):
    __model__ = User
    
class UserView(RecordViewBase):
    __entity__ = User
    __metadata_type__ = DummyMetadata
    

class TestRecordViewBase:
    def setup(self):
        self.base = UserView(session)
        self.filler = UserRecordFiller(session)

    def _test_create(self):
        pass

    def test__widget__(self):
        value = self.filler.get_value(values={'user_id':1})
        rendered = self.base(value=value)

        assert in_xhtml("""
<td>
    <b>groups</b>
</td>""", rendered)
        assert in_xhtml("""<td> 5
    </td>""", rendered)


    def test_add_fields(self):
        class FillerWithAddFields(RecordFiller):
            __model__ = User
            __add_fields__ = {'extra': None}
            def extra(self, obj, **kw):
                return "extra data"
        
        filler = FillerWithAddFields(session)
        
        class RecordWithAddFields(RecordViewBase):
            __entity__ = User
            __metadata_type__ = DummyMetadata
            __add_fields__ = {'extra': RecordFieldWidget(field_name='extra')}
            
            
        base = RecordWithAddFields(session)
        value = filler.get_value(values={'user_id':1})

        r = base(value=value)
        assert 'extra data' in r, r
