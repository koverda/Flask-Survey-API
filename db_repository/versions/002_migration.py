from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
answer = Table('answer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('id_questions', Integer),
    Column('id_responses', Integer),
    Column('text_a', String(length=511)),
)

question = Table('question', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text_q', String(length=511)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['answer'].create()
    post_meta.tables['question'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['answer'].drop()
    post_meta.tables['question'].drop()
