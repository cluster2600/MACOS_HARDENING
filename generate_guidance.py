#!/usr/bin/env python3
# filename: generate_guidance.py
# description: Process a given keyword, and output a baseline file

import os
import yaml
from arg_parser import create_args
from rule_handler import collect_rules, get_controls, output_baseline, odv_query
from utils import parse_authors, append_authors, available_tags

def main():
    args = create_args()
    try:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(file_dir)

        original_working_directory = os.getcwd()
        os.chdir(file_dir)

        all_rules = collect_rules()

        if args.list_tags:
            available_tags(all_rules)
            return

        if args.controls:
            baselines_file = os.path.join(parent_dir, 'includes', '800-53_baselines.yaml')
            with open(baselines_file) as r:
                baselines = yaml.load(r, Loader=yaml.SafeLoader)

            included_controls = get_controls(all_rules)
            needed_controls = []

            for control in baselines['low']:
                if control not in needed_controls:
                    needed_controls.append(control)

            for n_control in needed_controls:
                if n_control not in included_controls:
                    print(f'{n_control} missing from any rule, needs a rule, or included in supplemental')

            return

        build_path = os.path.join(parent_dir, 'build', 'baselines')
        if not (os.path.isdir(build_path)):
            try:
                os.makedirs(build_path)
            except OSError:
                print(f"Creation of the directory {build_path} failed")

    except IOError as msg:
        parser.error(str(msg))

    mscp_data_file = os.path.join(parent_dir, 'includes', 'mscp-data.yaml')
    with open(mscp_data_file) as r:
        mscp_data_yaml = yaml.load(r, Loader=yaml.SafeLoader)

    version_file = os.path.join(parent_dir, "VERSION.yaml")
    with open(version_file) as r:
        version_yaml = yaml.load(r, Loader=yaml.SafeLoader)

    found_rules = []
    for rule in all_rules:
        if args.keyword in rule.rule_tags or args.keyword == "all_rules":
            found_rules.append(rule)

    if args.keyword is None:
        print("No rules found for the keyword provided, please verify from the following list:")
        available_tags(all_rules)
    else:
        _established_benchmarks = ['stig', 'cis_lvl1', 'cis_lvl2']
        benchmark = args.keyword if any(bm in args.keyword for bm in _established_benchmarks) else "recommended"

        authors = parse_authors(mscp_data_yaml['authors'][args.keyword]) if args.keyword in mscp_data_yaml['authors'] else "|===\n  |Name|Organization\n  |===\n"
        full_title = f" {mscp_data_yaml['titles'][args.keyword]}" if args.keyword in mscp_data_yaml['titles'] and not args.tailor else f" {args.keyword}"

        baseline_tailored_string = ""
        if args.tailor:
            tailored_filename = sanitised_input(f'Enter a name for your tailored benchmark or press Enter for the default value ({args.keyword}): ', str, default_=args.keyword)
            custom_author_name = sanitised_input('Enter your name: ')
            custom_author_org = sanitised_input('Enter your organization: ')
            authors = append_authors(authors, custom_author_name, custom_author_org)
            baseline_tailored_string = f"{args.keyword.upper()} (Tailored)" if tailored_filename == args.keyword else f"{tailored_filename.upper()} (Tailored from {args.keyword.upper()})"
            odv_baseline_rules = odv_query(found_rules, benchmark)
            with open(f"{build_path}/{tailored_filename}.yaml", 'w') as baseline_output_file:
                baseline_output_file.write(output_baseline(odv_baseline_rules, version_yaml, baseline_tailored_string, benchmark, authors, full_title))
        else:
            with open(f"{build_path}/{args.keyword}.yaml", 'w') as baseline_output_file:
                baseline_output_file.write(output_baseline(found_rules, version_yaml, baseline_tailored_string, benchmark, authors, full_title))

    os.chdir(original_working_directory)

if __name__ == "__main__":
    main()
