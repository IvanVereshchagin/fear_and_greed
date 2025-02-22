from models.transaction import Transaction
from typing import List, Optional

def get_all_transactions(session) -> List[Transaction]:
    return session.query(Transaction).all()

def get_transaction_by_id(transaction_id: int, session) -> Optional[Transaction]:
    return session.get(Transaction, transaction_id)
   
def get_transaction_by_user_id(description: str, session) -> Optional[Transaction]:
    transaction = session.query(Transaction).filter(Transaction.description == description).first()
    if transaction:
        return transaction
    return None

def insert_transaction(new_transaction: Transaction, session) -> None:
    session.add( new_transaction)
    session.commit()
    session.refresh(new_transaction)