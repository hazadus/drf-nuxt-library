#
# Tests for `notes/` endpoint.
# Tests tagged "noci" are excluded when running tests in GutHub Actions (because of missing media files).
#
import json

from rest_framework import status

from books.models import Book

from .base_api_test_case import BaseAPITest


class NotesAPITest(BaseAPITest):
    """
    Test `notes/` DRF API endpoint.
    """

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
        authors = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
