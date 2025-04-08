from django.test import TestCase

from mezza.auth.models import User
from .models import Workspace, WorkspaceUser
from .services import create_workspace


class CreateWorkspaceTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass123")

    def test_create_workspace_without_users(self):
        """Test creating a space without any users"""
        space = create_workspace(name="Test Workspace", slug="test-space")

        # Verify space was created
        self.assertEqual(space.name, "Test Workspace")
        self.assertEqual(workspace.slug, "test-space")
        self.assertEqual(Workspace.objects.count(), 1)
        self.assertEqual(WorkspaceUser.objects.count(), 0)

    def test_create_workspace_with_users(self):
        """Test creating a space with associated users"""
        users = [self.user1, self.user2]
        space = create_workspace(name="Test Workspace", slug="test-space", users=users)

        # Verify space was created
        self.assertEqual(space.name, "Test Workspace")
        self.assertEqual(workspace.slug, "test-space")
        self.assertEqual(Workspace.objects.count(), 1)

        # Verify space users were created
        self.assertEqual(WorkspaceUser.objects.count(), 2)
        space_users = WorkspaceUser.objects.all()
        self.assertEqual(set(su.user for su in space_users), set(users))
        self.assertTrue(all(su.space == space for su in space_users))
