from app.app import registry
from app.schemas.health import HealthSchema


@registry.handles(rule='/health', method='GET', response_body_schema=HealthSchema())
def get_health():
    return {'status': 'OK'}
