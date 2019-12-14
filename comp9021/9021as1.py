import re
import itertools
import sys
from functools import reduce 

try:
    text_name = input('Which text file do you want to use for the puzzle?')
    f = open(text_name)
except FileNotFoundError:
    print('please enter right file name.')
    sys.exit()

#stage 1 extra all names in the puzzle
capital_word = ['Knight', 'Knave', 'Knaves', 'Knights', 'Sir', 'Sirs', 'I']#some captial words
text_name = f.read().replace('\n', ' ').replace('"', '').replace(',', '')
sentence_name = re.split(r'[.?!]', text_name)#split sentence according to .!?
del(sentence_name[-1])
name_list = []
for each_line in sentence_name:
    temp = each_line.split()
    del(temp[0])#delete the first captial word
    for word in temp:
        if word.istitle() == True and word not in capital_word and word not in name_list:
            name_list.append(word)
name_list.sort()
name_phrase = ''
for each_name in name_list:
    name_phrase+= ' ' + each_name
print(f'The Sirs are:{name_phrase}')
#stage 2 extra useful sentene from the whole paragraph
f.seek(0, 0)#read again
talking = {}
sentence_with_talking = []
name_talking = ''
text_talking = f.read().replace('\n', ' ')
talking_content = re.findall(r'"(.*?)"', text_talking.replace('.', '').replace('!', '').replace('?', '').replace(',', ''))#extra sentence between double quotes
talking_content1 = talking_content[:]
sentence_talking = [each for each in re.split(r"[!.?]\s*", text_talking.replace('"', '').replace(',', ''))]#split sentence according to .!?
for i, each_line in enumerate(talking_content):
    if talking_content.count(each_line) > 1:
        talking_content[i] = each_line + ' ' + str(i)#to handle the situation that different person say same sentence 
for string in sentence_talking:
    if any(sub in string for sub in talking_content):
        sentence_with_talking.append(string)
zip_1 = zip(sentence_with_talking, talking_content1)# to handle the situation that one person says several sentences
name = []
for i, j in zip_1:
    temp = i.replace(j, '').split()
    del(temp[0])
    for word in temp:
        if word.istitle() == True and word not in capital_word:#to extra all names in sentence
            name.append(word)
zip_2 = zip(talking_content, name)
for i, j in zip_2:
    talking[i] = j#match speakers with their talking sentences
def initial():#initialize the person ID, means can be 0(kanve) or 1(knight)
    for each_name in name_list:
        solution[each_name] = (0,1)
# all possible sentence forms in double quotes
form_1 = 'least one of is a knight'.split()
form_2 = 'least one of is a knave'.split()
form_3 = 'most one of is a knight'.split()
form_4 = 'most one of is a knave'.split()
form_5 = 'exactly one of is a knight'.split()
form_6 = 'exactly one of is a knave'.split()
form_7 = 'all of us are knights'.split()
form_8 = 'all of us are knaves'.split()
form_9 = 'i am a knight'.split()
form_10 = 'i am a knave'.split()#impossiple
form_11 = 'sir is a knight'.split()
form_12 = 'sir is a knave'.split()
form_13 = 'or is a knight'.split()#same as at least one knight!!!!!!
form_14 = 'or is a knave'.split()#same as at least one knave!!!!!!
form_15 = 'and are knights'.split()
form_16 = 'and are knaves'.split()
#stage 3 identify
final_result = []
for each in talking.items():
    #get all names in each sentence 
    #new_name_list (people in the talking sentence), each[0] means speaker, each[1] means talking sentence
    new_name_list = []
    if 'us' in each[0]:# us means including all person
        new_name_list = name_list[:]
    else:
        temp = each[0].split()
        del(temp[0])#delete useless captial words
        for each_word in temp:
            if each_word.istitle() == True and each_word not in capital_word and each_word not in new_name_list:
                new_name_list.append(each_word)
    if each[1] in new_name_list:
            new_name_list.remove(each[1])
    #initalize the person and their possible ID:(1 means Knight/0 means  Knave)
    solution = {}
    result = []
    for each_name in name_list:
        solution[each_name] = (0,1)
    #check whether the sentence is same as the form
    word_talking_content = each[0].lower().split()
    if not ['_' for temp in form_1 if temp not in word_talking_content]:#determine which sentence form
        if 'I' in each[0] or each[1] in each[0] or 'us' in each[0]:#some special conditions, the sentence include 'I', 'us' and the speaker
            solution[each[1]] = (1,)#condition 1: the speaker is knight and tell the truth
            result.append(set(itertools.product(*solution.values())))#throught'product' get all possilbe solutions
            solution[each[1]] = (0,)#condition 2 : the speaker is knave and lie
            for each_name in new_name_list:
                solution[each_name] = (0,)
            result.append(set(itertools.product(*solution.values())))
        else:
            solution[each[1]] = (1,)
            temp_1_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (0,)
            result.append(temp_1_set - set(itertools.product(*solution.values())))
            initial()#initialize all person condition into (0,1) means can be truth or lies, as other person condition has changde above
            solution[each[1]] = (0,)
            for each_name in new_name_list:
                solution[each_name] = (0,)
            result.append(set(itertools.product(*solution.values())))
        final_result.append(reduce(lambda x,y : x | y, result))#combine all possible solutions
    elif not ['_' for temp in form_2 if temp not in word_talking_content]:#different form and have similiar processes
        if 'I' in each[0] or each[1] in each[0] or 'us' in each[0]:
            solution[each[1]] = (1,)
            temp_1_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (1,)
            result.append(temp_1_set - set(itertools.product(*solution.values())))
        else:
            solution[each[1]] = (1,)
            temp_1_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (1,)
            result.append(temp_1_set - set(itertools.product(*solution.values())))
            initial()
            solution[each[1]] = (0,)
            for each_name in new_name_list:
                solution[each_name] = (1,)
            result.append(set(itertools.product(*solution.values())))
        final_result.append(reduce(lambda x,y : x | y, result))
    elif not ['_' for temp in form_3 if temp not in word_talking_content]:#different form and have similiar processes
        if 'I' in each[0] or each[1] in each[0] or 'us' in each[0]:
            solution[each[1]] = (1,)
            for each_name in new_name_list:
                solution[each_name] = (0,)
            result.append(set(itertools.product(*solution.values())))
            initial()
            solution[each[1]] = (0,)
            temp_0_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (0,)
            temp_0_set -= set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (1,)
                temp_0_set -= set(itertools.product(*solution.values()))
                solution[each_name] = (0,)
            result.append(temp_0_set)
        else:
            solution[each[1]] = (1,)
            for each_name in new_name_list:
                solution[each_name] = (0,)
            result.append(set(itertools.product(*solution.values())))
            for each_name in new_name_list:
                solution[each_name] = (1,)
                result.append(set(itertools.product(*solution.values())))
                solution[each_name] = (0,)
            initial()
            solution[each[1]] = (0,)
            temp_0_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (0,)
            temp_0_set -= set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (1,)
                temp_0_set -= set(itertools.product(*solution.values()))
                solution[each_name] = (0,)
            result.append(temp_0_set)
        final_result.append(reduce(lambda x,y : x | y, result))
    elif not ['_' for temp in form_4 if temp not in word_talking_content]:#different form and have similiar processes
        if 'I' in each[0] or each[1] in each[0] or 'us' in each[0]:
            solution[each[1]] = (1,)
            for each_name in new_name_list:
                solution[each_name] = (1,)
            result.append(set(itertools.product(*solution.values())))
            for each_name in new_name_list:
                solution[each_name] = (0,)
                result.append(set(itertools.product(*solution.values())))
                solution[each_name] = (1,)
            initial()
            solution[each[1]] = (0,)
            temp_0_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (1,)
            result.append(temp_0_set - set(itertools.product(*solution.values())))
        else:
            solution[each[1]] = (1,)
            for each_name in new_name_list:
                solution[each_name] = (1,)
            result.append(set(itertools.product(*solution.values())))
            for each_name in new_name_list:
                solution[each_name] = (0,)
                result.append(set(itertools.product(*solution.values())))
                solution[each_name] = (1,)
            initial()
            solution[each[1]] = (0,)
            temp_0_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (1,)
            result.append(temp_0_set - set(itertools.product(*solution.values())))
        final_result.append(reduce(lambda x,y : x | y, result))
    elif not ['_' for temp in form_5 if temp not in word_talking_content]:#different form and have similiar processes
        if 'I' in each[0] or each[1] in each[0] or 'us' in each[0]:
            solution[each[1]] = (1,)
            for each_name in new_name_list:
                solution[each_name] = (0,)
            result.append(set(itertools.product(*solution.values())))
            initial()
            solution[each[1]] = (0,)
            temp_0_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (0,)
            for each_name in new_name_list:
                solution[each_name] = (1,)
                temp_0_set -= set(itertools.product(*solution.values()))
                solution[each_name] = (0,)
            result.append(temp_0_set)
        else:
            solution[each[1]] = (1,)
            for each_name in new_name_list:
                solution[each_name] = (0,)
            for each_name in new_name_list:
                solution[each_name_1] = (1,)
                append(set(itertools.product(*solution.values())))
                solution[each_name] = (0,)
            initial()
            solution[each[1]] = (0,)
            temp_0_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (0,)
            for each_name in new_name_list:
                solution[each_name_1] = (1,)
                temp_0_set -= set(itertools.product(*solution.values()))
                solution[each_name] = (0,)
            result.append(temp_0_set)
        final_result.append(reduce(lambda x,y : x | y, result))
    elif not ['_' for temp in form_6 if temp not in word_talking_content]:#different form and have similiar processes
        if 'I' in each[0] or each[1] in each[0] or 'us' in each[0]:
            solution[each[1]] = (1,)
            for each_name in new_name_list:
                solution[each_name] = (1,)
            for each_name in new_name_list:
                solution[each_name] = (0,)
                result.append(set(itertools.product(*solution.values())))
                solution[each_name] = (1,)
            initial()
            solution[each[1]] = (0,)
            temp_0_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (1,)
            result.append(temp_0_set - set(itertools.product(*solution.values())))
        else:
            solution[each[1]] = (1,)
            for each_name in new_name_list:
                solution[each_name] = (1,)
            for each_name in new_name_list:
                solution[each_name] = (0,)
                result.append(set(itertools.product(*solution.values())))
                solution[each_name] = (1,)
            initial()
            solution[each[1]] = (0,)
            temp_0_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (1,)
            for each_name in new_name_list:
                solution[each_name] = (0,)
                temp_0_set -= set(itertools.product(*solution.values()))
                solution[each_name] = (1,)
            result.append(temp_0_set)
        final_result.append(reduce(lambda x,y : x | y, result))
    elif not ['_' for temp in form_7 if temp not in word_talking_content]:#different form and have similiar processes
        solution[each[1]] = (1,)
        for each_name in new_name_list:
            solution[each_name] = (1,)
        result.append(set(itertools.product(*solution.values())))
        initial()
        solution[each[1]] = (0,)
        result.append(set(itertools.product(*solution.values())))
        final_result.append(reduce(lambda x,y : x | y, result))
    elif not ['_' for temp in form_8 if temp not in word_talking_content]:#different form and have similiar processes
        solution[each[1]] = (0,)
        temp_0_set = set(itertools.product(*solution.values()))
        for each_name in new_name_list:
            solution[each_name] = (0,)
        result.append(temp_0_set - set(itertools.product(*solution.values())))
        final_result.append(reduce(lambda x,y : x | y, result))
    elif not ['_' for temp in form_9 if temp not in word_talking_content]:
        result.append(set(itertools.product(*solution.values())))
        final_result.append(reduce(lambda x,y : x | y, result))
    elif not ['_' for temp in form_10 if temp not in word_talking_content]:
        result.append(set(['']))
        final_result.append(reduce(lambda x,y : x | y, result))
    elif not ['_' for temp in form_11 if temp not in word_talking_content]:
        if each[1] in each[0]:
            result.append(set(itertools.product(*solution.values())))
        else:
            solution[each[1]] = (1,)
            for each_name in new_name_list:
                solution[each_name] = (1, )
            result.append(set(itertools.product(*solution.values())))
            initial()
            solution[each[1]] = (0,)
            for each_name in new_name_list:
                solution[each_name] = (0, )
            result.append(set(itertools.product(*solution.values())))
        final_result.append(reduce(lambda x,y : x | y, result))
    elif not ['_' for temp in form_12 if temp not in word_talking_content]:#different form and have similiar processes
        if each[1] in each[0]:
            final_result.append({('')})
        else:
            solution[each[1]] = (1,)
            for each_name in new_name_list:
                solution[each_name] = (0, )
            result.append(set(itertools.product(*solution.values())))
            initial()
            solution[each[1]] = (0,)
            for each_name in new_name_list:
                solution[each_name] = (1, )
            result.append(set(itertools.product(*solution.values())))
        final_result.append(reduce(lambda x,y : x | y, result))
    elif not ['_' for temp in form_13 if temp not in word_talking_content]:#different form and have similiar processes
        if 'I' in each[0] or each[1] in each[0] or 'us' in each[0]:
            solution[each[1]] = (1,)
            result.append(set(itertools.product(*solution.values())))
            solution[each[1]] = (0,)
            for each_name in new_name_list:
                solution[each_name] = (0,)
            result.append(set(itertools.product(*solution.values())))
        else:
            solution[each[1]] = (1,)
            temp_1_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (0,)
            result.append(temp_1_set - set(itertools.product(*solution.values())))
            initial()
            solution[each[1]] = (0,)
            for each_name in new_name_list:
                solution[each_name] = (0,)
            result.append(set(itertools.product(*solution.values())))
        final_result.append(reduce(lambda x,y : x | y, result))
    elif not ['_' for temp in form_14 if temp not in word_talking_content]:#different form and have similiar processes
        if 'I' in each[0] or each[1] in each[0] or 'us' in each[0]:
            solution[each[1]] = (1,)
            temp_1_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (1,)
            result.append(temp_1_set - set(itertools.product(*solution.values())))
        else:
            solution[each[1]] = (1,)
            temp_1_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (1,)
            result.append(temp_1_set - set(itertools.product(*solution.values())))
            initial()
            solution[each[1]] = (0,)
            for each_name in new_name_list:
                solution[each_name] = (1,)
            result.append(set(itertools.product(*solution.values())))
        final_result.append(reduce(lambda x,y : x | y, result))
    elif not ['_' for temp in form_15 if temp not in word_talking_content]:#different form and have similiar processes
        if 'I' in each[0] or each[1] in each[0]:
            solution[each[1]] = (1,)
            for each_name in new_name_list:
                solution[each_name] = (1, )
            result.append(set(itertools.product(*solution.values())))
            initial()
            solution[each[1]] = (0,)
            result.append(set(itertools.product(*solution.values())))
        else:
            solution[each[1]] = (1,)
            for each_name in new_name_list:
                solution[each_name] = (1, )
            result.append(set(itertools.product(*solution.values())))
            initial()
            solution[each[1]] = (0,)
            temp_0_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (1,)
            result.append(temp_0_set - set(itertools.product(*solution.values())))
        final_result.append(reduce(lambda x,y : x | y, result))
    elif not ['_' for temp in form_16 if temp not in word_talking_content]:#different form and have similiar processes
        if 'I' in each[0] or each[1] in each[0]:
            solution[each[1]] = (0,)
            temp_0_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (0, )
            result.append(temp_0_set - set(itertools.product(*solution.values())))
        else:
            solution[each[1]] = (1,)
            for each_name in new_name_list:
                solution[each_name] = (0,)
            result.append(set(itertools.product(*solution.values())))
            initial()
            solution[each[1]] = (0,)
            temp_0_set = set(itertools.product(*solution.values()))
            for each_name in new_name_list:
                solution[each_name] = (0,)
            result.append(temp_0_set - set(itertools.product(*solution.values())))
        final_result.append(reduce(lambda x,y : x | y, result))

inter = reduce(lambda x,y : x & y, final_result)#get the intersection of all solution to ignore useless solution that cannot meet all requirements
num = len(inter)
if num == 0 or inter == {''}:
    print('There is no solution.')
elif num == 1:
    print('There is a unique solution:')
    result_list = list(zip(*inter, name_list))
    char = {1:'Knight', 0:'Knave'}
    for i in range(len(name_list)):
        print(f'Sir {result_list[i][1]} is a {char[result_list[i][0]]}.')
else:
    print(f'There are {num} solutions.')
