class ShopRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "Shop":
            return "shop"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "Shop":
            return "shop"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == "Shop" or \
                obj2._meta.app_label == "Shop":
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == "Shop":
            return db == "shop"
        return None


class ProfileRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == "Profile":
            return "profile"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "Profile":
            return "profile"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == "Profile" or \
                obj2._meta.app_label == "Profile":
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == "Profile":
            return db == "profile"
        return None
