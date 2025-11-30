"""Script para inserir produtos fictícios do O Boticário e Natura no banco de dados"""

import random
from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import Marca, Pedido, PedidoItem, Produto, Usuario, Venda


def generate_sku(nome: str, marca: str) -> str:
    """Gera SKU baseado no nome do produto e marca"""
    prefix = "BOT" if marca.lower() == "boticário" or marca.lower() == "o boticário" else "NAT"
    nome_clean = nome.upper().replace(" ", "-").replace("'", "").replace("Ç", "C")
    nome_clean = "".join(c for c in nome_clean if c.isalnum() or c == "-")
    return f"{prefix}-{nome_clean[:20]}"


def get_or_create_usuario(db: Session) -> Usuario:
    """Busca ou cria um usuário padrão para os pedidos"""
    usuario = db.query(Usuario).filter(
        Usuario.email.ilike("%admin%")
    ).first()
    
    if not usuario:
        usuario = Usuario(
            id=uuid4(),
            nome="Admin",
            sobrenome="Sistema",
            email="admin@sistema.com",
            celular="11999999999",
            senha="admin123",
            permissao="ADMIN",
            ativo=True,
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow(),
        )
        db.add(usuario)
        db.flush()
        print("✓ Usuário padrão criado")
    else:
        print(f"✓ Usuário padrão já existe (ID: {usuario.id})")
    
    return usuario


def insert_produtos():
    """Insere produtos do O Boticário e Natura no banco de dados"""
    db: Session = SessionLocal()

    try:
        print("🚀 Iniciando inserção de produtos...\n")

        # Buscar ou criar marca O Boticário
        marca_boticario = db.query(Marca).filter(
            Marca.nome.ilike("%boticário%")
        ).first()

        if not marca_boticario:
            marca_boticario = Marca(
                id=uuid4(),
                nome="O Boticário",
                descricao="Marca de cosméticos e perfumaria brasileira",
                imagem_url="https://example.com/boticario.jpg",
                criado_em=datetime.utcnow(),
                atualizado_em=datetime.utcnow(),
            )
            db.add(marca_boticario)
            db.flush()
            print("✓ Marca 'O Boticário' criada")
        else:
            print(f"✓ Marca 'O Boticário' já existe (ID: {marca_boticario.id})")

        # Buscar ou criar marca Natura
        marca_natura = db.query(Marca).filter(
            Marca.nome.ilike("%natura%")
        ).first()

        if not marca_natura:
            marca_natura = Marca(
                id=uuid4(),
                nome="Natura",
                descricao="Marca de produtos naturais e cosméticos brasileira",
                imagem_url="https://example.com/natura.jpg",
                criado_em=datetime.utcnow(),
                atualizado_em=datetime.utcnow(),
            )
            db.add(marca_natura)
            db.flush()
            print("✓ Marca 'Natura' criada")
        else:
            print(f"✓ Marca 'Natura' já existe (ID: {marca_natura.id})")

        # Produtos O Boticário
        produtos_boticario = [
            {
                "nome": "Egeo Vanilla Vibe Desodorante Colônia 90ml",
                "descricao": "Fragrância feminina que traz a doçura da baunilha artesanal combinada ao toque picante da Pimenta Rosa",
                "preco_unitario": 154.90,
                "quantidade": 25,
            },
            {
                "nome": "Lily Eau de Parfum 90ml",
                "descricao": "Fragrância feminina com notas florais e amadeiradas",
                "preco_unitario": 179.90,
                "quantidade": 18,
            },
            {
                "nome": "Malbec Desodorante Colônia 100ml",
                "descricao": "Fragrância masculina marcante com notas amadeiradas e especiadas",
                "preco_unitario": 89.90,
                "quantidade": 32,
            },
            {
                "nome": "Cuide-se Bem Nuvem Loção Hidratante 400ml",
                "descricao": "Loção hidratante corporal com fragrância suave e textura leve",
                "preco_unitario": 48.90,
                "quantidade": 45,
            },
            {
                "nome": "Egeo Dolce Desodorante Body Spray 150ml",
                "descricao": "Body spray com fragrância doce e envolvente",
                "preco_unitario": 23.90,
                "quantidade": 60,
            },
            {
                "nome": "Nativa SPA Refil Loção Desodorante Hidratante Corporal Ameixa Negra 350ml",
                "descricao": "Refil de loção hidratante com fragrância intensa de ameixa negra",
                "preco_unitario": 67.90,
                "quantidade": 28,
            },
            {
                "nome": "Make B. Base Líquida Alta Cobertura 30ml",
                "descricao": "Base líquida com alta cobertura e acabamento natural",
                "preco_unitario": 49.90,
                "quantidade": 22,
            },
            {
                "nome": "Cuide-se Bem Desodorante Antitranspirante Aerosol 150ml",
                "descricao": "Desodorante antitranspirante em aerosol com proteção de 48h",
                "preco_unitario": 19.90,
                "quantidade": 55,
            },
            {
                "nome": "Kit de Pincéis Tudão Quem Disse, Berenice? (5 itens)",
                "descricao": "Kit com 5 pincéis para maquiagem completa",
                "preco_unitario": 82.90,
                "quantidade": 15,
            },
            {
                "nome": "Floratta Blue Desodorante Colônia 90ml",
                "descricao": "Fragrância feminina fresca com notas aquáticas e florais",
                "preco_unitario": 129.90,
                "quantidade": 20,
            },
        ]

        # Produtos Natura
        produtos_natura = [
            {
                "nome": "Ekos Açaí Polpa Hidratante 200ml",
                "descricao": "Hidratante corporal com óleo de açaí e manteiga de cupuaçu",
                "preco_unitario": 55.00,
                "quantidade": 30,
            },
            {
                "nome": "Kaiak Urbe Desodorante Colônia 100ml",
                "descricao": "Fragrância masculina com notas aquáticas e especiadas",
                "preco_unitario": 129.90,
                "quantidade": 25,
            },
            {
                "nome": "Chronos Acqua Biohidratante 50g",
                "descricao": "Gel hidratante facial com ação prebiótica e textura aquosa",
                "preco_unitario": 98.00,
                "quantidade": 18,
            },
            {
                "nome": "Sabonete Líquido Mãos Natura Bothânica Ficus Herb 250ml",
                "descricao": "Sabonete líquido para as mãos com fragrância herbal de figo",
                "preco_unitario": 29.90,
                "quantidade": 40,
            },
            {
                "nome": "Óleo Hidratante Corpo Natura Bothânica Origins 200ml",
                "descricao": "Óleo hidratante corporal com ingredientes naturais para pele macia e perfumada",
                "preco_unitario": 49.90,
                "quantidade": 28,
            },
            {
                "nome": "Spray de Ambientes Natura Bothânica Aura Gingi 200ml",
                "descricao": "Spray para ambientes com fragrância revigorante de gengibre",
                "preco_unitario": 39.90,
                "quantidade": 35,
            },
            {
                "nome": "Lumina Desodorante Colônia 100ml",
                "descricao": "Fragrância feminina com notas florais e frutais",
                "preco_unitario": 119.90,
                "quantidade": 22,
            },
            {
                "nome": "Ekos Castanha Desodorante Corporal 200ml",
                "descricao": "Desodorante corporal com óleo de castanha-do-pará",
                "preco_unitario": 45.00,
                "quantidade": 38,
            },
            {
                "nome": "Tododia Sabonete Líquido Ameixa 250ml",
                "descricao": "Sabonete líquido com fragrância de ameixa",
                "preco_unitario": 24.90,
                "quantidade": 50,
            },
            {
                "nome": "Mamãe e Bebê Loção Hidratante 200ml",
                "descricao": "Loção hidratante suave para mãe e bebê",
                "preco_unitario": 42.90,
                "quantidade": 27,
            },
        ]

        produtos_criados = []

        # Inserir produtos O Boticário
        print(f"\n📦 Inserindo {len(produtos_boticario)} produtos do O Boticário...")
        for prod_data in produtos_boticario:
            sku = generate_sku(prod_data["nome"], "O Boticário")
            produto = Produto(
                id=uuid4(),
                nome=prod_data["nome"],
                descricao=prod_data["descricao"],
                sku=sku,
                preco_unitario=prod_data["preco_unitario"],
                valor_venda=prod_data["preco_unitario"],
                quantidade=prod_data["quantidade"],
                catalogo=True,
                tag="boticario",
                marca_id=marca_boticario.id,
                criado_em=datetime.utcnow(),
                atualizado_em=datetime.utcnow(),
            )
            produtos_criados.append(produto)
            print(f"  ✓ {prod_data['nome'][:50]}... (SKU: {sku})")

        # Inserir produtos Natura
        print(f"\n📦 Inserindo {len(produtos_natura)} produtos da Natura...")
        for prod_data in produtos_natura:
            sku = generate_sku(prod_data["nome"], "Natura")
            produto = Produto(
                id=uuid4(),
                nome=prod_data["nome"],
                descricao=prod_data["descricao"],
                sku=sku,
                preco_unitario=prod_data["preco_unitario"],
                valor_venda=prod_data["preco_unitario"],
                quantidade=prod_data["quantidade"],
                catalogo=True,
                tag="natura",
                marca_id=marca_natura.id,
                criado_em=datetime.utcnow(),
                atualizado_em=datetime.utcnow(),
            )
            produtos_criados.append(produto)
            print(f"  ✓ {prod_data['nome'][:50]}... (SKU: {sku})")

        db.add_all(produtos_criados)
        db.flush()

        print(f"\n✅ {len(produtos_criados)} produtos inseridos com sucesso!")
        print(f"\n📊 Resumo:")
        print(f"  - O Boticário: {len(produtos_boticario)} produtos")
        print(f"  - Natura: {len(produtos_natura)} produtos")
        print(f"  - Total: {len(produtos_criados)} produtos")

        # Criar pedidos históricos
        print(f"\n🛒 Criando pedidos históricos no último ano...")
        usuario = get_or_create_usuario(db)
        
        agora = datetime.utcnow()
        inicio_ano = agora - timedelta(days=365)
        
        # Criar 75 pedidos distribuídos no último ano
        # Maior concentração nos últimos 3 meses (40 pedidos)
        # Resto distribuído ao longo do ano (35 pedidos)
        num_pedidos = 75
        pedidos_criados = []
        
        status_options = ["PENDENTE", "CONCLUIDO", "CANCELADO"]
        
        for i in range(num_pedidos):
            # Distribuição: 40% nos últimos 90 dias, 60% no resto do ano
            if i < 30:  # Últimos 3 meses (maior concentração)
                dias_aleatorios = random.randint(0, 90)
            else:  # Resto do ano
                dias_aleatorios = random.randint(0, 365)
            
            data_pedido = inicio_ano + timedelta(days=dias_aleatorios)
            # Garantir que a data não seja no futuro
            if data_pedido > agora:
                data_pedido = agora - timedelta(days=random.randint(1, 7))
            
            status = random.choice(status_options)
            
            # Criar venda apenas para pedidos concluídos
            venda = None
            if status == "CONCLUIDO":
                venda = Venda(
                    id=uuid4(),
                    data_venda=data_pedido,
                    valor_total=0,  # Será calculado depois
                    desconto=0,
                    pagamento_realizado=True,
                    criado_em=data_pedido,
                    atualizado_em=data_pedido,
                )
                db.add(venda)
                db.flush()
            
            # Criar pedido
            pedido = Pedido(
                id=uuid4(),
                usuario_id=usuario.id,
                venda_id=venda.id if venda else None,
                status=status,
                criado_em=data_pedido,
                atualizado_em=data_pedido,
            )
            db.add(pedido)
            db.flush()
            
            # Adicionar 1-5 produtos aleatórios ao pedido
            num_produtos = random.randint(1, 5)
            produtos_selecionados = random.sample(produtos_criados, min(num_produtos, len(produtos_criados)))
            
            valor_total_pedido = 0
            for produto in produtos_selecionados:
                quantidade = random.randint(1, 3)
                preco_unitario = float(produto.preco_unitario or 0)
                subtotal = preco_unitario * quantidade
                valor_total_pedido += subtotal
                
                pedido_item = PedidoItem(
                    id=uuid4(),
                    pedido_id=pedido.id,
                    produto_id=produto.id,
                    quantidade=quantidade,
                    preco_unitario=preco_unitario,
                )
                db.add(pedido_item)
            
            # Atualizar valor total da venda se existir
            if venda:
                venda.valor_total = valor_total_pedido
                venda.atualizado_em = data_pedido
            
            pedidos_criados.append(pedido)
            
            if (i + 1) % 15 == 0:
                print(f"  ✓ {i + 1}/{num_pedidos} pedidos criados...")
        
        db.commit()
        print(f"\n✅ {len(pedidos_criados)} pedidos históricos criados com sucesso!")
        print(f"   Período: {inicio_ano.strftime('%d/%m/%Y')} até {agora.strftime('%d/%m/%Y')}")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro ao inserir produtos: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    insert_produtos()

