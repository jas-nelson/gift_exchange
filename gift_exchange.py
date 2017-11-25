import csv
import logging
import datetime
import random
import sys


class GiftExchange:
    def __init__(self, log=None):
        self.initialize_logger(logname=log)
        self.logger = None
        self.participants = []
        self.matches = []
        self.has_given = []

    def generate_pairs(self, filename):
        if filename is None:
            self.logger.error(msg="Filename is None. Filename required.")

        with open(name=filename) as file:
        # with open(file=filename) as file:

            csvreader = csv.reader(file)
            for row in csvreader:
                row = [x.strip(' ') for x in row]
                self.participants.append(row)

        for person in self.participants:
            self.find_match(person=person)

    def initialize_logger(self, logname="gift_exchange.log"):
        self.logger = logging.basicConfig(filename=logname,
                                          format='%(asctime)s %(message)s',
                                          level=logging.INFO)

    def find_match(self, person):
        possible_gifter = random.choice(self.participants)
        gifter = possible_gifter[0]

        if gifter in self.has_given:
            self.find_match(person=person)
            return

        giftee_exclusions = []
        try:
            giftee, giftee_exclusions = self.get_exclusions(person)

            if (giftee is not gifter) and (gifter not in giftee_exclusions):
                self.matches.append((gifter, giftee))
                self.has_given.append(gifter)
            else:
                self.find_match(person=person)

        except:
            type, value, traceback = sys.exc_info()
            logging.error(msg="Type: " + str(type) + "\nValue: " + str(value) + "\nTraceback: " + str(traceback))



    def print_matches(self):
        for gifter, giftee in self.matches:
            print(str(gifter) + " gives to " + str(giftee))
            logging.info(msg=str(gifter) + " gives to " + str(giftee))

    def get_exclusions(self, participant_list):
        if participant_list is None:
            logging.error(msg="Cannot pass a None value to GiftExchange.get_exclusions().")
            return None

        i = 0
        participant = ""
        exclusions = []
        if len(participant_list) > 1:
            for elm in participant_list:
                if i == 0:
                    participant = elm
                else:
                    exclusions.append(elm)
                i = i + 1
        else:
            participant = participant_list[0]

        return participant,exclusions

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
