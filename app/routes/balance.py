from fastapi import APIRouter, HTTPException, status, Depends
from database.database import get_session
from models.user import User
from cruds import crud_user as UserService

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, validator


balance_route = APIRouter(tags=['Balance'])


class BalanceInquiry(BaseModel):
    email: str


@balance_route.post('/user_balance')
async def user_balance( data : BalanceInquiry, session=Depends(get_session)) -> dict:
    user = UserService.get_user_by_email( data.email, session=session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    return {"user balance": user.balance}


class BalanceUpdate(BaseModel):
    email: str
    amount: float

    


@balance_route.post('/add_funds')
async def update_balance( data : BalanceUpdate, session=Depends(get_session)) -> dict:
    user = UserService.get_user_by_email(data.email, session=session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not exist")

    new_balance = user.balance + data.amount

    updated_user = UserService.update_balance(user, new_balance, session=session)

    if not updated_user:
        
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to update balance in database")
    return {"message": "Balance was changed", "new_balance": updated_user.balance}