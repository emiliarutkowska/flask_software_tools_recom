from models.models import Tool, Review


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


def test_new_review():
    """
    GIVEN a Review model
    WHEN a new Review is created
    THEN check the user_name, rating, and review_test fields are defined correctly
    """
    new_review = Review("3", "John", 4, "Very nice tool")
    assert new_review.user_name == "John"
    assert new_review.rating == 4
    assert new_review.review_text == "Very nice tool"

