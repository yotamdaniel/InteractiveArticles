from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    max_tokens=3000,
    openai_api_key="...")  # your openai api key here

basicPrompt = PromptTemplate.from_template(
    "System: you are the author of {bookTitle}. Your goal is boil down the entire book into a single article. "
    "write a summery of {bookTitle}."
    "article length : 1000 words."
    "divide article into paragraphs based on chapters in the book or any other method that keeps the structure of the book."
    "return the article as a valid json with the key being each paragraph title and the value being the paragraph. "
)

questionsPrompt = PromptTemplate.from_template(
    "system: you are a curious reader who is trying to really understand the article. You are asking questions about the article."
    "The article is a summery of {bookTitle}."
    "article: {article}"
    "for each paragraph in the article, ask 3 questions that someone reading this for the first time might ask to fully comprehend the paragraph."
    "return the questions as a valid json with the key being each paragraph title(exactly the same as in original article) and the value being a list of questions."
)

morePrompt = PromptTemplate.from_template(
    "System: imagine you wrote a summery of {bookTitle}. \n"
    "a reader asked you 3 questions about the book: {questions}"
    "answer each question. Your answers should educate the reader. If applicable, each answers should provide concrete examples \n"
    "return the answers as a valid json with , delimiter. the key being each question and the value being the answer."
)

expandPrompt = PromptTemplate.from_template(
    "System: imagine you wrote a summery of {bookTitle}. \n"
    "write in greater details about the following paragraph of the summery: {paragraph}"
    "return the result as a valid json with the key '{title}' and the value being the expanded paragraph."
)


def generate_summary(info):
    chain = LLMChain(llm=llm, prompt=basicPrompt)
    # print(info[bookTitleItemKey])
    # print(basicPrompt.format(bookTitle=info[bookTitleItemKey]))
    # return "ok"
    return chain.run(bookTitle=info[bookTitleItemKey])


def generate_questions(info):
    # print(questionsPrompt.format(bookTitle=info[bookTitleItemKey],
    #                              article=info[articleItemKey]))
    # return "questions"
    chain = LLMChain(llm=llm, prompt=questionsPrompt)
    return chain.run(bookTitle=info[bookTitleItemKey],
                     article=info[articleItemKey])


def generate_more(title, info):
    chainExpand = LLMChain(llm=llm, prompt=expandPrompt)
    expanded = chainExpand.run(bookTitle=info[bookTitleItemKey],
                               paragraph=info[articleItemKey][title],
                               title=title)
    print(expanded)
    chainQuestions = LLMChain(llm=llm, prompt=morePrompt)
    print(title)
    print(morePrompt.format(bookTitle=info[bookTitleItemKey],
                            questions=info[questionsItemKey][title]))
    answers = chainQuestions.run(bookTitle=info[bookTitleItemKey],
                                 questions=info[questionsItemKey][title])
    return (expanded, answers)


bookTitleItemKey = "bookTitle"
articleItemKey = "article"
questionsItemKey = "questions"
