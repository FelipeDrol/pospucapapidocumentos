from sqlalchemy import Column, String, Integer, DateTime, LargeBinary
from datetime import datetime
from typing import Union

from  model import Base

class Documentos(Base):
    __tablename__ = 'documentos'

    id = Column("pk_documentos", Integer, primary_key=True)
    base64 = Column(LargeBinary, nullable=True)
    nome_arquivo = Column(String(140), unique=False)
    campo = Column(String(140), unique=False)
    valorEscolha = Column(String(140), unique=False)
    usuario = Column(String(140), unique=False)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, base64:LargeBinary, nome_arquivo:str, campo:str, valorEscolha:str, usuario:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria um registro de documento para um usuario

        Arguments:
            base64: binario do arquivo
            nome_arquivo: nome do arquivo
            campo: nome do campo arquivo
            valorEscolha: valorEscolha do campo arquivo
            usuario: Nome ou e-mail do usuario logado
            data_insercao: Data de quando o documento foi inserido à base
        """
        self.base64 = base64
        self.nome_arquivo = nome_arquivo
        self.campo = campo
        self.valorEscolha = valorEscolha
        self.usuario = usuario

        if data_insercao:
            self.data_insercao = data_insercao

