import os,sys

class A(object):

    path=""
    def __init__(self,word_for_train,train_output,path):
        self.jump="jump"
        self.run="rum"
        self.word_for_train=word_for_train
        self.train_output=train_output
        self.path=path


    def import_data(self,path):
        path=""
        return path

    def normal_method(self,test_for_method,*args,**kwargs):
        print("we have multiple variables"+format(*args,**kwargs))

    @classmethod
    def class_method(cls, x=1, **kwargs):
        return cls(x)

    @staticmethod
    def Static_function():
        print("this is an staticfunction")
