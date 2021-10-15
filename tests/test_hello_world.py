from AI_intro_project.hello_world import HelloWorld

def test_names():
    assert HelloWorld().names() == {'Minh', 'Phuc', 'Nam', 'Anh', 'Phong'}, 'Test HelloWorld().names(): return enough names of 5 members'
    
