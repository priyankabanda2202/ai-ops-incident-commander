from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///incidents.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True)
    service = Column(String)
    description = Column(Text)
    action = Column(String)

Base.metadata.create_all(engine)

def save_incident(service, description, action):
    session = Session()
    incident = Incident(
        service=service,
        description=description,
        action=action
    )
    session.add(incident)
    session.commit()
    session.close()

def get_all_incidents():
    session = Session()
    rows = session.query(Incident).all()
    session.close()
    return rows