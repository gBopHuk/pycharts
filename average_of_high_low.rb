#!/usr/bin/env ruby
# encoding: utf-8

USAGE = "usage: average_of_high_low FILE ..."

DAYS = {}

abort USAGE if ARGV.size < 1

for file in ARGV do 
  for line in open(file) do
    splitted = line.split(',')
    day = splitted.first
    high, low = splitted[3,2] #два элемента начиная с позиции 3 (отсчет ведется с нуля)
    mean = (high.to_f - low.to_f)/2
    DAYS[day] = mean
  end
end

for day, value in DAYS do
  puts "%s,%f" % [day, value]
end