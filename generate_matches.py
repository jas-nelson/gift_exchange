from gift_exchange import GiftExchange
import argparse
import os.path


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create some gifter/giftee matches", prog='generate_matches')

    parser.add_argument('-f', help='File containing list of participants of the gift exchange'
                        , required=True)
    parser.add_argument('--log', help='Log file name.')

    args = parser.parse_args()

    fileNameStr = args.f
    logArg = args.log
    exchange = GiftExchange(log=logArg)

    # fileNameStr = "/Users/jason/projects/holiday_gift_exchange/pippenger_sibling_group"

    exchange = GiftExchange()

    exchange.generate_pairs(filename=fileNameStr)
    exchange.print_matches()
