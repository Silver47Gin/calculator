
# 顶层函数实现表达式解析
def apply_op(values, ops):
    if len(values) < 2 or not ops:
        raise ValueError("表达式错误")
    b = values.pop()
    a = values.pop()
    op = ops.pop()
    if op == '+':
        values.append(a + b)
    elif op == '-':
        values.append(a - b)
    elif op == '*':
        values.append(a * b)
    elif op == '/':
        if b == 0:
            raise ValueError("除数不能为零")
        values.append(a / b)

def greater_precedence(op1, op2):
    precedence = {'+':1, '-':1, '*':2, '/':2}
    return precedence[op1] >= precedence[op2]

def parse_expression(tokens, index):
    values = []
    ops = []
    while index < len(tokens):
        token = tokens[index]
        if isinstance(token, float):
            values.append(token)
            index += 1
        elif token in '+-*/':
            while ops and ops[-1] in '+-*/' and greater_precedence(ops[-1], token):
                apply_op(values, ops)
            ops.append(token)
            index += 1
        elif token == '(': 
            val, index = parse_expression(tokens, index + 1)
            values.append(val)
        elif token == ')':
            index += 1
            break
        else:
            raise ValueError("非法字符")
    while ops:
        apply_op(values, ops)
    if not values:
        raise ValueError("表达式无效")
    return values[0], index

def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i] in ' \t':
            i += 1
        elif expr[i] in '+-*/()':
            tokens.append(expr[i])
            i += 1
        elif expr[i].isdigit() or expr[i] == '.':
            num = ''
            dot_count = 0
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                if expr[i] == '.':
                    dot_count += 1
                    if dot_count > 1:
                        raise ValueError("数字格式错误")
                num += expr[i]
                i += 1
            tokens.append(float(num))
        else:
            raise ValueError("表达式包含非法字符！")
    return tokens

def safe_eval(expr):
    tokens = tokenize(expr)
    val, _ = parse_expression(tokens, 0)
    return val
    tokens = tokenize(expr)
    return parse(tokens)

def main():
    print("欢迎使用表达式计算器！")
    print("直接输入数学表达式，如 1+2*3 或 exit 退出。")
    while True:
        expr = input("请输入表达式: ").strip()
        if expr.lower() == "exit":
            print("再见！")
            break
        try:
            allowed_chars = "0123456789+-*/(). "
            if not all(c in allowed_chars for c in expr):
                raise ValueError("表达式包含非法字符！")
            result = safe_eval(expr)
            print(f"结果: {result}")
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
