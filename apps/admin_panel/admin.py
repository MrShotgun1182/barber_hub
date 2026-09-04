from django.contrib import admin
from barbers.models.barber_model import BarberModel
from barbers.models.barber_service_model import BarberServiceModel
from barbers.models.working_hours_model import WorkingHoursModel
from django.contrib.auth.admin import UserAdmin
from accounts.models.user_model import UserModel


class WorkingHoursInline(admin.TabularInline):
    model = WorkingHoursModel
    extra = 0


class BarberServiceInline(admin.TabularInline):
    model = BarberServiceModel
    extra = 0


@admin.register(BarberModel)
class BarberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('user__username', 'user__phone_number')
    inlines = [WorkingHoursInline, BarberServiceInline]

@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'phone_number',
        'role',
        'is_staff',
        'is_active',
    )
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'phone_number', 'email')

    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات اختصاصی', {'fields': ('phone_number', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('اطلاعات اختصاصی', {'fields': ('phone_number', 'role')}),
    )