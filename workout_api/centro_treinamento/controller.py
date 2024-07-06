# controller de centro de treinamento
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, Query, status
from pydantic import UUID4
from sqlalchemy import select
from fastapi_pagination import Page, paginate

from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.contrib.repository.dependencias import DatabaseDependency

api_router = APIRouter()


@api_router.post(
    '/',
    summary='Criar um novo centro de treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(db_session: DatabaseDependency, centro_treinamento_in: CentroTreinamentoIn = Body(...)) -> CentroTreinamentoOut:
    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
    db_session.add(centro_treinamento_model)
    await db_session.commit()
    return centro_treinamento_out


@api_router.get(
    '/',
    summary='Consultar todos os centros de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=Page[CentroTreinamentoOut],
)
async def query(db_session: DatabaseDependency) -> Page[CentroTreinamentoOut]:
    centros_treinamento = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    return paginate(centros_treinamento)


@api_router.get(
    '/{id}',
    summary='Consultar centro de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def query(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Centro de treinamento não encontrado no id: {id}')
    return CentroTreinamentoOut.model_validate(centro_treinamento)
