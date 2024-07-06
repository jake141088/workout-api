# controller de categorias
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, Query, status
from pydantic import UUID4
from sqlalchemy import select
from fastapi_pagination import Page, paginate

from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.contrib.repository.dependencias import DatabaseDependency

api_router = APIRouter()


@api_router.post(
    '/',
    summary='Criar uma nova categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)) -> CategoriaOut:
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    db_session.add(categoria_model)
    await db_session.commit()
    return categoria_out


@api_router.get(
    '/',
    summary='Consultar todas categorias',
    status_code=status.HTTP_200_OK,
    response_model=Page[CategoriaOut],
)
async def query(db_session: DatabaseDependency) -> Page[CategoriaOut]:
    categorias = (await db_session.execute(select(CategoriaModel))).scalars().all()
    return paginate(categorias)


@api_router.get(
    '/{id}',
    summary='Consultar categoria',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def query(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Categoria não encontrada no id: {id}')
    return CategoriaOut.model_validate(categoria)
