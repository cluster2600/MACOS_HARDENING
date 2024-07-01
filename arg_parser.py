import argparse

def create_args():
    parser = argparse.ArgumentParser(
        description='Given a keyword tag, generate a generic baseline.yaml file containing rules with the tag.')
    parser.add_argument("-c", "--controls", default=None,
                        help="Output the 800-53 controls covered by the rules.", action="store_true")
    parser.add_argument("-k", "--keyword", default=None,
                        help="Keyword tag to collect rules containing the tag.", action="store")
    parser.add_argument("-l", "--list_tags", default=None,
                        help="List the available keyword tags to search for.", action="store_true")
    parser.add_argument("-t", "--tailor", default=None,
                        help="Customize the baseline to your organizations values.", action="store_true")

    return parser.parse_args()
