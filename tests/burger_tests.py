import pytest
from unittest.mock import Mock
from praktikum.burger import Burger

class TestBurger:

    def setup_method(self):
        self.burger = Burger()

    def test_set_buns(self):
        mock_bun = Mock()

        self.burger.set_buns(mock_bun)

        assert self.burger.bun == mock_bun

    def test_add_ingredient(self):
        mock_ingredient = Mock()

        self.burger.add_ingredient(mock_ingredient)

        assert len(self.burger.ingredients) == 1 and self.burger.ingredients[0] == mock_ingredient

    def test_remove_ingredient(self):
        mock_ingredient = Mock()

        self.burger.add_ingredient(mock_ingredient)

        self.burger.remove_ingredient(0)

        assert len(self.burger.ingredients) == 0

    def test_move_ingredient_from_end_to_begining(self):
        mock_ingredient1 = Mock()
        mock_ingredient2 = Mock()
        mock_ingredient3 = Mock()

        self.burger.add_ingredient(mock_ingredient1)
        self.burger.add_ingredient(mock_ingredient2)
        self.burger.add_ingredient(mock_ingredient3)

        self.burger.move_ingredient(2,0)

        assert self.burger.ingredients == [mock_ingredient3, mock_ingredient1, mock_ingredient2]

    def test_move_ingredient_from_begining_to_end(self):
        mock_ingredient1 = Mock()
        mock_ingredient2 = Mock()
        mock_ingredient3 = Mock()

        self.burger.add_ingredient(mock_ingredient1)
        self.burger.add_ingredient(mock_ingredient2)
        self.burger.add_ingredient(mock_ingredient3)

        self.burger.move_ingredient(0,2)

        assert self.burger.ingredients == [mock_ingredient2, mock_ingredient3, mock_ingredient1]

    @pytest.mark.parametrize("bun_price, ingredient_price, expected_result", [
        (100, [], 200),
        (200, [100], 500),
        (300, [200, 200], 1000),
        (100, [100, 200, 300], 800),
        (200, [200, 100, 300, 100, 200, 300], 1600),
        (300, [0], 600),
        (200, [0, 0, 0], 400),
    ])
    def test_get_price_for_different_valid_values(self, bun_price, ingredient_price, expected_result):
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        self.burger.set_buns(mock_bun)

        for price in ingredient_price:
            mock_ingredient = Mock()
            mock_ingredient.get_price.return_value = price
            self.burger.add_ingredient(mock_ingredient)

        assert self.burger.get_price() == expected_result

    
    def test_get_price_with_none_bun_price(self):
        mock_bun = Mock()
        mock_bun.get_price.return_value = None
        self.burger.set_buns(mock_bun)
    
        mock_ingredient = Mock()
        mock_ingredient.get_price.return_value = 100
        self.burger.add_ingredient(mock_ingredient)
    
        with pytest.raises(TypeError):
            self.burger.get_price()

    def test_get_price_with_none_ingredient_price(self):
        mock_bun = Mock()
        mock_bun.get_price.return_value = 200
        self.burger.set_buns(mock_bun)
    
        mock_ingredient = Mock()
        mock_ingredient.get_price.return_value = None
        self.burger.add_ingredient(mock_ingredient)
    
        with pytest.raises(TypeError):
            self.burger.get_price()

    def test_get_price_with_ingredients_set_to_none(self):
        mock_bun = Mock()
        mock_bun.get_price.return_value = 200
        self.burger.set_buns(mock_bun)
        self.burger.ingredients = None
    
        with pytest.raises(TypeError):
            self.burger.get_price()

    def test_get_price_with_all_none(self):
        mock_bun = Mock()
        mock_bun.get_price.return_value = None
        self.burger.set_buns(mock_bun)
        self.burger.ingredients.append(None)
    
        with pytest.raises(TypeError):
            self.burger.get_price()

    @pytest.mark.parametrize("bun_name, bun_price, ingredients_data, expected_result", [
        (
            "black bun", 100,
            [], 
            "(==== black bun ====)\n"
            "(==== black bun ====)\n"
            "\n"
            "Price: 200"
        ),
        (
            "red bun", 300,
            [("SAUCE", "hot sauce", 100)],
            "(==== red bun ====)\n"
            "= sauce hot sauce =\n"
            "(==== red bun ====)\n"
            "\n"
            "Price: 700"
        ),
        (
        "white bun", 200,
        [("SAUCE", "chili sauce", 300), ("FILLING", "cutlet", 100)],
        "(==== white bun ====)\n"
        "= sauce chili sauce =\n"
        "= filling cutlet =\n"
        "(==== white bun ====)\n"
        "\n"
        "Price: 800"
        ),
        (
        "black bun", 100,
        [
            ("SAUCE", "hot sauce", 100),
            ("SAUCE", "sour cream", 200),
            ("FILLING", "cutlet", 100),
            ("FILLING", "dinosaur", 200),
        ],
        "(==== black bun ====)\n"
        "= sauce hot sauce =\n"
        "= sauce sour cream =\n"
        "= filling cutlet =\n"
        "= filling dinosaur =\n"
        "(==== black bun ====)\n"
        "\n"
        "Price: 800"
    )
    ])
    def test_get_receipt(self, bun_name, bun_price, ingredients_data, expected_result):
        mock_bun = Mock()
        mock_bun.get_name.return_value = bun_name
        mock_bun.get_price.return_value = bun_price 
        self.burger.set_buns(mock_bun)
    
        for i_type, i_name, i_price in ingredients_data:
            mock_ingredient = Mock()
            mock_ingredient.get_type.return_value = i_type
            mock_ingredient.get_name.return_value = i_name
            mock_ingredient.get_price.return_value = i_price
            self.burger.add_ingredient(mock_ingredient)
    
        assert self.burger.get_receipt() == expected_result