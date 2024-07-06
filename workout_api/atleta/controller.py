# controller de atleta
from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, paginate

from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.atletas.models import atletaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.repository.dependencias import DatabaseDependency

api_router = APIRouter()


@api_router.post(
    '/',
    summary='Criar novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)):
    atleta_nome = atleta_in.atleta.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome
    
    atleta = (await db_session.execute(select(atletaModel).filter_by(nome=atleta_nome))).scalars().first()
    if not atleta:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f'Atleta: {atleta_nome} não foi encontrado')
    
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f'Centro de treinamento: {centro_treinamento_nome} não foi encontrado')
    
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'atleta', 'centro_treinamento'}))
        atleta_model.atleta_id = atleta.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        
        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError as e:
        db_session.rollback()
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(status_code=303, detail=f"Já existe um atleta cadastrado com o CPF: {atleta_in.atleta.cpf}")
        raise
    except Exception:
        db_session.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro ao inserir os dados no banco'
        )
    
    return atleta_out


@api_router.get(
    '/',
    summary='Consultar todos os atletas',
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletaOut],
)
async def query(db_session: DatabaseDependency, nome: str = Query(None), cpf: str = Query(None)) -> Page[AtletaOut]:
    query = select(AtletaModel)
    if nome:
        query = query.filter(AtletaModel.nome == nome)
    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)
    
    atletas = (await db_session.execute(query)).scalars().all()
    return paginate(atletas)


@api_router.get(
    '/{id}',
    summary='Consultar atleta',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta = (await db_session.execute(select(atletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')
    return AtletaOut.model_validate(atleta)


@api_router.patch(
    '/{id}',
    summary='Editar um atleta',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def update(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta = (await db_session.execute(select(atletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)
        
    await db_session.commit()
    await db_session.refresh(atleta)
    return AtletaOut.model_validate(atleta)


@api_router.delete(
    '/{id}',
    summary='Deletar atleta',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta = (await db_session.execute(select(atletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')
    
    await db_session.delete(atleta)
    await db_session.commit()
