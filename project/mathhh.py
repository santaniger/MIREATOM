from itertools import permutations
from sympy import Symbol, Add, Mul, Pow, preorder_traversal, sympify, simplify, expand
from multiset import Multiset
from functools import lru_cache
from sys import setrecursionlimit
from latex2sympy2 import latex2sympy

# Увеличение лимита рекурсии, для рекурсивной анонимизации переменных
setrecursionlimit(10000)

@lru_cache(maxsize=None)
def anonymize_variables(expr):
    variables = list(expr.free_symbols)
    anon_exprs = []
    for permutation in set(permutations(variables)):
        # Исходя из особенностей библиотеки sympy, иногда мы мжем получить неопределённое поведение при замене переменных, к примеру:
        # a - b может быть интерпритированно как a - b или -b + a
        # для предотвращения ошибок в вычислении схожести, создаём все возможные перестановки переменных
        new_variables = [Symbol(f'var{i}') for i in range(len(permutation))]
        substitution_dict = dict(zip(permutation, new_variables))

        #Проходим по дереву, заменяя вершины с переменными, на их анонимизированные аналоги
        def replace_variables(node):
            if node.is_Symbol:
                return substitution_dict[node]
            elif isinstance(node, Add):
                return Add(*[replace_variables(arg) for arg in node.args], evaluate=False)
            elif isinstance(node, Mul):
                return Mul(*[replace_variables(arg) for arg in node.args], evaluate=False)
            elif isinstance(node, Pow):
                return Pow(replace_variables(node.base), replace_variables(node.exp), evaluate=False)
            else:
                return node

        new_expr = replace_variables(expr)
        anon_exprs.append(new_expr)
    return anon_exprs

@lru_cache(maxsize=None)
def full_anonymize_variables(expr):
    """
    Действует аналогично предидущей, но заменяя все переменные на 1 шаблон - x
    """
    variables = list(expr.free_symbols)
    new_variables = [Symbol(f'x') for i in range(len(variables))]
    substitution_dict = dict(zip(variables, new_variables))

    def replace_variables(node):
        if node.is_Symbol:
            return substitution_dict[node]
        elif isinstance(node, Add):
            return Add(*[replace_variables(arg) for arg in node.args], evaluate=False)
        elif isinstance(node, Mul):
            return Mul(*[replace_variables(arg) for arg in node.args], evaluate=False)
        elif isinstance(node, Pow):
            return Pow(replace_variables(node.base), replace_variables(node.exp), evaluate=False)
        else:
            return node

    new_expr = replace_variables(expr)
    return new_expr

@lru_cache(maxsize=None)
def calculate_similarity(expr1, expr2, use_names):
    # Проверка состояния переключателя учёта переменных
    if not use_names:
        expr1 = anonymize_variables(expr1)
        expr2 = anonymize_variables(expr2)
    else:
        expr1 = {expr1}
        expr2 = {expr2}

    flag = 1
    percent = 0
    for now_anon_expr1 in expr1:
        for now_anon_expr2 in expr2:
            # Проходим по дереву, принимая за корень дерева каждую из вершин, компилируя и добавляя в множество с повторениями
            set1 = Multiset(preorder_traversal(now_anon_expr1))
            set2 = Multiset(preorder_traversal(now_anon_expr2))
            # Подсчёт количества таких поддеревьем в двух сравниваемых деревьях (без учёта одиночных переменных)
            lenfull = sum(1 for i in set1 if str(i.func) != "<class 'sympy.core.symbol.Symbol'>")
            lenfull += sum(1 for i in set2 if str(i.func) != "<class 'sympy.core.symbol.Symbol'>")
            # Подсчёт количества схожих деревьев (без учёта одиночных переменных)
            lenset = sum(1 for i in set1.intersection(set2) if str(i.func) != "<class 'sympy.core.symbol.Symbol'>")
            if flag:
                percent = int(lenset / lenfull * 200)
                flag -= 1
            # Подсчёт коэффициента, схожего с коэффициентом Жаккара для двух деревьев (количество схожих поддеревьев, делённое на количество всех поддеревьев)
            if percent != int(lenset / lenfull * 200):
                return max(percent, int(lenset / lenfull * 200))
            percent = int(lenset / lenfull * 200)
    return percent

def calculate(expr1, expr2, use_names):
    """
    Основная функция для вычисления сходства между двумя выражениями
    """
    expr1 = latex2sympy(expr1)
    expr2 = latex2sympy(expr2)
    expr1 = sympify(expr1, evaluate=False)
    expr2 = sympify(expr2, evaluate=False)

    # Аналогично с main.py: Если выражения были уравнениями, то мы получим список уравнений,
    # в каждом из которых выражена определённая переменная, мы обрабатываем этот случай, беря 1 элемент и перенося его левую часть вправо
    if isinstance(expr1, list):
        expr1 = expr1[0]
    if isinstance(expr2, list):
        expr2 = expr2[0]
    # Процент визуальной схожести
    max_percent = calculate_similarity(expr1, expr2, use_names)

    # Продолжение обработки уравнений. Если текущее выражение - не уравнение, то проверяем смысловую эквивалентность
    if str(expr1.func) != "<class 'sympy.core.relational.Equality'>" and str(expr2.func) != "<class 'sympy.core.relational.Equality'>":
        if expr1.equals(expr2):
            # Если выражения эквивалентны, то процент их схожести = 100%
            max_simple_percent1 = 100
            max_simple_percent2 = 100
        else:
            # Иначе - процент равен максимуму сравнения в упрощённой и элементарной формах
            max_simple_percent1 = calculate_similarity(simplify(expr1), simplify(expr2), use_names)
            max_simple_percent2 = calculate_similarity(expand(expr1), expand(expr2), use_names)
        return max_percent, max(max_simple_percent1, max_simple_percent2)
    else:
        # Если это уравнение, то переносим в одну сторону и сравниваем без пребразований
        if str(expr1.func) == "<class 'sympy.core.relational.Equality'>":
            expr1 = expr1.rhs - expr1.lhs
        if str(expr2.func) == "<class 'sympy.core.relational.Equality'>":
            expr2 = expr2.rhs - expr2.lhs
        max_simple_percent1 = calculate_similarity(simplify(expr1), simplify(expr2), use_names)
        max_simple_percent2 = calculate_similarity(expand(expr1), expand(expr2), use_names)
    return max_percent, max(max_simple_percent1, max_simple_percent2)
