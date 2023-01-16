from models.models import Tool


def test_new_software_tool():
    """
    GIVEN a Tool model
    WHEN a new Tool is created
    THEN check the name, link, and description fields are defined correctly
    """
    tool = Tool("Newtool", "https://newtool.com", "Decritpion")
    assert tool.name == "Newtool"
    assert tool.link == "https://newtool.com"
    assert tool.description == "Decritpion"
