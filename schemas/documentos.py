from pydantic import *
from typing import List
from model.documentos import Documentos
import base64

class DocumentoViewSchema(BaseModel):
    """ 
    Define como um novo documento a ser inserido deve ser representado
    """
    base64: str
    nome_arquivo: str = "arquivo.txt"
    campo: str = "Email"
    valorEscolha: str = "RG"
    usuario: str = "usuario@email.com"


class ListagemDocumentosSchema(BaseModel):
    """ 
    Define como uma listagem de Documentos será retornada
    """
    documentos:List[DocumentoViewSchema]

class DocumentoEditSchema(BaseModel):
    """ 
    Define como um documento deve ser editado
    """
    base64: str
    nome_arquivo: str = "arquivo.txt"
    usuario: str = "usuario@email.com"
    campo: str = "Email"
    valorEscolha: str = "RG"
    id: int = 1

class DocumentoBuscaIdSchema(BaseModel):
    """ 
    Define como deve ser a estrutura que representa a busca. Que será feita apenas com base no id do Documento
    """
    id: int = 1

class DocumentosBuscaUsuarioSchema(BaseModel):
    """ 
    Define como deve ser a estrutura que representa a busca. Que será feita apenas com base no usuario do Documento
    """
    usuario: str = "usuario@email.com"

def apresenta_documentos(documentos: List[Documentos]):
    """ 
    Retorna todos os documentos
    """
    result = []
    for documento in documentos:
        encoded_data = base64.b64encode(documento.base64).decode('utf-8')
        result.append({
            "id": documento.id,
            "usuario": documento.usuario,
            "base64": encoded_data,
            "nome_arquivo": documento.nome_arquivo,
            "campo": documento.campo,
            "valorEscolha": documento.valorEscolha,
            "data_insercao": documento.data_insercao
        })

    return {"documentos": result}

def apresenta_documento(documento: Documentos):
    """ 
    Retorna um documento
    """
    encoded_data = base64.b64encode(documento.base64).decode('utf-8')
    return {
            "id": documento.id,
            "usuario": documento.usuario,
            "base64": encoded_data,
            "nome_arquivo": documento.nome_arquivo,
            "campo": documento.campo,
            "valorEscolha": documento.valorEscolha,
            "data_insercao": documento.data_insercao
        }