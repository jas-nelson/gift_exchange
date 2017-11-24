import csv
import logging
import datetime
import random


class GiftExchange:
    def __init__(self):
        self.initialize_logger()
        self.logger = None
        self.participants = []
        self.matches = []
        self.prev_matches = []

    def generate_pairs(self, filename):
        if filename is None:
            self.logger.error(msg="Filename is None. Filename required.")

        with open(name=filename) as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                self.participants.append(row)

        for person in self.participants:
            self.find_match(person=person)

    def initialize_logger(self):
        self.logger = logging.basicConfig(filename="gift_exchange.log",
                                          format='%(asctime)s %(message)s',
                                          level=logging.INFO)

    def find_match(self, person):
        possibleMatch = random.choice(self.participants)
        if possibleMatch not in self.prev_matches:
            self.matches.append((person, possibleMatch))
            self.prev_matches.append(possibleMatch)
        else:
            self.find_match(person=person)

    def print_matches(self):
        for gifter, giftee in self.matches:
            print(str(gifter[0]) + " buys for " + str(giftee[0]) + "\n")
            logging.info(msg=str(gifter[0]) + " buys for " + str(giftee[0]))



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create some gifter/giftee matches", prog='generate_matches')

    parser.add_argument('--participantFile', help='File containing list of participants of the gift exchange')
    parser.add_argument('--log', help='Log file name.')

    args = parser.parse_args()

    exchange = GiftExchange()
    fileNameStr = args.participantFile
    log = args.log

    exchange.generate_pairs(filename=fileNameStr)
    exchange.print_matches()
