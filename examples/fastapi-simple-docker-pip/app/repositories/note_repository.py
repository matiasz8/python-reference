from uuid import UUID

from app.schemas.note import NoteOut


class NoteRepository:
    def __init__(self) -> None:
        pass

    def get_note_by_id(self, note_id: UUID) -> NoteOut:
        mock_note = NoteOut(
            title="Mocked Note",
            description="This is a mocked note.",
            summary="summary",
            media_url="https://localhost",
            preview_image_url="https://localhost",
            owner_id=str(UUID("12345678-1234-5678-1234-567812345678")),
        )

        return mock_note

    def get_all_notes(self) -> list[NoteOut]:
        mock_note_list = [
            NoteOut(
                title="Mocked Note",
                description="This is a mocked note.",
                summary="summary",
                media_url="https://localhost",
                preview_image_url="https://localhost",
                owner_id=str(UUID("12345678-1234-5678-1234-567812345678")),
            ),
            NoteOut(
                title="Mocked Note",
                description="This is a mocked note.",
                summary="summary",
                media_url="https://localhost",
                preview_image_url="https://localhost",
                owner_id=str(UUID("87654321-4321-8765-4321-876543218765")),
            ),
        ]
        return mock_note_list
