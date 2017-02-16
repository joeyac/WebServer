# coding=utf-8


# 这个映射关系是前后端通用的,判题服务器提供接口,也应该遵守这个,可能需要一些转换
RESULT = {
    "accepted": 0,
    "runtime_error": 1,
    "time_limit_exceeded": 2,
    "memory_limit_exceeded": 3,
    "compile_error": 4,
    "presentation_error": 5,
    "wrong_answer": 6,
    "system_error": 7,

    "waiting": 8,

    "submit_error": 9,
    "unknown_error": 10,
}

RE_RESULT = {
     0: "accepted",
     1: "runtime error",
     2: "time limit exceeded",
     3: "memory limit exceeded",
     4: "compile error",
     5: "presentation error",
     6: "wrong answer",
     7: "system error",

     8: "waiting",

     9: "submit error",
     10: "unknown error",
}

languages = {
    "c": 1,
    "c++": 2,
    "java": 3,
    "python2": 4,
    "python3": 5,
}

RE_languages = {
    1: 'c',
    2: 'c++',
    3: 'java',
    4: 'python2',
    5: 'python3',
}

front_lang = {
    'USTBOJ': ['c', 'c++', 'java', 'python2', 'python3'] ,
    'POJ': ['g++', 'gcc', 'java', 'pascal', 'c', 'c++', 'fortran'] ,
    'HDU': ['g++', 'gcc', 'c++', 'c', 'pascal', 'java', 'c#'],
    'Codeforces': ['g++', 'c', 'g++11', 'g++14', 'gcc', 'java', 'python2', 'python3'],
}