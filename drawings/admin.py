from django.contrib import admin

from drawings.models import Drawing, DrawingOmissionRequest, Participant, DrawingResult


@admin.register(Drawing)
class DrawingAdmin(admin.ModelAdmin):
    pass


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    pass


@admin.register(DrawingResult)
class DrawingResultAdmin(admin.ModelAdmin):
    pass


@admin.register(DrawingOmissionRequest)
class DrawingOmissionRequestAdmin(admin.ModelAdmin):
    pass
