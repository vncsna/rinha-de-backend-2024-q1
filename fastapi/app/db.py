from sqlalchemy import Column, Integer, String, BigInteger, CHAR, ForeignKey, Text, TIMESTAMP, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings import settings


Base = declarative_base()

engine = create_engine(settings.postgres_dsn.unicode_string())

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = Session()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    else:
        if session.is_active:
            session.commit()
    finally:
        session.close()


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    limit = Column(BigInteger)
    balance = Column(BigInteger)


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    value = Column(BigInteger)
    type = Column(CHAR(1))
    description = Column(Text)
    created_at = Column(TIMESTAMP, default=func.now())
    customer_id = Column(Integer, ForeignKey('customers.id'))
