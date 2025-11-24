"""CRM Controller"""

import json
import os
from datetime import datetime
from typing import Dict

from fastapi import HTTPException, status
from google import genai
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import GEMINI_API_KEY
from app.db.models import (
    Marca,
    Pedido,
    PedidoItem,
    Produto,
    Usuario,
    Venda,
)
from app.utils import json_transform

client = genai.Client(api_key=GEMINI_API_KEY)


def _read_prompt(filename: str) -> str:
    """Lê um arquivo de prompt da pasta gemini"""
    prompt_path = os.path.join(
        os.getcwd(), "app", "gemini", filename
    )
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def _get_relatorio_financeiro_data(db: Session) -> Dict:
    """Coleta dados agregados para relatório financeiro"""
    # Total de receita e pedidos
    pedidos_info = (
        db.query(
            func.count(Pedido.id).label("total_pedidos"),
            func.sum(
                func.coalesce(PedidoItem.preco_unitario, 0) *
                func.coalesce(PedidoItem.quantidade, 0)
            ).label("total_receita")
        )
        .join(PedidoItem, Pedido.id == PedidoItem.pedido_id)
        .first()
    )

    # Produtos mais vendidos
    produtos_vendidos = (
        db.query(
            Produto.nome,
            func.sum(PedidoItem.quantidade).label("quantidade_total"),
            func.sum(
                func.coalesce(PedidoItem.preco_unitario, 0) *
                func.coalesce(PedidoItem.quantidade, 0)
            ).label("receita")
        )
        .join(PedidoItem, Produto.id == PedidoItem.produto_id)
        .group_by(Produto.id, Produto.nome)
        .order_by(func.sum(PedidoItem.quantidade).desc())
        .limit(10)
        .all()
    )

    # Análise por status
    status_analise = (
        db.query(
            Pedido.status,
            func.count(Pedido.id).label("quantidade"),
            func.sum(
                func.coalesce(PedidoItem.preco_unitario, 0) *
                func.coalesce(PedidoItem.quantidade, 0)
            ).label("valor_total")
        )
        .join(PedidoItem, Pedido.id == PedidoItem.pedido_id)
        .group_by(Pedido.status)
        .all()
    )

    # Marcas com maior performance
    marcas_performance = (
        db.query(
            Marca.nome,
            func.sum(
                func.coalesce(PedidoItem.preco_unitario, 0) *
                func.coalesce(PedidoItem.quantidade, 0)
            ).label("receita_total"),
            func.sum(PedidoItem.quantidade).label("quantidade_vendida")
        )
        .join(Produto, Marca.id == Produto.marca_id)
        .join(PedidoItem, Produto.id == PedidoItem.produto_id)
        .group_by(Marca.id, Marca.nome)
        .order_by(func.sum(
            func.coalesce(PedidoItem.preco_unitario, 0) *
            func.coalesce(PedidoItem.quantidade, 0)
        ).desc())
        .limit(5)
        .all()
    )

    # Período
    periodo = (
        db.query(
            func.min(Pedido.criado_em).label("data_inicio"),
            func.max(Pedido.criado_em).label("data_fim")
        ).first()
    )

    return {
        "resumo": {
            "total_receita": float(pedidos_info.total_receita or 0),
            "total_pedidos": pedidos_info.total_pedidos or 0,
            "periodo": {
                "inicio": periodo.data_inicio.isoformat() if periodo and periodo.data_inicio else None,
                "fim": periodo.data_fim.isoformat() if periodo and periodo.data_fim else None,
            }
        },
        "produtos_mais_vendidos": [
            {
                "nome": p.nome,
                "quantidade_total": int(p.quantidade_total or 0),
                "receita": float(p.receita or 0)
            }
            for p in produtos_vendidos
        ],
        "analise_status": [
            {
                "status": s.status or "Sem status",
                "quantidade": int(s.quantidade or 0),
                "valor_total": float(s.valor_total or 0)
            }
            for s in status_analise
        ],
        "marcas_performance": [
            {
                "nome": m.nome,
                "receita_total": float(m.receita_total or 0),
                "quantidade_vendida": int(m.quantidade_vendida or 0)
            }
            for m in marcas_performance
        ]
    }


def get_relatorio_financeiro(db: Session):
    """Gera relatório financeiro resumido usando Gemini"""
    try:
        # Coleta dados do banco
        dados = _get_relatorio_financeiro_data(db)
        dados_json = json.dumps(dados, ensure_ascii=False, indent=2)

        # Lê o prompt
        prompt = _read_prompt("relatorio_financeiro.txt")

        # Chama Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{prompt}\n\nDados:\n{dados_json}",
        )

        # Converte resposta para JSON
        resultado = json_transform.convert_json(response.text)
        return resultado

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Arquivo de prompt não encontrado: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao gerar relatório financeiro: {str(e)}",
        )


def _get_alertas_reabastecimento_data(db: Session) -> Dict:
    """Coleta dados de produtos para alertas de reabastecimento"""
    # Quantidade vendida por produto (últimos 30 dias)
    from datetime import timedelta
    data_limite = datetime.utcnow() - timedelta(days=30)

    vendas_produtos = (
        db.query(
            PedidoItem.produto_id,
            func.sum(PedidoItem.quantidade).label("quantidade_vendida")
        )
        .join(Pedido, PedidoItem.pedido_id == Pedido.id)
        .filter(Pedido.criado_em >= data_limite)
        .group_by(PedidoItem.produto_id)
        .having(func.sum(PedidoItem.quantidade) > 0)  # Apenas produtos com vendas
        .all()
    )

    vendas_dict = {v.produto_id: v.quantidade_vendida for v in vendas_produtos}

    # Buscar apenas produtos que têm vendas E estoque baixo
    produtos_ids_com_vendas = list(vendas_dict.keys())
    
    if not produtos_ids_com_vendas:
        return {"produtos": []}

    produtos = (
        db.query(
            Produto.id,
            Produto.nome,
            Produto.sku,
            Produto.quantidade,
            Produto.nome.label("nome_produto")
        )
        .filter(
            Produto.id.in_(produtos_ids_com_vendas),
            Produto.quantidade.isnot(None),
            Produto.quantidade <= 30  # Apenas produtos com estoque <= 30
        )
        .all()
    )

    # Filtrar produtos com alta velocidade de venda
    produtos_prioritarios = []
    for p in produtos:
        vendas_30d = int(vendas_dict.get(p.id, 0))
        estoque_atual = p.quantidade or 0
        
        # Calcular dias de estoque restante (aproximado)
        if vendas_30d > 0:
            dias_restantes = (estoque_atual / vendas_30d) * 30
        else:
            dias_restantes = 999
        
        # Priorizar: produtos com vendas significativas (>= 3 unidades em 30 dias) e estoque baixo
        if vendas_30d >= 3 and estoque_atual <= 30:
            produtos_prioritarios.append({
                "id": str(p.id),
                "nome": p.nome_produto,
                "sku": p.sku,
                "quantidade_atual": estoque_atual,
                "quantidade_vendida_30dias": vendas_30d,
                "dias_estoque_restante": round(dias_restantes, 1)
            })

    return {
        "produtos": produtos_prioritarios
    }


def get_alertas_reabastecimento(db: Session):
    """Gera alertas de reabastecimento usando Gemini"""
    try:
        # Coleta dados do banco
        dados = _get_alertas_reabastecimento_data(db)
        dados_json = json.dumps(dados, ensure_ascii=False, indent=2)

        # Lê o prompt
        prompt = _read_prompt("alertas_reabastecimento.txt")

        # Chama Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{prompt}\n\nDados:\n{dados_json}",
        )

        # Converte resposta para JSON
        resultado = json_transform.convert_json(response.text)
        return resultado

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Arquivo de prompt não encontrado: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao gerar alertas de reabastecimento: {str(e)}",
        )


def _get_previsao_demanda_data(db: Session) -> Dict:
    """Coleta dados históricos para previsão de demanda"""
    # Período de análise
    periodo = (
        db.query(
            func.min(Pedido.criado_em).label("data_inicio"),
            func.max(Pedido.criado_em).label("data_fim")
        ).first()
    )

    # Vendas por produto ao longo do tempo
    vendas_produtos = (
        db.query(
            Produto.id,
            Produto.nome,
            Produto.quantidade,
            func.sum(PedidoItem.quantidade).label("total_vendido"),
            func.count(Pedido.id).label("num_pedidos")
        )
        .join(PedidoItem, Produto.id == PedidoItem.produto_id)
        .join(Pedido, PedidoItem.pedido_id == Pedido.id)
        .group_by(Produto.id, Produto.nome, Produto.quantidade)
        .all()
    )

    # Vendas por mês (tendência)
    vendas_mensais = (
        db.query(
            func.date_trunc('month', Pedido.criado_em).label("mes"),
            func.count(Pedido.id).label("num_pedidos"),
            func.sum(
                func.coalesce(PedidoItem.preco_unitario, 0) *
                func.coalesce(PedidoItem.quantidade, 0)
            ).label("receita")
        )
        .join(PedidoItem, Pedido.id == PedidoItem.pedido_id)
        .group_by(func.date_trunc('month', Pedido.criado_em))
        .order_by(func.date_trunc('month', Pedido.criado_em))
        .all()
    )

    return {
        "periodo": {
            "inicio": periodo.data_inicio.isoformat() if periodo and periodo.data_inicio else None,
            "fim": periodo.data_fim.isoformat() if periodo and periodo.data_fim else None,
        },
        "vendas_produtos": [
            {
                "id": str(v.id),
                "nome": v.nome,
                "quantidade_atual": v.quantidade or 0,
                "total_vendido": int(v.total_vendido or 0),
                "num_pedidos": int(v.num_pedidos or 0)
            }
            for v in vendas_produtos
        ],
        "tendencias_mensais": [
            {
                "mes": v.mes.isoformat() if v.mes else None,
                "num_pedidos": int(v.num_pedidos or 0),
                "receita": float(v.receita or 0)
            }
            for v in vendas_mensais
        ]
    }


def get_previsao_demanda(db: Session):
    """Gera previsão de demanda usando Gemini"""
    try:
        # Coleta dados do banco
        dados = _get_previsao_demanda_data(db)
        dados_json = json.dumps(dados, ensure_ascii=False, indent=2)

        # Lê o prompt
        prompt = _read_prompt("previsao_demanda.txt")

        # Chama Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{prompt}\n\nDados:\n{dados_json}",
        )

        # Converte resposta para JSON
        resultado = json_transform.convert_json(response.text)
        return resultado

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Arquivo de prompt não encontrado: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao gerar previsão de demanda: {str(e)}",
        )


def _get_proxima_acao_data(db: Session) -> Dict:
    """Coleta dados completos para sugestão de próxima ação"""
    # Resumo financeiro
    pedidos_info = (
        db.query(
            func.count(Pedido.id).label("total_pedidos"),
            func.sum(
                func.coalesce(PedidoItem.preco_unitario, 0) *
                func.coalesce(PedidoItem.quantidade, 0)
            ).label("total_receita")
        )
        .join(PedidoItem, Pedido.id == PedidoItem.pedido_id)
        .first()
    )

    # Pedidos pendentes
    pedidos_pendentes = (
        db.query(func.count(Pedido.id))
        .filter(Pedido.status.in_(["Pendente", "pendente", "PENDENTE"]))
        .scalar() or 0
    )

    # Produtos com estoque baixo
    produtos_estoque_baixo = (
        db.query(func.count(Produto.id))
        .filter(Produto.quantidade <= 10)
        .scalar() or 0
    )

    # Ticket médio
    ticket_medio = 0.0
    if pedidos_info and pedidos_info.total_pedidos > 0:
        ticket_medio = float(pedidos_info.total_receita or 0) / pedidos_info.total_pedidos

    # Top produtos sem estoque
    produtos_sem_estoque = (
        db.query(Produto.id, Produto.nome, Produto.quantidade)
        .filter(Produto.quantidade <= 0)
        .limit(5)
        .all()
    )

    # Produtos mais vendidos recentemente
    from datetime import timedelta
    data_limite = datetime.utcnow() - timedelta(days=7)
    produtos_recentes = (
        db.query(
            Produto.id,
            Produto.nome,
            func.sum(PedidoItem.quantidade).label("quantidade_vendida")
        )
        .join(PedidoItem, Produto.id == PedidoItem.produto_id)
        .join(Pedido, PedidoItem.pedido_id == Pedido.id)
        .filter(Pedido.criado_em >= data_limite)
        .group_by(Produto.id, Produto.nome)
        .order_by(func.sum(PedidoItem.quantidade).desc())
        .limit(5)
        .all()
    )

    return {
        "resumo_financeiro": {
            "total_receita": float(pedidos_info.total_receita or 0),
            "total_pedidos": pedidos_info.total_pedidos or 0,
            "ticket_medio": ticket_medio
        },
        "operacional": {
            "pedidos_pendentes": pedidos_pendentes,
            "produtos_estoque_baixo": produtos_estoque_baixo
        },
        "produtos_sem_estoque": [
            {
                "id": str(p.id),
                "nome": p.nome,
                "quantidade": p.quantidade or 0
            }
            for p in produtos_sem_estoque
        ],
        "produtos_tendencia": [
            {
                "id": str(p.id),
                "nome": p.nome,
                "quantidade_vendida_7dias": int(p.quantidade_vendida or 0)
            }
            for p in produtos_recentes
        ]
    }


def get_proxima_acao(db: Session):
    """Gera sugestão de próxima melhor ação usando Gemini"""
    try:
        # Coleta dados do banco
        dados = _get_proxima_acao_data(db)
        dados_json = json.dumps(dados, ensure_ascii=False, indent=2)

        # Lê o prompt
        prompt = _read_prompt("proxima_acao.txt")

        # Chama Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{prompt}\n\nDados:\n{dados_json}",
        )

        # Converte resposta para JSON
        resultado = json_transform.convert_json(response.text)
        return resultado

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Arquivo de prompt não encontrado: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao gerar sugestão de próxima ação: {str(e)}",
        )

