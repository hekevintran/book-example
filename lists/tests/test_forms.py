from django.test import TestCase

from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_LIST_ERROR,
    ExistingListItemForm, ItemForm
)
from lists.models import Item, List
from unittest.mock import Mock, patch
from django.contrib.auth import get_user_model
User = get_user_model()


class ItemFormTest(TestCase):

    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())


    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR])


    def test_form_save_creates_new_item_and_parent_list(self):
        user = Mock(is_authenticated=lambda: False)
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save(owner=user)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, List.objects.first())


    @patch('lists.forms.List')
    def test_form_save_saves_owner_if_user_is_logged_in(self, mockList):
        user = User.objects.create()
        list_ = List.objects.create()
        list_.owner = None
        mockList.return_value = list_

        form = ItemForm(data={'text': 'do me'})
        form.save(owner=user)

        self.assertEqual(list_.owner, user)


    @patch('lists.forms.List')
    def test_form_save_does_not_save_owner_if_user_not_logged_in(self, mockList):
        user = Mock(is_authenticated=lambda: False)
        list_ = List.objects.create()
        list_.owner = None
        mockList.return_value = list_

        form = ItemForm(data={'text': 'do me'})
        form.save(owner=user)

        self.assertIsNone(list_.owner)




class ExistingListItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())


    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR])


    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='no twins!')
        form = ExistingListItemForm(for_list=list_, data={'text': 'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])


    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'hi'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])

