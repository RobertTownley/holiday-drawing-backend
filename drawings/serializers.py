from drawings.models import Drawing, DrawingOmissionRequest, DrawingResult, Participant
from rest_framework import serializers


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["exclusion_reason"]
        model = Participant


class DrawingResultSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["__all__"]
        model = DrawingResult


class DrawingOmissionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["__all__"]
        model = DrawingOmissionRequest


class DrawingSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    results = serializers.SerializerMethodField()

    class Meta:
        fields = "__all__"
        model = Drawing

    def get_participants(self, obj):
        participants = Participant.objects.filter(drawing_id=obj.id)
        return ParticipantSerializer(participants, many=True).data

    def get_results(self, obj):
        results = DrawingResult.objects.filter(drawing_id=obj.id)
        return DrawingResultSerializer(results, many=True).data
