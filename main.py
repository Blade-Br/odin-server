from fastapi import FastAPI

from schemas.inventario import InventarioSchema
from schemas.metricas import MetricasSchema


app = FastAPI(
    title="OdinServer API",
    description="API central do sistema OdinMonitor.",
    version="0.1.0"
)


@app.get("/")
def pagina_inicial():
    return {
        "mensagem": "OdinServer está em execução."
    }


@app.get("/health")
def verificar_saude():
    return {
        "status": "online"
    }


@app.post("/inventarios")
def receber_inventario(inventario: InventarioSchema):
    return {
        "mensagem": "Inventário recebido e validado com sucesso.",
        "hostname": inventario.identificacao.hostname
    }


@app.post("/metricas")
def receber_metricas(metricas: MetricasSchema):
    return {
        "mensagem": "Métricas recebidas e validadas com sucesso.",
        "timestamp": metricas.timestamp
    }
