#!/usr/bin/env python
# -*- encoding: utf-8 -*-



from django.db.models.query import QuerySet as BaseQueryset


class QuerySet(BaseQueryset):
    
    def nobody(self):
        # 查询已被伪删除的数据
        return self.filter(is_delete=True)
    
    def body(self):
        # 查询未被伪删除的数据
        return self.filter(is_delete=False)
    
    def fakedelete(self):
        # 伪删除
        return self.body().update(is_delete=True)
    
    def regain(self):
        # 恢复伪删除数据
        return self.nobody().update(is_delete=False)