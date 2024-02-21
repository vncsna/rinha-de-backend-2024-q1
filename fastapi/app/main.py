from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db import Customer, Transaction, get_session

app = FastAPI()


class BalanceView(BaseModel):
    total: int = Field(alias="balance")
    limite: int = Field(alias="limit")
    data_extrato: datetime = Field(default_factory=datetime.now)


class TransactionView(BaseModel):
    valor: int = Field(alias="value")
    tipo: str = Field(alias="type")
    descricao: str = Field(alias="description")
    realizada_em: datetime = Field(alias="created_at")


class StatementView(BaseModel):
    saldo: BalanceView
    ultimas_transacoes: List[TransactionView]


@app.get(
    "/clientes/{customer_id}/extrato",
    response_model=StatementView,
    response_model_by_alias=False,
)
def get_statement(customer_id: int, session: Session = Depends(get_session)):
    b = session.query(Customer).filter_by(id=customer_id).one()
    t = session.query(Transaction).filter_by(cliente_id=customer_id).all()
    return {"saldo": b, "ultimas_transacoes": t}


class TransactionCreate(BaseModel):
    value: int = Field(alias="value")
    type: str = Field(alias="tipo")
    description: str = Field(alias="descricao")


class CustomerView(BaseModel):
    saldo: int = Field(alias="balance")
    limite: int = Field(alias="limit")


@app.post(
    "/clientes/{customer_id}/transacoes",
    response_model=CustomerView,
    response_model_by_alias=False,
)
def create_transaction(
    customer_id: int,
    body: TransactionCreate,
    session: Session = Depends(get_session),
):
    if customer := session.query(Customer).filter_by(id=customer_id).one_or_none():
        if customer.saldo - body.valor >= - customer.limite:
            customer.saldo = customer.saldo - body.valor
            session.add(Transaction(**{"cliente_id": customer_id, **body.model_dump()}))
        return customer
