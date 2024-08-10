from django.contrib import admin

class IsExpensiveFilter(admin.SimpleListFilter):
    title = 'is_expensive'
    parameter_name = 'is_expensive'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
                )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(price__gt=500)
        elif value == 'No':
            return queryset.filter(price__lt=500)
        return queryset
    



    
class IsLotFilter(admin.SimpleListFilter):
    title = 'is_lot'
    parameter_name = 'is_lot'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
                )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(order_quantity__gt=5)
        elif value == 'No':
            return queryset.filter(order_quantity__lt=5
                                   )
        return queryset