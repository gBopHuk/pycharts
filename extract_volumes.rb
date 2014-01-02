#!/usr/bin/env ruby
# encoding: utf-8

USAGE = "usage: extract_volumes HH:MM-HH:MM FILE ..."

range = ARGV.shift# получаем первый элемент из массива ARGV 
                  # и удаляем его оттуда (нафиг он нам там нужен дальше)


if not (/^[0-2][0-9]:[0-5][0-9]-[0-2][0-9]:[0-5][0-9]$/ === range)  then
  abort "Неправильный формат диапазона\n\n#{USAGE}"
end #проверили диапазон, на всякий случай

a, b = range.split('-') #теперь в a и b строки вида "HH:MM"

DAYS = {}

for file in ARGV do 
# предполагаем что в массиве аргументов отсались только имена файлов
# для всех файлов
  for line in open(file) do
    # читаем по строчно 
    splitted = line.split(',') # разбиваем по запятой
    day, time = splitted[0,2] # первые два элемента — день и время
    volume = splitted.last.to_i # последний элемент — объем, и сразу в целое число конвертируем (to_i)
    if a <= time and time <= b then
      DAYS[day] ||= 0 # волшебная конструкция руби
                      # если DAYS[day] пуст, то там будет теперь ноль
                      # а если нет, то ничего не произойдет
      DAYS[day] += volume # докидываем объем к этому дню
    end
  end
end

#Теперь в ассоциативном массиве DAYS дофига данных. Выводим их.

for day, value in DAYS do
  puts "#{day},#{value}"
end