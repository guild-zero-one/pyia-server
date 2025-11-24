"""SQLAlchemy Models for CRM"""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class Marca(Base):
    """Modelo para a tabela marca"""

    __tablename__ = "marca"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(255))
    imagem_url = Column(String(255))
    criado_em = Column(DateTime(6), default=datetime.utcnow)
    atualizado_em = Column(DateTime(6), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    produtos = relationship("Produto", back_populates="marca")


class Produto(Base):
    """Modelo para a tabela produto"""

    __tablename__ = "produto"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(255))
    sku = Column(String(255))
    preco_unitario = Column(Float)
    valor_venda = Column(Float)
    quantidade = Column(Integer)
    catalogo = Column(Boolean, default=False)
    tag = Column(String(255))
    imagem_url = Column(String(255))
    marca_id = Column(PostgresUUID(as_uuid=True), ForeignKey("marca.id"))
    criado_em = Column(DateTime(6), default=datetime.utcnow)
    atualizado_em = Column(DateTime(6), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    marca = relationship("Marca", back_populates="produtos")
    pedido_itens = relationship("PedidoItem", back_populates="produto")


class Usuario(Base):
    """Modelo para a tabela usuario"""

    __tablename__ = "usuario"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    nome = Column(String(255), nullable=False)
    sobrenome = Column(String(255))
    email = Column(String(255))
    celular = Column(String(255))
    senha = Column(String(255))
    permissao = Column(String(255))
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(6), default=datetime.utcnow)
    atualizado_em = Column(DateTime(6), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    pedidos = relationship("Pedido", back_populates="usuario", foreign_keys="Pedido.usuario_id")


class Venda(Base):
    """Modelo para a tabela venda"""

    __tablename__ = "venda"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    data_venda = Column(DateTime)
    valor_total = Column(Numeric(10, 2))
    desconto = Column(Numeric(10, 2))
    pagamento_realizado = Column(Boolean, default=False)
    criado_em = Column(DateTime(6), default=datetime.utcnow)
    atualizado_em = Column(DateTime(6), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    pedidos = relationship("Pedido", back_populates="venda", foreign_keys="Pedido.venda_id")


class Pedido(Base):
    """Modelo para a tabela pedido"""

    __tablename__ = "pedido"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    usuario_id = Column(PostgresUUID(as_uuid=True), ForeignKey("usuario.id"))
    venda_id = Column(PostgresUUID(as_uuid=True), ForeignKey("venda.id"))
    status = Column(String(255))
    criado_em = Column(DateTime(6), default=datetime.utcnow)
    atualizado_em = Column(DateTime(6), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="pedidos", foreign_keys=[usuario_id])
    venda = relationship("Venda", back_populates="pedidos", foreign_keys=[venda_id])
    itens = relationship("PedidoItem", back_populates="pedido")


class PedidoItem(Base):
    """Modelo para a tabela pedido_item"""

    __tablename__ = "pedido_item"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    pedido_id = Column(PostgresUUID(as_uuid=True), ForeignKey("pedido.id"))
    produto_id = Column(PostgresUUID(as_uuid=True), ForeignKey("produto.id"))
    quantidade = Column(Integer)
    preco_unitario = Column(Numeric(10, 2))

    # Relacionamentos
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="pedido_itens")

