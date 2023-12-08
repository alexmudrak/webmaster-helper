from api.abstract.models import AbstarctManager


class WebmasterManager(AbstarctManager):
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)
