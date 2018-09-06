import json
from datetime import datetime

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from models import Candidate
from serializers import CandidateSerializer

client = Client()

class CandidateAllTest(TestCase):
    def setUp(self):
        Candidate.objects.create(
            name = "Get Right",
            years_exp = 15,
            status = 'pending',
            date_applied = datetime(2018, 07, 03, 12, 55, 42),
            reviewed = False,
            description = "Enjoys being the best"
        )

        Candidate.objects.create(
            name = "Ice Frog",
            years_exp = 17,
            status = 'Accepted',
            date_applied = datetime(2018, 02, 03, 12, 55, 42),
            reviewed = False,
            description = "Balances everything in life"
        )

        Candidate.objects.create(
            name = "Forest",
            years_exp = 5,
            status = 'pending',
            date_applied = datetime(2018, 04, 03, 12, 55, 42),
            reviewed = False,
            description = "Can do things, many things."
        )

        Candidate.objects.create(
            name = "Pobelter",
            years_exp = 7,
            status = 'Rejected',
            date_applied = datetime(2018, 05, 03, 12, 55, 42),
            reviewed = True,
            description = "Stuck in the middle with you"
        )

    def test_get(self):
        response = client.get(reverse('candidate-list'))
        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSingleCandidate(TestCase):
    """ Test module for GET single Candidate """

    def setUp(self):
        self.john = Candidate.objects.create(
            name = "John Cena",
            years_exp = 15,
            status = 'pending',
            date_applied = datetime(2018, 07, 03, 12, 55, 42),
            reviewed = False,
            description = "Enjoys being invisibile"
        )

        self.alfred = Candidate.objects.create(
            name = "Alfred Abitha",
            years_exp = 17,
            status = 'Accepted',
            date_applied = datetime(2018, 02, 03, 12, 55, 42),
            reviewed = False,
            description = "Spends his free time learning to fish with his hands"
        )

        self.david = Candidate.objects.create(
            name = "David McClean",
            years_exp = 5,
            status = 'pending',
            date_applied = datetime(2018, 04, 03, 12, 55, 42),
            reviewed = False,
            description = "Once ran from Ohio to Arizona, and forgot why he did it"
        )

        self.cassy = Candidate.objects.create(
            name = "Cassy DaVidino",
            years_exp = 7,
            status = 'Rejected',
            date_applied = datetime(2018, 05, 03, 12, 55, 42),
            reviewed = True,
            description = "Can throw a football 530 yards"
        )

    def test_get_valid_single_candidate(self):
        response = client.get(
            reverse('candidate-detail', kwargs={'pk': self.david.pk}))
        candidate = Candidate.objects.get(pk=self.david.pk)
        serializer = CandidateSerializer(candidate)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_candidate(self):
        response = client.get(
            reverse('candidate-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateNewCandidateTest(TestCase):
    """ Test module for inserting a new candidate """

    def setUp(self):
        self.valid_payload = {
            'name' : "Shroud",
            'years_exp' : 8,
            'status' : 'pending',
            'date_applied' : '2018-07-02T09:55:42Z',
            'reviewed' : True,
            'description' : "Really good vision"
        }
        self.invalid_payload = {
            'name' : "",
            'years_exp' : 7,
            'status' : 'Rejected',
            'date_applied' : '2018-06-05T09:55:42Z',
            'reviewed' : True,
            'description' : "Really good at running"
        }

    def test_create_valid_candidate(self):
        response = client.post(
            reverse('candidate-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_candidate(self):
        response = client.post(
            reverse('candidate-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSingleCandidate(TestCase):
    """ Test module for updating an existing candidate """

    def setUp(self):
        self.toasty = Candidate.objects.create(
            name='Toasty', years_exp=4, status='pending', date_applied=datetime(2018, 02, 03, 12, 55, 42), reviewed=False, description="Lives in a house")
        self.danger = Candidate.objects.create(
            name='Danger', years_exp=1, status='accepted', date_applied=datetime(2018, 05, 03, 12, 55, 42), reviewed=False, description="high speed")
        self.valid_payload = {
            'name' : "Shroud",
            'years_exp' : 8,
            'status' : 'pending',
            'date_applied' : '2018-07-02T09:55:42Z',
            'reviewed' : True,
            'description' : "Really good vision"
        }
        self.invalid_payload = {
            'name' : "",
            'years_exp' : 7,
            'status' : 'Rejected',
            'date_applied' : '2018-06-05T09:55:42Z',
            'reviewed' : True,
            'description' : "Really good at running"
        }

    def test_valid_update_candidate(self):
        response = client.put(
            reverse('candidate-detail', kwargs={'pk': self.danger.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_candidate(self):
        response = client.put(
            reverse('candidate-detail', kwargs={'pk' : self.danger.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSingleCandidateTest(TestCase):
    """ Test module for deleting an existing candidate record """

    def setUp(self):
        self.toasty = Candidate.objects.create(
            name='Toasty', years_exp=4, status='pending', date_applied=datetime(2018, 02, 03, 12, 55, 42), reviewed=False, description="Lives in a house")
        self.danger = Candidate.objects.create(
            name='Danger', years_exp=1, status='accepted', date_applied=datetime(2018, 05, 03, 12, 55, 42), reviewed=False, description="high speed")

    def test_valid_delete_candidate(self):
        response = client.delete(
            reverse('candidate-detail', kwargs={'pk': self.toasty.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_candidate(self):
        response = client.delete(
            reverse('candidate-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UpdateStatusCandidate(TestCase):
    """ Test module for updating an existing candidate """

    def setUp(self):
        self.shroud = Candidate.objects.create(
            name='Shroud', years_exp=4, status='pending', date_applied=datetime(2018, 02, 03, 12, 55, 42), reviewed=False, description="Lives in a house")
        self.danger = Candidate.objects.create(
            name='Danger', years_exp=15, status='accepted', date_applied=datetime(2018, 05, 03, 12, 55, 42), reviewed=False, description="Really good at running")
        self.valid_payload = {
            'name' : "Shroud",
            'years_exp' : 4,
            'status' : 'accepted',
            'date_applied' : '2018-07-02T09:55:42Z',
            'description' : "Lives in a house"
        }
        self.invalid_payload = {
            'name' : "Danger",
            'years_exp' : 15,
            'status' : 'Rejected',
            'date_applied' : '2018-06-05T09:55:42Z',
            'description' : "Really good at running"
        }

    def test_valid_status_update(self):
        response = client.put(
            reverse('candidate-detail', kwargs={'pk': self.shroud.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_status_update(self):
        response = client.put(
            reverse('candidate-detail', kwargs={'pk' : self.danger.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateYearsExpTest(TestCase):
    """ Test module for updating an existing candidate """

    def setUp(self):
        self.shroud = Candidate.objects.create(
            name='Shroud', years_exp=4, status='pending', date_applied=datetime(2018, 02, 03, 12, 55, 42), reviewed=False, description="Lives in a house")
        self.danger = Candidate.objects.create(
            name='Danger', years_exp=15, status='accepted', date_applied=datetime(2018, 05, 03, 12, 55, 42), reviewed=False, description="Really good at running")
        self.valid_payload = {
            'name' : "Shroud",
            'years_exp' : 43,
            'status' : 'accepted',
            'date_applied' : '2018-07-02T09:55:42Z',
            'description' : "Lives in a house"
        }
        self.invalid_payload = {
            'name' : "Danger",
            'years_exp' : 55,
            'status' : 'Rejected',
            'date_applied' : '2018-06-05T09:55:42Z',
            'description' : "Really good at running"
        }

    def test_valid_years_exp_update(self):
        response = client.put(
            reverse('candidate-detail', kwargs={'pk': self.shroud.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_years_exp_update(self):
        response = client.put(
            reverse('candidate-detail', kwargs={'pk' : self.danger.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)