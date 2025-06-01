import requests,math

#Parâmetros: amount / idCategory / type / difficulty
#Nota: Apenas "amount" é obrigatório, caso os demais não sejam passados, a api aleatoriza seu argumento
class Request:
    def __init__(self, amount,token):
        self.amount = amount
        self.idCategory = 0
        self.type = 0
        self.difficulty = 0
        self.token = token

        self.url = (f'https://tryvia.ptr.red/api.php'
                    f'?amount={self.amount}'
                    f'&category={self.idCategory}'
                    f'&type={self.type}'
                    f'&difficulty={self.difficulty}'
                    f'&token={self.token}')

    def set_idcategory(self, id):
        self.idCategory = id

    def set_type_of_choices(self, type):
        self.type = type

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def response(self):
        return requests.get(self.url)

    def get_Json(self):
        return self.response().json()

    def get_serialized_questions(self):
        return self.get_Json()['results']

    def get_deserialized_questions(self):
        return list(map(lambda q: Question(q),self.get_serialized_questions()))

#Desserializar uma questão: json -> objeto
class Question:
    def __init__(self, question_json):
        self.json = question_json
        self.category = self.json['category']
        self.type_of_choices = self.json['type']
        self.difficulty = self.json['difficulty']
        self.question = self.json['question']
        self.correct_answer = self.json['correct_answer']
        self.incorrect_answers = self.json['incorrect_answers']

    def get_info(self):
        console_question = f'{self.question}\n{self.correct_answer}'
        for incorrect in self.incorrect_answers:
            console_question += f'\n{incorrect}'

        return console_question

def teste(amount=1, limit_per_request = 50):
    token = requests.get('https://tryvia.ptr.red/api_token.php?command=request').json()['token']
    calls = []

    while (amount > 0):
        num_questions_per_call = min(amount, limit_per_request)
        calls.append(Request(num_questions_per_call,token).get_deserialized_questions())
        amount -= num_questions_per_call

    return calls

print(teste(201))