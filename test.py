flag = True

title = input('название теста латинскими символами: ')
params = input('впиши имена рассматриваемых переменных через пробел: ')
l = len(params.split())
print('для остановки вместо данных напиши stop')

with open(f'Tests/test{title}.txt', 'w') as file:
    file.writelines(title+'\n')
    file.writelines(params+'\n')
    i = 1
    while flag:
        line = input(f'0. итерация данных n{i}:\n')
        while len(line.split())!=l and line!='stop':
            line = input('количество данных не совпадает с заданными переменными введите ещё раз:\n')
        if line=='stop':
            break
        file.writelines(f'{i}. ' + line + '\n')
        i+=1