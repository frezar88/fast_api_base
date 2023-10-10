from app.base_service.base_service import BaseService
from app.hotels.models import Hotels


class HotelsService(BaseService):
    model = Hotels
