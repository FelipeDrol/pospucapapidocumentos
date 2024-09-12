from flask_openapi3 import OpenAPI, request, Info, Tag
from flask_openapi3 import Info
from flask import Flask, jsonify, redirect
from sqlalchemy.exc import IntegrityError
from model import Session, Documentos
from logger import logger
from schemas import *
from flask_cors import CORS
import base64
import os

info = Info(title="API de Documentos", version="1.0.0")
app = OpenAPI(__name__, info=info)

CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
documento_tag = Tag(name="Documento", description="Visualização, Adição, edição e remoção de documentos à base")

#Metodos Gerais
def get_todos_documentos():
    return Session().query(Documentos).all()

def retornos_listagem_documentos():
    return {"200": ListagemDocumentosSchema, "400": ErrorSchema, "404": ErrorSchema}

def retornos_documento_view():
    return {"200": DocumentoViewSchema, "400": ErrorSchema, "404": ErrorSchema}

def retorno_erro(e, mensagem, code):
    logger.warning(e)
    error_msg = mensagem + ": " + repr(e)
    return {"message": error_msg}, code

#Apis Home
@app.get('/', tags=[home_tag])
def home():
    """
    Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')
    
#Apis Documentos
@app.get('/documentos', tags=[documento_tag], responses = retornos_listagem_documentos())
def get_documentos():
    """
    Retorna todos os documentos cadastrados
    """
    try:
        documentos = Session().query(Documentos).all()
        return apresenta_documentos(documentos), 200
    except Exception as e:
        retorno_erro(e, "Não foi possível obter o documento", 400)
        error_msg = "Erro ao buscar todos os documentos: " + repr(e)    
        return {"message": error_msg}, 404

@app.get('/documento', tags=[documento_tag], responses = retornos_documento_view())
def get_documento(query: DocumentosBuscaUsuarioSchema):
    """
    Retorna todos Documento a partir do seu usuario
    """
    try:
        documentos = Session().query(Documentos).filter(Documentos.usuario == query.usuario).all()
        if(documentos):
            return apresenta_documentos(documentos), 200
        else:
            return {"message": "Documento não localizado"}, 404
    except Exception as e:
        retorno_erro(e, "Erro ao obter documento por id", 400)

@app.delete('/documento', tags=[documento_tag], responses = retornos_listagem_documentos())
def del_documento(query: DocumentosBuscaUsuarioSchema):
    """
    Deleta TODOS documento a partir do seu Email
    Retorna todos os documentos cadastrados
    """
    try:
        session = Session()
        sqlQuery = session.query(Documentos).filter(Documentos.usuario == query.usuario)
        documento = sqlQuery.first()

        if(documento):
            sqlQuery.delete()
            session.commit()
            return apresenta_documentos([]), 200
        else:
            return {"message": "Documento não localizado"}, 404
    except Exception as e:
        retorno_erro(e, "Não foi possível obter o documento")
        error_msg = "Erro ao deletar documento: " + repr(e)
        return {"message": error_msg}, 404
    
@app.post('/documento', tags=[documento_tag], responses = retornos_documento_view())
def add_documento(form: DocumentoViewSchema):
    """
    Adiciona um novo documento à base
    Retorna todos os documento cadastrados
    """
    try:
        binary_data = base64.b64decode(form.base64)
        documento = Documentos(base64=binary_data,nome_arquivo = form.nome_arquivo,campo = form.campo, valorEscolha = form.valorEscolha, usuario = form.usuario)
        session = Session()
        session.add(documento)
        session.commit()

        return apresenta_documento(documento), 200
    except Exception as e:
        retorno_erro(e, "Não foi possível obter o documento", 400)
        error_msg = "Não foi possível adicionar o novo documento:" + repr(e)
        return {"message": error_msg}, 404
    
@app.put('/documento', tags=[documento_tag], responses = retornos_documento_view())
def edit_documento(form: DocumentoEditSchema):
    """
    Edita um documento existente pelo seu id
    Retorna todos os documentos cadastrados
    """
    try:
        session = Session()
        documento = session.query(Documentos).filter(Documentos.id == form.id).first()
        if(documento):
            binary_data = base64.b64decode(form.base64)
            documento.base64 = binary_data
            documento.usuario = form.usuario
            documento.nome_arquivo = form.nome_arquivo
            documento.campo = form.campo
            documento.valorEscolha = form.valorEscolha
            session.commit()

            return apresenta_documento(documento), 200
        else:
            return {"message": "Documento não localizado"}, 404
    except Exception as e:
        retorno_erro(e, "Erro ao editar Documento")