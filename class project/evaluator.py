from tokenizer import tokenize
from parser import parse

def evaluate(ast, environment):
    if ast["tag"] == "number":
        assert type(ast["value"]) in [float, int],f"unexpected numerical type {type(ast["value"])}"
        return ast["value"], False
    if ast["tag"] == "identifier":
        identifier = ast["value"]
        if identifier in environment:
            return environment[identifier], False
        if "$parent" in environment:
            return evaluate(ast, environment["$parent"])
        assert False, f"Unknown identifier: '{identifier}'."
    if ast["tag"] == "+":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value + right_value, False
    if ast["tag"] == "-":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value - right_value, False
    if ast["tag"] == "*":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value * right_value, False
    if ast["tag"] == "/":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        assert right_value != 0, "Division by zero"
        return left_value / right_value, False
    if ast["tag"] == "negate":
        value, _ = evaluate(ast["value"], environment)
        return -value, False
    if ast["tag"] == "&&":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value and right_value, False
    if ast["tag"] == "||":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value or right_value, False
    if ast["tag"] == "!":
        value, _ = evaluate(ast["value"], environment)
        return not value, False
    if ast["tag"] == "<":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value < right_value, False
    if ast["tag"] == ">":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value > right_value, False
    if ast["tag"] == "<=":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value <= right_value, False
    if ast["tag"] == ">=":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value >= right_value, False
    if ast["tag"] == "==":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value == right_value, False
    if ast["tag"] == "!=":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value != right_value, False
    if ast["tag"] == "print":
        if ast["value"]:
            value, _ = evaluate(ast["value"], environment)
            print(value)
        else:
            print()
        return None, False

    if ast["tag"] == "if":
        condition, _ = evaluate(ast["condition"], environment)
        if condition:
            _, _ = evaluate(ast["then"], environment)
        if "else" in ast:
            _, _ = evaluate(ast["else"], environment)
        return None, False

    if ast["tag"] == "while":
        condition, _ = evaluate(ast["condition"], environment)
        while condition:
            _, _ = evaluate(ast["do"], environment)
            condition, _ = evaluate(ast["condition"], environment)   
        return None, False
    if ast["tag"] == "=":
        assert 'target' in ast
        target = ast['target']
        assert target['tag'] == 'identifier'
        identifier = target['value']
        value, _ = evaluate(ast["value"], environment)
        environment[identifier] = value
        return None, False
    if ast["tag"] == "list":
        while ast:
            assert "statement" in ast
            _, return_chain = evaluate(ast["statement"], environment)
            ast = ast["list"]
        return None, return_chain
    assert False, "Unknown operator in AST"

def equals(code, environment, expected_result, expected_environment=None):
    result, _ = evaluate(parse(tokenize(code)), environment)
    assert (result == expected_result), f"""ERROR: When executing
    {[code]} 
    -- expected result -- 
    {[expected_result]}
    -- got --
    {[result]}."""
    if expected_environment != None:
        assert (
            environment == expected_environment
        ), f"""ERROR: When executing
        {[code]} 
        -- expected environment -- 
        {[expected_environment]}
        -- got --
        {[environment]}."""

def test_evaluate_single_value():
    print("test evaluate single value")
    equals("4",{},4,{})
    equals("3",{},3,{})
    equals("4.2",{},4.2,{})
    equals("X", {'X':1}, 1)
    equals("Y", {'X':1, 'Y':2}, 2)

def test_evaluate_addition():
    print("test evaluate addition")
    equals("1+1",{},2,{})
    equals("1+2+3",{},6,{})
    equals("1.2+2.3+3.4",{},6.9,{})
    equals("X+Y", {"X": 1, "Y": 2}, 3)

def test_evaluate_subtraction():
    print("test evaluate subtraction")
    equals("1-1",{},0,{})
    equals("3-2-1",{},0,{})

def test_evaluate_multiplication():
    print("test evaluate multiplication")
    equals("1*1",{},1,{})
    equals("3*2*2",{},12,{})
    equals("3+2*2",{},7,{})
    equals("(3+2)*2",{},10,{})

def test_evaluate_division():
    print("test evaluate division")
    equals("4/2",{},2,{})
    equals("8/4/2",{},1,{})

def test_evaluate_negation():
    print("test evaluate negation")
    equals("-2",{},-2,{})
    equals("--3",{},3,{})


def test_evaluate_print_statement():
    print("test evaluate_print_statement")
    equals("print(77)", {}, None, {})
    equals("print()", {}, None, {})
    equals("print(50+7)", {}, None, {})
    equals("print(50+8)", {}, None, {})

def test_evaluate_if_statement():
    print("testing evaluate_if_statement")
    equals("if(1) 3", {}, None, {})
    equals("if(0) 3", {}, None, {})
    equals("if(1) x=1", {"x":0}, None, {"x":1})
    equals("if(0) x=1", {"x":0}, None, {"x":0})
    # equals("if(1) 1; else 2;", {"x": 0}, None, {"x": 1})
    # equals("if(0) x=1; else x=2;", {"x": 0}, None, {"x": 2})


# def test_evaluate_while_statement():
#     print("testing evaluate_if_statement")
#     equals("if(1) 3", {}, 3, {})
#     equals("if(0) 3", {}, False, {})
#     equals("if(0) 3 else 2", {}, 2, {})
#     equals("if(0) {4;5;6} else {3;2;1}", {}, 1, {})


def test_evaluate_assignment_statement():
    print("test evaluate_assignment_statement")
    equals("X=1", {}, None, {"X": 1})
    equals("x=x+1", {"x": 1}, None, {"x": 2})
    equals("y=x+1", {"y": 1, "$parent": {"x": 3}}, None, {"y": 4, "$parent": {"x": 3}})

def test_evaluate_statement_list():
    print("test evaluate_statement_list")
    equals("1", {}, 1)
    equals("1;2;print(4);print(5);x=6;print(x)", {}, None)

if __name__ == "__main__":
    test_evaluate_single_value()
    test_evaluate_addition()
    test_evaluate_subtraction()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_evaluate_negation()
    test_evaluate_print_statement()
    test_evaluate_if_statement()
    test_evaluate_assignment_statement()
    test_evaluate_statement_list()
    print("done.")