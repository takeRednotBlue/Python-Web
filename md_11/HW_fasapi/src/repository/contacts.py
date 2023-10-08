from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.database.models import Contact
from src.schemas.contacts import ResponseContact, ContactModel


async def get_contacts(skip: int, limit: int, db: Session) -> list[ResponseContact] | None:
    statement = select(Contact).offset(skip).limit(limit)
    return db.execute(statement).scalars()


async def get_contact_by_first_name(first_name: str, db: Session) -> ResponseContact | None:
    statement = select(Contact).filter(Contact.first_name == first_name.title())
    return db.execute(statement).scalars()


async def get_contact_by_last_name(last_name: str, db: Session) -> ResponseContact | None:
    statement = select(Contact).filter(Contact.last_name == last_name.title())
    return db.execute(statement).scalars()


async def get_contact_by_email(email: str, db: Session) -> ResponseContact | None:
    statement = select(Contact).filter(Contact.email == email.lower())
    return db.execute(statement).scalars()


async def get_contacts_by_birthday(interval: int, db: Session) -> list[ResponseContact] | None:
    start_date = datetime.now().date() - timedelta(days=interval)
    statement = select(Contact)
    contacts = db.execute(statement).scalars()
    result = []
    for contact in contacts:
        if start_date <= contact.birthday.replace(year=start_date.year):
            result.append(contact)
    return result


async def create_contact(body: ContactModel, db: Session) -> ResponseContact:
    contact = Contact(**body.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contact(contact_id: int, db: Session) -> ResponseContact | None:
    statement = select(Contact).filter(Contact.id == contact_id)
    return db.execute(statement).scalar_one_or_none()


async def update_contact(body: ContactModel, contact_id: int, db: Session) -> ResponseContact | None:
    statement = select(Contact).filter(Contact.id == contact_id)
    contact = db.execute(statement).scalar_one_or_none()
    if not contact:
        return None
    contact.first_name = body.first_name
    contact.last_name = body.last_name
    contact.phone = body.phone
    contact.email = body.email
    contact.birthday = body.birthday
    db.commit()
    db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: Session) -> ResponseContact | None:
    statement = select(Contact).filter(Contact.id == contact_id)
    contact = db.execute(statement).scalar_one_or_none()
    if not contact:
        return None
    db.delete(contact)
    db.commit()
    return contact




