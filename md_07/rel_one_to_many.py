from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase,relationship
from sqlalchemy import Column, String, Integer, Text, ForeignKey, select


engine = create_engine('sqlite:///test.db')
Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    name = Column(String(20))
    articles = relationship('Article', back_populates='author')


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer(), primary_key=True)
    title = Column(String(255))
    content = Column(Text())
    user_id = Column(Integer(), ForeignKey('users.id'))
    author = relationship('User', back_populates='articles')


Base.metadata.create_all(engine)
Base.metadata.bind = engine


if __name__ == '__main__':
    # Create
    user = User(name='Boris Johnson')
    session.add(user)
    session.commit()
    
    article = article = Article(title='Our country’s saddest day', content='Lorem ipsum...', user_id=user.id)
    session.add(article)
    session.commit()

    # Read
    statement = select(User)
    user = session.scalars(statement).one()
    print(user.id, user.name)
