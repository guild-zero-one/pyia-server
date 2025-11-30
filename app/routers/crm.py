"""CRM Routes"""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.controllers import crm_controller
from app.db.database import get_db

router = APIRouter(prefix="/crm", tags=["CRM"])


@router.get(
    "/relatorio-financeiro",
    status_code=status.HTTP_200_OK,
)
def relatorio_financeiro(
    periodo: str = Query(default="mes_atual", description="Período de análise"),
    db: Session = Depends(get_db)
):
    """Gera relatório financeiro resumido usando IA"""
    return crm_controller.get_relatorio_financeiro(db, periodo)


@router.get(
    "/alertas-reabastecimento",
    status_code=status.HTTP_200_OK,
)
def alertas_reabastecimento(
    periodo: str = Query(default="mes_atual", description="Período de análise"),
    db: Session = Depends(get_db)
):
    """Gera alertas de reabastecimento de estoque usando IA"""
    return crm_controller.get_alertas_reabastecimento(db, periodo)


@router.get(
    "/previsao-demanda",
    status_code=status.HTTP_200_OK,
)
def previsao_demanda(
    periodo: str = Query(default="mes_atual", description="Período de análise"),
    db: Session = Depends(get_db)
):
    """Gera previsão de demanda usando IA"""
    return crm_controller.get_previsao_demanda(db, periodo)


@router.get(
    "/proxima-acao",
    status_code=status.HTTP_200_OK,
)
def proxima_acao(
    periodo: str = Query(default="mes_atual", description="Período de análise"),
    db: Session = Depends(get_db)
):
    """Sugere próxima melhor ação usando IA"""
    return crm_controller.get_proxima_acao(db, periodo)

