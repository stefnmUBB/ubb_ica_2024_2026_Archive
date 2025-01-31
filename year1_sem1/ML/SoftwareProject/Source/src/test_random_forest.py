from models.decision_tree import test_decision_tree
from models.random_forest import test_random_forest


if __name__ == "__main__":
    print("===== Test Decision Tree =====")
    test_decision_tree()
    print("===== Test Decision Tree =====\n")

    print("===== Test Random Forest =====")
    test_random_forest()
    print("===== Test Random Forest =====")
