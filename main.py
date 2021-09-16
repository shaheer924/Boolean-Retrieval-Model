import os

from nltk.stem import PorterStemmer

# from nltk.tokenize import word_tokenize

# import nltk
# nltk.download()

# list data read all file Data
data = []
file = []
index = {}
invertedIndex = {}
word = []
positionalIndex = {}
result = []
i = 0

ps = PorterStemmer()

# Reading the data
path: str = r"D:\Assignment_01_IR\ShortStories"  # Path to read files of short stories
for filename in os.listdir(path):
    full_path = os.path.join(path, filename)  # evaluating Path of all File
    with open(full_path, encoding="utf-8") as f:
        file_data = f.read()
        data.append(file_data)  # appending the file_data in data list
        # print(filename)
        file.append(filename)
    i = i + 1


# print(data[1][0] + data[1][1])


def word_break(arr):  # Breaking the lines into words of all file
    dat = []
    element = ''
    for m in range(len(arr)):  # Conditions to break Words
        if arr[m] == ' ' or arr[m] == ',' or arr[m] == '.' or arr[m] == '\n' or arr[m] == '"' or arr[m] == '?' or \
                arr[m] == ';' or arr[m] == ':' or arr[m] == '!' or arr[m] == '-' or arr[m] == '—' or arr[m] == '“' \
                or arr[m] == '”' or arr[m] == '(' or arr[m] == ')':
            if element == '”' or element == ' ' or element == ':' or element == '!':
                element = ''
                continue
            else:
                dat.append(element.replace('!', '').replace('\n', '').replace('"', '').replace('?', '').replace('“', '')
                           .replace(';', '').lower())  # appending data in dat list
            element = ''  # removing previous word from element
            continue

        element = element + arr[m]  # entering word in element from data list
        for n in range(len(element)):
            if element[n] == '”':
                element[n].replace('”', '1')
    for j in range(dat.count('')):
        dat.remove('')
    # print(dat)
    arr = dat
    return arr  # returning the list which is converted into individual word


def stop_words(arr):  # removing stop words from data list
    ft = open("D:\\Assignment_01_IR\Stopword-List.txt ", "r")  # path to read stop words
    stopwords = ft.read()
    stopwords = word_break(stopwords)  # entering stop words in to stopwords list
    for n in range(len(stopwords)):
        counts = arr.count(stopwords[n])  # counting specific stop words in a file
        for o in range(counts):
            arr.remove(stopwords[n])  # removing stop words from a file one by one (file)
    return arr  # returning the whole data list named as arr in this function


def stemming():
    for l_data in range(len(data)):
        for w_data in range(len(data[l_data])):
            data[l_data][w_data] = ps.stem(data[l_data][w_data])


def convert_Dictionary_1():  # converting data into dictionary with key as a file name
    for i in range(len(data)):
        index[file[i]] = data[i]  # index is a dictionary to insert data as dictionary


def word_find(arr, word_f):  # finding word from specific file or whole data list
    i = 0
    for i in range(len(arr)):
        if arr[i] == word_f:  # arr is a document and word_f is a word to be find
            return True  # if word found then return true else return false
    return False


def inverted_index():  # inverted index of data which is read from file
    for i in range(len(data)):
        for j in range(len(data[i])):
            # print(data[i][j])
            if data[i][j] not in word:
                word.append(data[i][j])  # appending data in word
                continue
    lists = []
    for i in range(len(word)):
        for j in file:
            if word[i] in index[j]:
                lists.append(j.strip('.txt'))
        invertedIndex[word[i]] = lists  # appending data i inverted index
        lists = []


def positional_index_1(letters, pos):
    red = []
    read = {}
    for x in invertedIndex[letters]:
        lpt = index[x + '.txt']
        for y in range(len(index[x + '.txt'])):
            if word[pos] == lpt[y]:  # positional index condition for a single word
                red.append(y + 1)  # appending data in dictionaries
            read.update({x: red})  # appending data in dictionary to append in positional index
        red = []
    return read


def positional_index():
    for pos in range(len(word)):
        real = positional_index_1(word[pos],pos)  # dictionary for a word
        positionalIndex.update({word[pos]: [len(invertedIndex[word[pos]]), real]})  #positional index


def processing_and(word_1, word_2, query):  # processing the queries of AND
    ans = []
    print(word_1, word_2, query)
    list1 = invertedIndex[ps.stem(word_1)]
    list2 = invertedIndex[ps.stem(word_2)]
    print(list1)
    print(list2)
    if len(list1) <= len(list2):
        for listing in range(len(list1)):
            if list1[listing] in list2:
                ans.append(list1[listing])
    else:
        for listing in range(len(list2)):
            if list2[listing] in list1:
                ans.append(list2[listing])
    print(ans)
    result.append(ans)
    print(result)


def processing_or(word_1, word_2, query):  # processing the queries of OR
    print(word_1, word_2, query)
    ans = []
    list1 = invertedIndex[ps.stem(word_1)]
    list2 = invertedIndex[ps.stem(word_2)]
    print(list1)
    print(list2)
    ans = list1
    for listing in range(len(list2)):
        if list2[listing] not in list1:
            ans.append(list2[listing])
    print(ans)
    result.append(ans)
    print(result)


def processing_not(word_2, query):  # processing the queries of NOT
    print(word_2, query)
    ans = []
    list2 = invertedIndex[ps.stem(word_2)]
    print(list2)
    for x in file:
        if x.strip('.txt') not in list2:
            ans.append(x.strip('.txt'))
    print(ans)
    result.append(ans)
    print(result)


def processing_single(word_1):  # processing the queries for Single Word
    ans = invertedIndex[ps.stem(word_1)]
    print(ans)


def list_and(arr1, arr2):  # ANDing 2 list
    res = []
    if len(arr1) <= len(arr2):
        for listing in range(len(arr1)):
            if arr1[listing] in arr2:
                res.append(arr1[listing])
    else:
        for listing in range(len(arr2)):
            if arr2[listing] in arr1:
                res.append(arr1[listing])
    print("Result : ", res)
    return res


def processing(string_input):  # processing queries main
    cnt = 0
    ele = []
    elements = ''
    for t in range(len(string_input)):  # breaking the queries into single words
        if string_input[t] == '/':
            continue
        if string_input[t] == ' ' or string_input[t] == '.':
            ele.append(elements)
            elements = ''
        else:
            elements = elements + string_input[t]
    print(ele)
    for w in range(len(ele)):  # accessing the functions to be performed
        if ele[w] == 'and' or ele[w] == 'or' or ele[w] == 'not':
            cnt = cnt + 1
    print("Function To Be performed : ",cnt)
    # retrieving the operations
    number = 0
    if len(ele) == 3 and cnt == 0:  # for queries of distance of words
        number = ele[len(ele) - 1]
        lst1 = invertedIndex[ps.stem(ele[0])]
        lst2 = invertedIndex[ps.stem(ele[1])]
        lst = list_and(lst1, lst2)
        print(lst)
    else:
        for opt_cnt in range(len(ele)):
            if ele[opt_cnt] == 'and':  # and word queries of AND (Complex, Simple)
                word1 = ele[opt_cnt - 1]
                word2 = ele[opt_cnt + 1]
                opt = ele[opt_cnt]
                processing_and(word1, word2, opt)
            if ele[opt_cnt] == 'or':  # and word queries of OR (Complex, Simple)
                word1 = ele[opt_cnt - 1]
                word2 = ele[opt_cnt + 1]
                opt = ele[opt_cnt]
                processing_or(word1, word2, opt)
            if ele[opt_cnt] == 'not':  # and word queries of NOT (Complex, Simple)
                word2 = ele[opt_cnt + 1]
                print(ele[opt_cnt + 1])
                opt = ele[opt_cnt]
                processing_not(word2, opt)
            if cnt == 0:  # and word queries of Single
                word1 = ele[opt_cnt]
                processing_single(word1)
        if cnt == 2 or cnt == 4: # and word queries of 2 words
            list_and(result[0], result[1])


# main functions to be performed in list


for k in range(len(data)):
    data[k] = word_break(data[k])  # word break from files
for a in range(len(data)):
    data[a] = stop_words(data[a])  # removing stop words from data
stemming()  # performing stemming
convert_Dictionary_1()  # Own usage function
inverted_index()  # inverted index
positional_index()  # Positional index
# print(positionalIndex)
print("Note : After entering Query insert '.' or 'Space' to end the query") # Note
value_input = input("Enter Your String Here : ") # reading Queries
processing(value_input) # function Called

# Note that when the Queries entered queries will be ended  by using '.' 'full stop' Most important