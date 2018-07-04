# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
import datetime
from .models import Question
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class Question_test(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        future_question = Question(pub_date = timezone.now() + datetime.timedelta(days = 30))
        self.assertIs(future_question.was_published_recently(), False)
        
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() + datetime.timedelta(days = 1, seconds = 1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)
        
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() + datetime.timedelta(minutes = 5, seconds = 59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), False)
        
def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create (question_text = question_text, pub_date = time)

class QuestionIndexTests(TestCase):

    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.") # verify that no questions appear and the Warning message is printed
        self.assertQuerysetEqual(response.context['question_list'], [])  #verify that question list is empty
        
    def past_question(self):
        past_question = create_question(question_text = 'past question', days = -30)
        response = self.client.get(reverse ('polls:index'))
        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question: past question>'])
            
    def future_question(self):
        future_question = create_question(question_text = 'future question', days = 30)
        response = self.client.get(reverse ('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['question_list'],[]
        )
    
    def past_question_and_future_question(self):
        future_question = create_question(question_text = 'future question', days = 30)
        past_question   = create_question(question_text = 'past question'  , days = -30)
        response        = self.client.get(reverse ('polls:index'))
        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question : past question>']
            )
            
    def test_two_past_questions(self):
        past_question_1 = create_question(question_text = 'past question 1', days = -30)
        past_question_2 = create_question(question_text = 'past question 2', days = -45)
        response        = self.client.get(reverse ('polls:index'))
        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question: past question 2>' , '<Question: past question 1>']
            )
            
class QuestionDetailViewTest(TestCase):
    
    def test_future_question(self):
        future_question = create_question(question_text = "future question", days = 5)
        url = reverse('polls:detail', args = (future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        past_question = create_question(question_text = "past_question", days = -4)
        url = reverse('polls:detail', args = (past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
        
        
        
        
        
    
    
        