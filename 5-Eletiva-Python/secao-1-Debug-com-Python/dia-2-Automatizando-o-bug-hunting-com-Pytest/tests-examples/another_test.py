def test_list_item_multiply(my_list):  # Recebemos a mesma fixture aqui também
    assert [item * 3 for item in my_list] == [3, 6, 9]
