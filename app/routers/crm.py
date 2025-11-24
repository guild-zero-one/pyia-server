"""CRM Routes"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers import crm_controller
from app.db.database import get_db

router = APIRouter(prefix="/crm", tags=["CRM"])


@router.get(
    "/relatorio-financeiro",
    status_code=status.HTTP_200_OK,
)
def relatorio_financeiro(db: Session = Depends(get_db)):
    """Gera relatório financeiro resumido usando IA"""
    return crm_controller.get_relatorio_financeiro(db)


@router.get(
    "/alertas-reabastecimento",
    status_code=status.HTTP_200_OK,
)
def alertas_reabastecimento(db: Session = Depends(get_db)):
    """Gera alertas de reabastecimento de estoque usando IA"""
    return crm_controller.get_alertas_reabastecimento(db)


@router.get(
    "/previsao-demanda",
    status_code=status.HTTP_200_OK,
)
def previsao_demanda(db: Session = Depends(get_db)):
    """Gera previsão de demanda usando IA"""
    return crm_controller.get_previsao_demanda(db)


@router.get(
    "/proxima-acao",
    status_code=status.HTTP_200_OK,
)
def proxima_acao(db: Session = Depends(get_db)):
    """Sugere próxima melhor ação usando IA"""
    return crm_controller.get_proxima_acao(db)

