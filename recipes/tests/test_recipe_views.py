from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def test_recipe_home_views_fuction_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shoes_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No found recipes here',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_category_views_fuction_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1000}))  # noqa: E501
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'

        # Need a recipe for this test
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipe_recipe_views_fuction_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_recipe_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1000}))  # noqa: E501
        self.assertEqual(response.status_code, 404)

    def test_recipe_recipe_template_loads_recipes(self):
        needed_title = 'This is a detail page - It load one recipe'

        # Need a recipe for this test
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)
