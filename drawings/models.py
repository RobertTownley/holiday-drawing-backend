import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Drawing(BaseModel):
    year = models.IntegerField(db_index=True)

    WAITING_TO_BEGIN = "Waiting To Begin"
    GATHERING_PARTICIPANTS = "Gathering Participants"
    UNDERWAY = "Underway"
    CONCLUDED = "Concluded"

    STATUS_CHOICES = [
        (WAITING_TO_BEGIN, WAITING_TO_BEGIN),
        (GATHERING_PARTICIPANTS, GATHERING_PARTICIPANTS),
        (UNDERWAY, UNDERWAY),
        (CONCLUDED, CONCLUDED),
    ]
    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default=WAITING_TO_BEGIN
    )
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Participant(BaseModel):
    name = models.CharField(max_length=255)
    drawing = models.ForeignKey("drawings.Drawing", on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="participant_created_by"
    )
    gift_note = models.TextField(
        help_text="Description of what the recipient would like"
    )
    exclusion_reason = models.TextField(
        help_text="Reason for exclusion preferences, in case this needs to be manually overridden",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.name} {self.drawing}"


class DrawingResult(BaseModel):
    giver = models.ForeignKey(
        "drawings.Participant", on_delete=models.CASCADE, related_name="drawing_giver"
    )
    recipient = models.ForeignKey(
        "drawings.Participant",
        on_delete=models.CASCADE,
        related_name="drawing_recipient",
    )
    drawing = models.ForeignKey(
        "drawings.Drawing",
        on_delete=models.CASCADE,
        related_name="drawing_result_drawing",
    )

    def __str__(self):
        return f"{self.giver} to {self.recipient} in {self.drawing}"


class DrawingOmissionRequest(BaseModel):
    giver = models.ForeignKey(
        "drawings.Participant", on_delete=models.CASCADE, related_name="omission_giver"
    )
    recipient = models.ForeignKey(
        "drawings.Participant",
        on_delete=models.CASCADE,
        related_name="omission_recipient",
    )
    drawing = models.ForeignKey(
        "drawings.Drawing",
        on_delete=models.CASCADE,
        related_name="omission_drawing",
    )
