from django.test import TestCase
from mezza.auth.models import User

from .models import Workspace, WorkspaceUser
from .services import create_workspace


class CreateWorkspaceTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass123")

    def test_create_workspace_without_users(self):
        """Test creating a workspace without any users"""
        workspace = create_workspace(name="Test Workspace", slug="test-workspace")

        # Verify workspace was created
        self.assertEqual(workspace.name, "Test Workspace")
        self.assertEqual(workspace.slug, "test-workspace")
        self.assertEqual(Workspace.objects.count(), 1)
        self.assertEqual(WorkspaceUser.objects.count(), 0)

    def test_create_workspace_with_users(self):
        """Test creating a workspace with associated users"""
        users = [self.user1, self.user2]
        workspace = create_workspace(
            name="Test Workspace", slug="test-space", users=users
        )

        # Verify workspace was created
        self.assertEqual(workspace.name, "Test Workspace")
        self.assertEqual(workspace.slug, "test-workspace")
        self.assertEqual(Workspace.objects.count(), 1)

        # Verify workspace users were created
        self.assertEqual(WorkspaceUser.objects.count(), 2)
        workspace_users = WorkspaceUser.objects.all()
        self.assertEqual(set(su.user for su in workspace_users), set(users))
        self.assertTrue(all(su.workspace == workspace for su in workspace_users))
