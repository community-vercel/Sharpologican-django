class EspanRouter:
    """
    A router to control all database operations on models in the
    Espan application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'Espan':
            return 'Espan'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'Espan':
            return 'Espan'
        return None


class FranceRouter:
    """
    A router to control all database operations on models in the
    France application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'France':
            return 'France'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'France':
            return 'France'
        return None


class NetherlandsRouter:
    """
    A router to control all database operations on models in the
    Netherlands application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'Netherlands':
            return 'Netherlands'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'Netherlands':
            return 'Netherlands'
        return None