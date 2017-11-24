from gift_exchange import GiftExchange
import argparse
import os.path


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create some gifter/giftee matches", prog='generate_matches')

    parser.add_argument('--participantFile', help='File containing list of participants of the gift exchange'
                        , required=True)
    parser.add_argument('--log', help='Log file name.')

    args = parser.parse_args()

    exchange = GiftExchange()
    fileNameStr = args.participantFile
    log = args.log

    exchange.generate_pairs(filename=fileNameStr)
    exchange.print_matches()
