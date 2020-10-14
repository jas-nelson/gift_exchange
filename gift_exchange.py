import os
import csv
import logging
import datetime
import random
import sys


class GiftExchange:
    def __init__(self, log='giftExchange_defaultLogger'):
        self.logger = None
        self.participants_exclusions = []
        self.participants = []
        self.matches = []
        self.has_given = []
        self.has_received = []
        self.local_exclusion = []
        self.initialize_logger(logname=self.process_log_path(log))

    def generate_pairs(self, filename):
        if filename is None:
            self.logger.error(msg="Filename is None. Filename required.")

        with open(file=filename) as file:
        # with open(file=filename) as file:

            csvreader = csv.reader(file)
            for row in csvreader:
                row = [x.strip(' ') for x in row]
                self.participants_exclusions.append(row)

        # get unique participants
        [self.participants.append(x[0]) for x in self.participants_exclusions]

        self.run_matching()



    def run_matching(self):
        for person in self.participants_exclusions:
            self.find_match(person=person)

        if len(self.participants) != len(self.participants_exclusions):
            self.has_given = []
            self.matches = []
            self.run_matching()

    def initialize_logger(self, logname="gift_exchange.log"):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        fileHandler = logging.FileHandler(logname)
        fileHandler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s %(message)s')
        fileHandler.setFormatter(formatter)

        self.logger.addHandler(fileHandler)

    def abort_matches_try_again(self):
        self.has_given.clear()
        self.has_received.clear()
        self.matches.clear()
        self.run_matching()

    def find_match(self, person):
        if person[0] in self.has_received:
            return



        # select potential gifter
        gifter = random.choice(list(set([x[0] for x in self.participants_exclusions]) - set(self.has_given) -
                                    set(self.local_exclusion)))
        giftee = person[0]

        if gifter in self.has_given:
            self.find_match(person=person)
            return

        gifter_exclusions = []
        try:
            gifter_exclusions = self.get_exclusions(gifter)

            if (giftee is not gifter) and (giftee not in gifter_exclusions):
                self.matches.append((gifter, giftee))
                self.has_given.append(gifter)
                self.has_received.append(giftee)
            elif (giftee is gifter) and (len(list(set([x[0] for x in self.participants_exclusions]) -
                                                  set(self.has_given) - set(giftee))) is 0) and len(self.has_given) > 0:
                self.abort_matches_try_again()
            else:

                self.local_exclusion.append(gifter)
                self.find_match(person=person)
                self.local_exclusion.clear()


        except Exception as e:
            print("error: ", e)
            self.abort_matches_try_again()




    def print_matches(self):
        for gifter, giftee in self.matches:
            print(str(gifter) + " gives to " + str(giftee))
            self.logger.info(msg=str(gifter) + " gives to " + str(giftee))


    def get_exclusions(self, participant_name):
        if participant_name is None:
            self.logger.error(msg="Cannot pass a None value to GiftExchange.get_exclusions().")
            return None

        # return participant,exclusions
        return [x[1:] for x in self.participants_exclusions if x[0] == participant_name][0]

    def process_log_path(self, fileName):
        if os.path.isabs(fileName):
            return os.path.abspath(fileName)
        else:
            return os.path.abspath(os.path.relpath(fileName, os.getcwd()))
#
# if __name__ == "__main__":
#     import argparse
#
#     parser = argparse.ArgumentParser(description="Create some gifter/giftee matches", prog='generate_matches')
#
#     parser.add_argument('-f', help='File containing list of participants of the gift exchange'
#                         , required=True)
#     parser.add_argument('--log', help='Log file name.')
#
#     args = parser.parse_args()
#
#     sys.setrecursionlimit(3000)
#
#     exchange = GiftExchange(log=args.log)
#     fileNameStr = args.f
#     # print(os.getcwd())
#     # print(args.log)
#     # log = process_log_path(args.log)
#
#     exchange.generate_pairs(filename=fileNameStr)
#     exchange.print_matches()
#
#     sys.setrecursionlimit(1000)


if __name__ == "__main__":

    sys.setrecursionlimit(3000)

    exchange = GiftExchange(log="debug.log")
    fileNameStr = "/Users/jason/projects/holiday_gift_exchange/pippenger_sibling_group"
    # print(os.getcwd())
    # print(args.log)
    # log = process_log_path(args.log)

    exchange.generate_pairs(filename=fileNameStr)
    exchange.print_matches()

    sys.setrecursionlimit(1000)

