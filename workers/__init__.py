from celery import Celery

from infrastructure.config.settings import get_settings

settings = get_settings()

celery = Celery(
    "cryptonite_engine",
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BACKEND,
    include=[
        "workers.ingestion_worker",
        "workers.metrics_worker",
        "workers.graph_worker",
        "workers.contract_worker",
        "workers.market_worker",
        "workers.signal_worker",
        "workers.orchestrator_worker",
    ],
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "workers.ingestion.*": {"queue": "ingestion"},
        "workers.metrics.*": {"queue": "metrics"},
        "workers.graph.*": {"queue": "graph"},
        "workers.contract.*": {"queue": "contract"},
        "workers.market.*": {"queue": "market"},
        "workers.signal.*": {"queue": "signal"},
        "workers.orchestrator.*": {"queue": "orchestrator"},
    },
)
