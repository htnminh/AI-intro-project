import sys
sys.path.append('C:/Github repositories/AI-intro-project/')

from files.hello_world import HelloWorld

def test_names():
    assert HelloWorld().names() == {'Minh', 'Phuc', 'Nam', 'Anh', 'Phong'}
    
