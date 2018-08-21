# -*- coding: utf-8 -*-
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

import speech_recognition as sr

# from gensim import models

import new_skill_project4_1

import jieba
from jieba import analyse

import pymongo
from pymongo import MongoClient

chatbot = ChatBot(
    "link",
    
    trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer',
    storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
    logic_adapters=[
        "chatterbot.logic.MathematicalEvaluation", #數學計算
        "chatterbot.logic.BestMatch", #匹配問題與答案
        # "chatterbot.logic.TimeLogicAdapter" #時間擺前面會有判斷錯誤，故擺後面。
    ],
    filters=['chatterbot.filters.RepetitiveResponseFilter'],
    # input_adapter="chatterbot.input.TerminalAdapter",
    # output_adapter="chatterbot.output.TerminalAdapter",
    database="chatterbot-database",
    read_only=True
)
# 1、BestMatch返回基于已知响应的输入语句最匹配的响应。
# 2、Time Logic：返回当前时间。
# 3、Mathematical Evaluation：计算数学相关问题。
# 4、Low Confidence Response：如果无法以高置信度确定响应，此适配器将返回指定的默认响应。
# 5、Specific Response：如果聊天机器人收到的输入与该适配器指定的输入文本相匹配，则返回指定的响应。

# jieba.set_dictionary('dict.txt.big')#載入自定義

# jieba.analyse.set_stop_words('user_stopwords.txt')
# jieba.load_userdict(".\dict.txt.big") 
# chatbot.set_trainer(ChatterBotCorpusTrainer)
chatbot.set_trainer(ListTrainer)
# chatbot.train("chatterbot.corpus.english")# 載入英文的語言庫

# chatbot.train(["你覺得你自己哪裡最厲害","目前我並不厲害,厲害的是你們的創造力"])



print("Type something to begin...")

# The following loop will execute each time the user enters input

while True:
    try:
        # We pass None to this method because the parameter
        # is not used by the TerminalAdapter
        keyword = input("you:")
        if "\u4E00" <= keyword <= "\u9FFF":
            jieba.load_userdict(".\dict.txt.big") 
            i = jieba.cut(str(keyword),cut_all=True)
            tags = jieba.analyse.extract_tags(str(keyword),10)
            print("split: "+"/".join(i))
            # print ("tags_Output：" + str(tags[0]))
            # print(type(tags)) 
            # keyword = ''.join(tags)
            # keyword = tags
            bot_say = new_skill_project4_1.search(keyword)
            bot_input = chatbot.get_response(keyword)
            
            if bool(bot_input) == 1 and bool(bot_say) == 1 :
                print("Bot: "+str(bot_say))
            else:
                # print(bool(bot_input))
                print("Bot: "+str(bot_input))

        elif not "\u4E00" <= keyword <= "\u9FFF":
            
            bot_say = new_skill_project4_1.search(keyword)
            bot_input = chatbot.get_response(keyword)



            if bool(bot_input) == 1 and bool(bot_say) == 1 :
                # print(type(bot_say))
                print("Bot: "+str(bot_say))
            elif bool(bot_input) == 1 and bool(bot_say) == 0 :

                # print(type(bot_input))
                print("Bot: "+str(bot_input))
                
            else:
                pass
                    
            # print("Bot: "+str(bot_input))
            # print("en_US_Bot: "+str(bot_say))

        else:
            pass#可以放其他語言

    except (KeyboardInterrupt, EOFError, SystemExit):
        break