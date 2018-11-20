import os
import csv
import logging
import datetime
import random
import sys


class GiftExchange:
    def __init__(self, log='giftExchange_defaultLogger'):
        self.logger = None
        self.participants = []
        self.matches = []
        self.has_given = []
        self.initialize_logger(logname=self.process_log_path(log))

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
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        fileHandler = logging.FileHandler(logname)
        fileHandler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s %(message)s')
        fileHandler.setFormatter(formatter)

        self.logger.addHandler(fileHandler)


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
            self.logger.error(msg="Type: " + str(type) + "\nValue: " + str(value) + "\nTraceback: " + str(traceback))



    def print_matches(self):
        for gifter, giftee in self.matches:
            print(str(gifter) + " gives to " + str(giftee))
            self.logger.info(msg=str(gifter) + " gives to " + str(giftee))


    def get_exclusions(self, participant_list):
        if participant_list is None:
            self.logger.error(msg="Cannot pass a None value to GiftExchange.get_exclusions().")
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

    def process_log_path(self, fileName):
        if os.path.isabs(fileName):
            return os.path.abspath(fileName)
        else:
            return os.path.abspath(os.path.relpath(fileName, os.getcwd()))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create some gifter/giftee matches", prog='generate_matches')

    parser.add_argument('-f', help='File containing list of participants of the gift exchange'
                        , required=True)
    parser.add_argument('--log', help='Log file name.')

    args = parser.parse_args()

    exchange = GiftExchange(log=args.log)
    fileNameStr = args.f
    print(os.getcwd())
    print(args.log)
    # log = process_log_path(args.log)

    exchange.generate_pairs(filename=fileNameStr)
    exchange.print_matches()
