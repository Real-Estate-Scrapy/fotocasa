from scrapy.utils.project import get_project_settings
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def connect_db():
    s = get_project_settings()
    return create_engine(URL(**s['DATABASE']))


def create_tables(engine, drop_tables=False):
    if drop_tables:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class Property(Base):
    _tablename_ = 'property'
    _table_args_ = {'schema': 'real_estate'}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        default=uuid.uuid4
    )

    url = Column(String)