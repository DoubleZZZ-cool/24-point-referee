from itertools import permutations, product, chain, zip_longest
from fractions import Fraction

def solve(digits):
    # 将数字转换为字符串形式
    digits = list(map(str, digits))
    num_len = len(digits)
    
    # 所有数字排列组合
    digit_permutations = sorted(set(permutations(digits)))
    
    # 所有运算符的排列组合
    operator_combinations = list(product('+-*/', repeat=num_len - 1))
    
    # 括号插入位置的组合
    brackets = (
        [()] +  # 无括号的情况
        [(x, y) for x in range(0, 2*num_len-1, 2) for y in range(x+4, 2*num_len+1, 2)]
    )
    
    # 遍历所有数字和运算符组合
    for digit_perm in digit_permutations:
        for ops in operator_combinations:
            # 如果有除法，使用 Fraction 确保精确度
            if '/' in ops:
                expr_digits = [('Fraction(%s)' % d) for d in digit_perm]
            else:
                expr_digits = digit_perm
            
            # 生成基本的表达式（无括号）
            expression = list(chain.from_iterable(zip_longest(expr_digits, ops, fillvalue='')))
            
            # 遍历所有括号的组合情况
            for b in brackets:
                expr_with_brackets = expression[:]
                for insert_index, bracket in zip(b, '()' * (len(b) // 2)):
                    expr_with_brackets.insert(insert_index, bracket)
                
                expr_str = ''.join(expr_with_brackets)
                
                try:
                    # 计算表达式结果
                    result = eval(expr_str)
                except ZeroDivisionError:
                    continue  # 遇到除零错误跳过
                
                # 判断结果是否为24
                if result == 24:
                    if '/' in ops:
                        expr_with_brackets = [
                            (term if not term.startswith('Fraction(') else term[9:-1]) 
                            for term in expr_with_brackets
                        ]
                    ans = ' '.join(expr_with_brackets).rstrip()
                    print(f"Solution found: {ans}")
                    return ans
    
    # 没有找到解决方案
    print(f"No solution found for: {' '.join(digits)}")
    return None

# Test case
solve([8, 1, 3, 2])
