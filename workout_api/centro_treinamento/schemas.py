from typing import Annotated
from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema


class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT king', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do centro de treinamento', example='Rua x QD2', max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietário do centro de treinamento', example='Marcos', max_length=30)]
    
    
    
    class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT king', max_length=20)]
    
    
class CentroTreinamentoOut(CentroTreinamento):
    id: Annotated[UUID4, Field(description='Identificador do centro de treinamento')]