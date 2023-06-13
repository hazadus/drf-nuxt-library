#
# Tests for `notes/` endpoint.
# Tests tagged "noci" are excluded when running tests in GutHub Actions (because of missing media files).
#
import json

from rest_framework import status

from books.models import Book, Note
from users.models import CustomUser

from .base_api_test_case import BaseAPITest


class NotesAPITest(BaseAPITest):
    """
    Test `notes/` DRF API endpoint.
    """

    note = None

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.note = Note.objects.create(
            user=cls.new_user,
            book=Book.objects.first(),
            text="Test note text",
        )

    def test_notes_list_without_auth_api(self):
        """
        Ensure that `NoteListView`:

        - return `HTTP_401_UNAUTHORIZED` without authorization.
        """
        url = "/api/v1/notes/"
        response = self.client.get(
            url,
        )
        authors = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_notes_list_with_auth_api(self):
        """
        Ensure that `NoteListView` with auth:

        - return `HTTP_200_OK`
        """
        url = "/api/v1/notes/"
        response = self.client.get(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )
        notes = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(notes),
            Note.objects.filter(user_id=self.new_user.pk).count(),
        )

    def test_notes_create_api(self):
        """
        Ensure that `NoteCreateView` using POST method:

        - correctly creates Note instance;
        - auth'd user set as author (using `CreateAsAuthenticatedUser` mixin);
        - returns `HTTP_201_CREATED`;

        """
        url = "/api/v1/notes/create/"
        note_text = "Test Note"
        book_instance = Book.objects.first()
        response = self.client.post(
            url,
            {
                # `user` is required, although `CreateAsAuthenticatedUser` overwrites it anyway
                "user": 1,
                "book": book_instance.pk,
                "text": note_text,
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        note_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(note_data["user"], self.new_user.pk)
        self.assertEqual(note_data["book"], book_instance.pk)
        self.assertEqual(note_data["text"], note_text)

    def test_notes_create_fails_with_wrong_data_api(self):
        """
        Ensure that `NoteCreateView` using POST method:

        - fails with incomplete data;
        - returns `HTTP_400_BAD_REQUEST`;

        """
        book_instance = Book.objects.first()
        incomplete_data = [
            {
                "user": 1,
                "book": book_instance.pk,
            },
            {
                "text": "New Note",
                "book": book_instance.pk,
            },
            {
                "user": 1,
                "text": "New Note",
            },
            {
                "user": 1,
            },
            {
                "book": book_instance.pk,
            },
            {
                "text": "New Note",
            },
        ]

        url = "/api/v1/notes/create/"

        for data in incomplete_data:
            response = self.client.post(
                url,
                data,
                **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
            )

            note_data = json.loads(response.content)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_notes_detail_get_forbidden_for_wrong_user_api(self):
        """
        Ensure that `NoteDetailView`:

        - return `HTTP_403_FORBIDDEN` when trying to GET other user's note.
        """
        note_instance = Note.objects.filter(
            user=CustomUser.objects.filter(username="hazadus").first(),
        ).first()
        url = f"/api/v1/notes/{note_instance.pk}/"

        response = self.client.get(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_notes_detail_patch_forbidden_for_wrong_user_api(self):
        """
        Ensure that `NoteDetailView`:

        - return `HTTP_403_FORBIDDEN` when trying to PATCH other user's note.
        """
        note_instance = Note.objects.filter(
            user=CustomUser.objects.filter(username="hazadus").first(),
        ).first()
        url = f"/api/v1/notes/{note_instance.pk}/"

        response = self.client.patch(
            url,
            {
                "text": "Changed note text",
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_notes_detail_delete_forbidden_for_wrong_user_api(self):
        """
        Ensure that `NoteDetailView`:

        - return `HTTP_403_FORBIDDEN` when trying to DELETE other user's note.
        """
        note_instance = Note.objects.filter(
            user=CustomUser.objects.filter(username="hazadus").first(),
        ).first()
        url = f"/api/v1/notes/{note_instance.pk}/"

        response = self.client.delete(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_notes_detail_get_api(self):
        """
        Ensure that `NoteDetailView`:

        - return `HTTP_200_OK` when trying to GET user's own note;
        - return correct data when trying to GET user's own note.
        """
        note = Note.objects.filter(user=self.new_user).first()
        url = f"/api/v1/notes/{note.pk}/"

        response = self.client.get(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        note_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(note_data["id"], note.pk)
        self.assertEqual(note_data["book"], note.book.pk)
        self.assertEqual(note_data["text"], note.text)

    def test_notes_detail_patch_api(self):
        """
        Ensure that `NoteDetailView`:

        - return `HTTP_200_OK` when trying to PATCH user's own note;
        - return correct data when trying to PATCH user's own note.
        """
        note = Note.objects.filter(user=self.new_user).first()
        updated_text = "Updated note text"
        url = f"/api/v1/notes/{note.pk}/"

        response = self.client.patch(
            url,
            {
                "text": updated_text,
            },
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        note_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(note_data["id"], note.pk)
        self.assertEqual(note_data["book"], note.book.pk)
        self.assertEqual(note_data["text"], updated_text)

    def test_notes_detail_delete_api(self):
        """
        Ensure that `NoteDetailView`:

        - return `HTTP_204_NO_CONTENT` when trying to DELETE user's own note;
        - the Note actually gets deleted from database.
        """
        note = Note.objects.create(
            user=self.new_user,
            book=Book.objects.first(),
            text="This note will be deleted soon",
        )
        note_pk = note.pk
        url = f"/api/v1/notes/{note.pk}/"

        response = self.client.delete(
            url,
            **{"HTTP_AUTHORIZATION": "Token " + self.auth_token},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.filter(pk=note_pk).count(), 0)
