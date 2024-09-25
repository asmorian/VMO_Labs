class Array:
    arr =[[False, '', 0, 511]]

    def add(self, name, size):
        maxsize = 0
        pos = 0
        for i in range(len(self.arr)):
            if(self.arr[i][0] == False):
                if(self.arr[i][3] > maxsize):
                    maxsize = self.arr[i][3]
                    pos = i
        self.arr.insert(pos, [True, name, self.arr[pos][2], size])
        self.arr[pos + 1][3] -= size
        self.arr[pos + 1][2] = self.arr[pos][2] + self.arr[pos][3]
        print('Адрес памяти: ', self.arr[pos][2])

    def rem(self, ad):

        for i in range(len(self.arr)):
            if(self.arr[i][2] == ad):
                self.arr[i][0] = False
                self.arr[i][1] = ''
        k = 0
        while(k < len(self.arr)-1):
            if((self.arr[k][0] == False) and (self.arr[k+1][0] == False)):
                self.arr[k][3] += self.arr[k+1][3]
                del self.arr[k+1]
                if(k > 0):
                    k -= 1
            k += 1
        print(self.arr)

    def info(self):
        False_Count = 0
        True_Count = 0
        Fl = []
        Tr = []
        F_mem = 0
        T_mem = 0
        for i in range(len(self.arr)):
            if(self.arr[i][0] == False):
                False_Count += 1
                Fl.append(self.arr[i][2])
                F_mem += self.arr[i][3]
            else:
                True_Count += 1
                Tr.append(self.arr[i][2])
                T_mem += self.arr[i][3]

        print('Общее количество свободных процессов: ', False_Count)
        print('Общее количество занятых процессов: ', True_Count)
        print('Общее количество свободной памяти: ', F_mem)
        print('Общее количество занятой памяти: ', T_mem)
        print('Адреса свободной памяти: ', Fl)
        print('Адреса занятой памяти: ', Tr)


s = Array()
while(1):

    print('ДЕЙСТВИЕ:')
    print('1 ДОБАВИТЬ ПРОЦЕСС В ПАМЯТЬ')
    print('2 УДАЛИТЬ ПРОЦЕСС ИЗ ПАМЯТИ')
    print('3 ПОКАЗАТЬ ДАННЫЕ')
    print('4 ВЫВЕСТИ ОБЛАСТЬ ПАМЯТИ')

    inp = int(input())
    if(inp == 1):
        a = input('Наименование процесса: ')
        b = int(input('Выделение памяти: '))
        s.add(a, b)
        del b
    elif(inp == 2):
        b = int(input('Адрес удаляемого процесса: '))
        s.rem(b)
        del b

    elif(inp == 3):
        s.info()

    elif(inp == 4):
        print(s.arr)
    else:
        break
