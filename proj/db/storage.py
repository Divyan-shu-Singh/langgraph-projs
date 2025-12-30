from sqlalchemy import (
    create_engine, Column, Integer, String, Text, DateTime
)
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DB_URL = "sqlite:///conversations.db"

engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False}
)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    convo_id = Column(String, index=True)
    role = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(engine)


def save_message(convo_id, role, content):
    db = Session()
    db.add(Message(
        convo_id=convo_id,
        role=role,
        content=content
    ))
    db.commit()
    db.close()


def load_messages(convo_id):
    db = Session()
    rows = (
        db.query(Message)
        .filter(Message.convo_id == convo_id)
        .order_by(Message.created_at)
        .all()
    )
    db.close()
    return [{"role": r.role, "content": r.content} for r in rows]
