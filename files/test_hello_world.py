from hello_world import HelloWorld

def test_names():
    assert HelloWorld().names() == {'Minh', 'Phuc', 'Nam', 'Anh', 'Phong'}

