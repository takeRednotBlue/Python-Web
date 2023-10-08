from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from src.repository import contacts as repo_contacts
from src.schemas.contacts import ContactModel, ResponseContact
from src.database.db import get_db

router = APIRouter(prefix='/contacts')


@router.get('/')
async def list_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        first_name: str = None, last_name: str = None, email: str = None
                        ) -> list[ResponseContact] | ResponseContact:
    contacts = await repo_contacts.get_contacts(skip, limit, db)

    if first_name:
        contacts = await repo_contacts.get_contact_by_first_name(first_name, db)
    elif last_name:
        contacts = await repo_contacts.get_contact_by_last_name(last_name, db)
    elif email:
        contacts = await repo_contacts.get_contact_by_email(email, db)

    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no contacts")

    return contacts


@router.post('/', response_model=ResponseContact)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repo_contacts.create_contact(body, db)
    return contact


@router.get('/birthday', response_model=list[ResponseContact])
async def get_birthday(interval: int = 7, db: Session = Depends(get_db)):
    contacts = await repo_contacts.get_contacts_by_birthday(interval, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"In the next {interval} days there are no birthdays.")
    return contacts


@router.get('/{contact_id}', response_model=ResponseContact)
async def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repo_contacts.get_contact(contact_id, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact


@router.put('/{contact_id}', response_model=ResponseContact)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db)):
    new_contact = await repo_contacts.update_contact(body, contact_id, db)
    if not new_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return new_contact


@router.delete('/{contact_id}', response_model=ResponseContact)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repo_contacts.delete_contact(contact_id, db)
    return contact


