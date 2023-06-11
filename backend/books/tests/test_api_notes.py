#
# Tests for `notes/` endpoint.
# Tests tagged "noci" are excluded when running tests in GutHub Actions (because of missing media files).
#
import json

from rest_framework import status

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
