#Servem para fazer as validações e dados que irao aparecer na api#
from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from workout_api.atleta.schemas import AtletaIn
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixin


class AtletaIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='Joao', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_length=11)] #PODE-SE USAR UM VALIDATOR PARA VERIFICAÇÃO
    idade: Annotated[int, Field(description='Idade do atleta', example='25', )]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example='100.00')]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example='150.0')]
    sexo: Annotated[str, Field(description='Sexo do atleta', examples='M', max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='centro de treinamento do atleta')]
    
   
  
class AtletaIn(Atleta):
    pass
    
    
class AtletaOut(Atleta, OutMixin):
    pass


class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='Joao', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example='25', )]