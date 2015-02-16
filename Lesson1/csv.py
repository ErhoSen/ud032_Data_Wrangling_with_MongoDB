import os
import csv

def parse_file(datafile):
    data = []
    with open(datafile, "rb") as f:
        r = csv.DictReader(f)
        colums = []
        buf = True
        counter=0
        for line in f:
            album = {}
            if counter>9:
                break
            if buf:
                colums = [line.strip() for line in line.split(',')]
                buf = False
                continue
            info = line.split(',')
            for i in range(len(info)):
                album[colums[i]] = info[i].strip()
            data.append(album)
            counter+=1
    return data

def test():
    datafile = 'beatles-diskography.csv'
    d = parse_file(datafile)
    for elem in d:
        print elem

test()