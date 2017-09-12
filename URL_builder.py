import csv

class Url_Builder():

    def __init__(self):
        f = open(r"C:\Users\Jelle\Documents\GitHub\dmas\photo_spotted.csv")
        nf = open(r"C:\Users\Jelle\Documents\GitHub\dmas\new.csv", "w")

        base_url = "http://oud.cleopatra-groningen.nl/user/photos/"

        for line in f:
            line = line[1:-2]
            print(line)
            nf.write(base_url + line + "\n")