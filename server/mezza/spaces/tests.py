from django.test import TestCase
from django.contrib.auth import get_user_model

from mezza.models import Space, SpaceUser, User
from mezza.spaces.operations import create_space


class CreateSpaceTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')

    def test_create_space_without_users(self):
        """Test creating a space without any users"""
        space = create_space(
            name='Test Space',
            slug='test-space'
        )

        # Verify space was created
        self.assertEqual(space.name, 'Test Space')
        self.assertEqual(space.slug, 'test-space')
        self.assertEqual(Space.objects.count(), 1)
        self.assertEqual(SpaceUser.objects.count(), 0)

    def test_create_space_with_users(self):
        """Test creating a space with associated users"""
        users = [self.user1, self.user2]
        space = create_space(
            name='Test Space',
            slug='test-space',
            users=users
        )

        # Verify space was created
        self.assertEqual(space.name, 'Test Space')
        self.assertEqual(space.slug, 'test-space')
        self.assertEqual(Space.objects.count(), 1)

        # Verify space users were created
        self.assertEqual(SpaceUser.objects.count(), 2)
        space_users = SpaceUser.objects.all()
        self.assertEqual(set(su.user for su in space_users), set(users))
        self.assertTrue(all(su.space == space for su in space_users))
