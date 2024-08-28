import sys

import jieba
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter


class PdfRetriever:
    def __init__(self, file: str):
        loader = PyPDFLoader(file)
        self.__docs = loader.load()

        chunk_size = 250
        chunk_overlap = 30
        self.__text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.__split_docs = self.__text_splitter.split_documents(self.__docs)
        self.__retriever = BM25Retriever.from_documents(self.__split_docs, preprocess_func=self.__cut_words)

    def retrieve(self, text: str)->str:
        results = self.__retriever.invoke(text)
        result = ""
        for content in results[0:2]:
            result = result + content.page_content + "\n"
        return result

    @staticmethod
    def __cut_words(text: str):
        return jieba.lcut(text)

def main():
    retriever = PdfRetriever(file=sys.argv[1])
    question = "在汽车中，如果轮胎失压显示系统(RPA)指示轮胎压力损失，应该怎么做？"
    results = retriever.retrieve(question)
    print(type(results[0]))
    print(len(results))
    print(results)


if __name__ == "__main__":
    main()