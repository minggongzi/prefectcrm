
from kingadmin.admin_base import BaseKingAdmin
class AdminSite(object):
    def __init__(self):
        self.enabled_admins ={}

    def register(self,model_class,admin_class=None):
        '''注册ADMIN'''
        print('register',model_class,admin_class)
        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name
        if not admin_class:#避免多个model 共享同一个BaseKingadmin
            admin_class = BaseKingAdmin()
        else:
            admin_class = admin_class()


        admin_class.model = model_class#把models_class赋值给admin_class

        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name] ={}
        self.enabled_admins[app_name][model_name] =admin_class

site = AdminSite()