from flask import Flask, jsonify, request, send_from_directory
from latex2sympy2 import *
from sympy import postorder_traversal
from DB import getList, getInfo
from mathhh import calculate, full_anonymize_variables
import logging

# Получение данных (формула, описание, файл-источник) из базы для быстрого обращения во время перебора
DB = getList()

app = Flask(__name__)

def generate_colored_latex(expr1, expr2):
    expr1 = latex2sympy(expr1)
    expr2 = latex2sympy(expr2)
    # Если выражения были уравнениями, то мы получим список уравнений, в каждом из которых выражена определённая переменная, мы обрабатываем этот случай, беря 1 элемент и перенося его левую часть вправо
    if isinstance(expr1, list):
        expr1 = expr1[0]
    if isinstance(expr2, list):
        expr2 = expr2[0]
    if str(expr1.func) == "<class 'sympy.core.relational.Equality'>":
        expr1 = expr1.rhs - expr1.lhs
    if str(expr2.func) == "<class 'sympy.core.relational.Equality'>":
        expr2 = expr2.rhs - expr2.lhs

    # Для подсветки синтаксиса мы использовали ПОЛНОСТЬЮ обезличенные переменные (не учитывая различия в именах переменных, считая a и b как одну переменную)
    expr1 = full_anonymize_variables(expr1)
    expr2 = full_anonymize_variables(expr2)

    # Получение поддеревьев
    set1 = set(postorder_traversal(expr1))
    set2 = set(postorder_traversal(expr2))
    common = set1.intersection(set2)

    latex1 = str(latex(expr1))
    latex2 = str(latex(expr2))

    # Подсветка общих поддеревьев зеленым цветом
    for i in common:
        if str(i.func) not in ["<class 'sympy.core.symbol.Symbol'>", "<class 'sympy.core.numbers.Integer'>"]:
            logging.info(f'{i}, {latex1}, {latex2}')
            latex1 = latex1.replace(str(latex(i)), r'\textcolor{green}{' + str(latex(i)) + r'}')
            latex2 = latex2.replace(str(latex(i)), r'\textcolor{green}{' + str(latex(i)) + r'}')
    return r'\textcolor{red}{' + latex1 + '}', r'\textcolor{red}{' + latex2 + '}'

# Эндпоинт инициализации
@app.route('/', methods=['GET', 'POST'])
def start():
    return send_from_directory('', 'index.html')

# Эндпоинт поиска похожих формул
@app.route('/list/', methods=["POST"])
def listserch():
    data = request.get_json()
    latex_code = data.get('latex')
    use_names = data.get('use_names')
    ans = []
    if latex_code:
        # Проход по полученной ранее базе и вычисление процентов для каждого элемента
        for i in DB:
            raw_score, score = calculate(latex_code, i[0], use_names)
            if raw_score + score:
                ans.append({"latex_code": i[0], "raw_sccore": raw_score, "score": score})

        # Сортировка результатов по проценту "смысловой" и "визуальной" схожести
        ans.sort(key=lambda x: (x["score"], x["raw_sccore"]), reverse=True)
        return jsonify({"list": ans}), 200
    return jsonify({"error": "Need 'text'"}), 400

# Эндпоинт детализации выбранной формулы
@app.route('/info/', methods=["POST"])
def info():
    base_latex = request.form.get("base_latex")
    text = request.form.get("text")

    #обращение к БД, получение детализации
    row = getInfo(text)

    if text and base_latex:
        # Получение подсвеченных LaTeX выражений
        latex1, latex2 = generate_colored_latex(base_latex, text)
        return jsonify({"LaTeX": latex2, "legend": row[1], "link": row[2]}), 200
    return jsonify({"error": "Need 'text'"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # print(check(expression1, expression2))
