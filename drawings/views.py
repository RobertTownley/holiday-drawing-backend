from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drawings.models import Drawing, DrawingOmissionRequest, Participant
from drawings.serializers import DrawingSerializer, ParticipantSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def drawings_view(request):
    drawings = Drawing.objects.all()
    data = DrawingSerializer(drawings, many=True).data
    return Response({"drawings": data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def drawing_view(request, id: str):
    drawing = Drawing.objects.get(id=id)
    data = DrawingSerializer(drawing).data
    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def participant_view(request):
    drawing = Drawing.objects.get(id=request.data["drawing_id"])
    existing_id = request.data["id"]
    created_by = request.user
    if existing_id:
        participant = Participant.objects.get(
            id=existing_id,
            created_by=created_by,
        )
        participant.name = request.data["name"]
        participant.gift_note = request.data["gift_note"]
        participant.exclusion_reason = request.data["exclusion_reason"]
        participant.save()

    elif Participant.objects.filter(
        name=request.data["name"], drawing=drawing
    ).exists():
        return Response(
            {
                "msg": "Participant already exists",
            },
            status=400,
        )
    else:
        participant, created = Participant.objects.get_or_create(
            name=request.data["name"],
            drawing=drawing,
            created_by=created_by,
            gift_note=request.data["gift_note"],
            exclusion_reason=request.data["exclusion_reason"],
        )
    DrawingOmissionRequest.objects.filter(giver=participant, drawing=drawing).delete()

    for omission_id in request.data["omissionIds"]:
        p = Participant.objects.get(id=omission_id)
        DrawingOmissionRequest.objects.get_or_create(
            drawing=drawing,
            giver=participant,
            recipient=p,
        )

    return Response(status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def omission_view(request):
    name = request.GET.get("name")
    drawing_id = request.GET.get("drawing")
    if not name or not drawing_id:
        return Response(
            {
                "omissionReason": "",
                "omissionIds": [],
            }
        )
    participant = Participant.objects.get(
        drawing_id=request.GET.get("drawing"), name=request.GET.get("name")
    )
    omissions = DrawingOmissionRequest.objects.filter(giver=participant).values_list(
        "recipient__id",
        flat=True,
    )
    return Response(
        {
            "omissionReason": participant.exclusion_reason,
            "omissionIds": list(omissions),
        }
    )
