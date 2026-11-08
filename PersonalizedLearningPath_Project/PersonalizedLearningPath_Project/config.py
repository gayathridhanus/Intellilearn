COURSES = {
    "Python Fundamentals": [
        {"name": "Variables", "prerequisite": None, "difficulty": "Beginner"},
        {"name": "Data Types", "prerequisite": "Variables", "difficulty": "Beginner"},
        {"name": "Conditional Statements", "prerequisite": "Data Types", "difficulty": "Beginner"},
        {"name": "Loops", "prerequisite": "Conditional Statements", "difficulty": "Intermediate"},
        {"name": "Functions", "prerequisite": "Loops", "difficulty": "Intermediate"},
        {"name": "Lists and Dictionaries", "prerequisite": "Data Types", "difficulty": "Intermediate"},
    ],
    "Machine Learning Basics": [
        {"name": "Introduction to ML", "prerequisite": None, "difficulty": "Beginner"},
        {"name": "Data Preprocessing", "prerequisite": "Introduction to ML", "difficulty": "Beginner"},
        {"name": "Regression", "prerequisite": "Data Preprocessing", "difficulty": "Intermediate"},
        {"name": "Classification", "prerequisite": "Data Preprocessing", "difficulty": "Intermediate"},
        {"name": "Model Evaluation", "prerequisite": "Classification", "difficulty": "Intermediate"},
    ],
}
QUESTION_BANK = {
    "Variables": [("Which symbol assigns a value?", ["==", "=", "!=", ":"], 1), ("Which is a valid variable name?", ["2name", "user_name", "class", "my-name"], 1)],
    "Data Types": [("Which type stores True or False?", ["int", "str", "bool", "list"], 2), ("What is the type of 3.14?", ["int", "float", "str", "bool"], 1)],
    "Conditional Statements": [("Which keyword starts a condition?", ["for", "if", "def", "import"], 1), ("Which keyword checks another condition?", ["elif", "loop", "next", "caseof"], 0)],
    "Loops": [("Which loop iterates over a sequence?", ["if", "try", "for", "def"], 2), ("What does break do?", ["Skips one iteration", "Ends the loop", "Restarts Python", "Defines a function"], 1), ("Which loop repeats while a condition is true?", ["while", "class", "with", "return"], 0)],
    "Functions": [("Which keyword defines a function?", ["func", "function", "def", "lambda"], 2), ("Which keyword sends a value back?", ["print", "return", "yieldfrom", "pass"], 1)],
    "Lists and Dictionaries": [("Which brackets create a list?", ["{}", "()", "[]", "<>"], 2), ("A dictionary stores:", ["key-value pairs", "only values", "rows only", "characters"], 0)],
    "Introduction to ML": [("Machine learning learns patterns from:", ["Data", "Only HTML", "A monitor", "A keyboard"], 0), ("Which is supervised learning?", ["Clustering", "Classification with labels", "Compression", "Sorting"], 1)],
    "Data Preprocessing": [("A common way to handle missing numeric values is:", ["Imputation", "Ignore all rows", "Rename columns", "Increase font size"], 0), ("Why scale features?", ["Make units comparable", "Delete labels", "Create images", "Encrypt data"], 0)],
    "Regression": [("Regression commonly predicts:", ["A continuous value", "A folder", "A password", "A file type"], 0), ("Which is a regression metric?", ["MAE", "Accuracy only", "Recall only", "BLEU"], 0)],
    "Classification": [("Classification predicts:", ["A category", "A continuous value only", "A file size", "A date format"], 0), ("Which metric helps with imbalanced classes?", ["F1-score", "File size", "R-squared only", "Word count"], 0)],
    "Model Evaluation": [("A test set estimates performance on:", ["Unseen data", "Training batches only", "Passwords", "UI designs"], 0), ("AUC measures:", ["Ranking discrimination", "Database size", "Training time only", "Number of features"], 0)],
}
