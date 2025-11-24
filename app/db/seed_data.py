"""Script para inserir dados de teste no banco de dados"""

from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import (
    Marca,
    Pedido,
    PedidoItem,
    Produto,
    Usuario,
    Venda,
)


def seed_data():
    """Insere dados de exemplo no banco"""
    db: Session = SessionLocal()

    try:
        print("Inserindo dados de teste...")

        # Criar marcas
        marca1 = Marca(
            id=uuid4(),
            nome="Boticário",
            descricao="Marca de cosméticos brasileira",
            imagem_url="https://example.com/boticario.jpg",
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow(),
        )
        marca2 = Marca(
            id=uuid4(),
            nome="Natura",
            descricao="Marca de produtos naturais",
            imagem_url="https://example.com/natura.jpg",
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow(),
        )
        marca3 = Marca(
            id=uuid4(),
            nome="Avon",
            descricao="Marca de beleza e cosméticos",
            imagem_url="https://example.com/avon.jpg",
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow(),
        )

        db.add_all([marca1, marca2, marca3])
        db.flush()

        print(f"✓ Criadas 3 marcas: {marca1.nome}, {marca2.nome}, {marca3.nome}")

        # Criar produtos
        produtos = []
        produtos_data = [
            {
                "nome": "Perfume Malbec",
                "descricao": "Perfume masculino",
                "sku": "BOT-MALBEC-001",
                "preco_unitario": 89.90,
                "valor_venda": 89.90,
                "quantidade": 50,
                "catalogo": True,
                "tag": "boticario",
                "marca_id": marca1.id,
            },
            {
                "nome": "Shampoo Hidratação",
                "descricao": "Shampoo para cabelos secos",
                "sku": "BOT-SHAMPOO-001",
                "preco_unitario": 24.90,
                "valor_venda": 24.90,
                "quantidade": 3,  # Estoque baixo
                "catalogo": True,
                "tag": "boticario",
                "marca_id": marca1.id,
            },
            {
                "nome": "Creme Facial Natura",
                "descricao": "Creme anti-idade",
                "sku": "NAT-CREME-001",
                "preco_unitario": 45.00,
                "valor_venda": 45.00,
                "quantidade": 15,
                "catalogo": True,
                "tag": "natura",
                "marca_id": marca2.id,
            },
            {
                "nome": "Batom Avon",
                "descricao": "Batom matte",
                "sku": "AVN-BATOM-001",
                "preco_unitario": 19.90,
                "valor_venda": 19.90,
                "quantidade": 0,  # Sem estoque
                "catalogo": True,
                "tag": "avon",
                "marca_id": marca3.id,
            },
            {
                "nome": "Desodorante Boticário",
                "descricao": "Desodorante roll-on",
                "sku": "BOT-DESOD-001",
                "preco_unitario": 12.90,
                "valor_venda": 12.90,
                "quantidade": 100,
                "catalogo": True,
                "tag": "boticario",
                "marca_id": marca1.id,
            },
        ]

        for prod_data in produtos_data:
            produto = Produto(
                id=uuid4(),
                criado_em=datetime.utcnow(),
                atualizado_em=datetime.utcnow(),
                **prod_data,
            )
            produtos.append(produto)

        db.add_all(produtos)
        db.flush()

        print(f"✓ Criados {len(produtos)} produtos")

        # Criar usuários
        usuario1 = Usuario(
            id=uuid4(),
            nome="João",
            sobrenome="Silva",
            email="joao.silva@example.com",
            celular="11999999999",
            senha="hash_senha_123",
            permissao="ADMIN",
            ativo=True,
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow(),
        )
        usuario2 = Usuario(
            id=uuid4(),
            nome="Maria",
            sobrenome="Santos",
            email="maria.santos@example.com",
            celular="11888888888",
            senha="hash_senha_456",
            permissao="COMUM",
            ativo=True,
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow(),
        )

        db.add_all([usuario1, usuario2])
        db.flush()

        print(f"✓ Criados 2 usuários: {usuario1.nome}, {usuario2.nome}")

        # Criar vendas
        venda1 = Venda(
            id=uuid4(),
            data_venda=datetime.utcnow() - timedelta(days=10),
            valor_total=224.80,  # 2x Perfume (89.90) + 1x Creme (45.00)
            desconto=0.00,
            pagamento_realizado=True,
            criado_em=datetime.utcnow() - timedelta(days=10),
            atualizado_em=datetime.utcnow() - timedelta(days=10),
        )
        venda2 = Venda(
            id=uuid4(),
            data_venda=datetime.utcnow() - timedelta(days=2),
            valor_total=74.70,  # 3x Shampoo (24.90)
            desconto=5.00,
            pagamento_realizado=False,
            criado_em=datetime.utcnow() - timedelta(days=2),
            atualizado_em=datetime.utcnow() - timedelta(days=2),
        )
        venda3 = Venda(
            id=uuid4(),
            data_venda=datetime.utcnow() - timedelta(days=5),
            valor_total=153.40,  # 1x Perfume (89.90) + 5x Desodorante (12.90)
            desconto=0.00,
            pagamento_realizado=True,
            criado_em=datetime.utcnow() - timedelta(days=5),
            atualizado_em=datetime.utcnow() - timedelta(days=3),
        )

        db.add_all([venda1, venda2, venda3])
        db.flush()

        print("✓ Criadas 3 vendas")

        # Criar pedidos
        pedido1 = Pedido(
            id=uuid4(),
            usuario_id=usuario1.id,
            venda_id=venda1.id,
            status="CONCLUIDO",
            criado_em=datetime.utcnow() - timedelta(days=10),
            atualizado_em=datetime.utcnow() - timedelta(days=8),
        )
        pedido2 = Pedido(
            id=uuid4(),
            usuario_id=usuario2.id,
            venda_id=venda2.id,
            status="PENDENTE",
            criado_em=datetime.utcnow() - timedelta(days=2),
            atualizado_em=datetime.utcnow() - timedelta(days=2),
        )
        pedido3 = Pedido(
            id=uuid4(),
            usuario_id=usuario1.id,
            venda_id=venda3.id,
            status="CONCLUIDO",
            criado_em=datetime.utcnow() - timedelta(days=5),
            atualizado_em=datetime.utcnow() - timedelta(days=3),
        )

        db.add_all([pedido1, pedido2, pedido3])
        db.flush()

        print("✓ Criados 3 pedidos")

        # Criar itens dos pedidos
        itens = [
            PedidoItem(
                id=uuid4(),
                pedido_id=pedido1.id,
                produto_id=produtos[0].id,  # Perfume Malbec
                quantidade=2,
                preco_unitario=89.90,
            ),
            PedidoItem(
                id=uuid4(),
                pedido_id=pedido1.id,
                produto_id=produtos[2].id,  # Creme Facial
                quantidade=1,
                preco_unitario=45.00,
            ),
            PedidoItem(
                id=uuid4(),
                pedido_id=pedido2.id,
                produto_id=produtos[1].id,  # Shampoo
                quantidade=3,
                preco_unitario=24.90,
            ),
            PedidoItem(
                id=uuid4(),
                pedido_id=pedido3.id,
                produto_id=produtos[0].id,  # Perfume Malbec
                quantidade=1,
                preco_unitario=89.90,
            ),
            PedidoItem(
                id=uuid4(),
                pedido_id=pedido3.id,
                produto_id=produtos[4].id,  # Desodorante
                quantidade=5,
                preco_unitario=12.90,
            ),
        ]

        db.add_all(itens)
        db.commit()

        print(f"✓ Criados {len(itens)} itens de pedido")
        print("\n✅ Dados de teste inseridos com sucesso!")
        print("\nResumo:")
        print(f"  - {len([marca1, marca2, marca3])} marcas")
        print(f"  - {len(produtos)} produtos")
        print(f"  - {len([usuario1, usuario2])} usuários")
        print(f"  - {len([venda1, venda2, venda3])} vendas")
        print(f"  - {len([pedido1, pedido2, pedido3])} pedidos")
        print(f"  - {len(itens)} itens de pedido")

    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao inserir dados: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
