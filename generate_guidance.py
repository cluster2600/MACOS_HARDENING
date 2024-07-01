import os
import yaml
from arg_parser import create_args
from rule_handler import collect_rules, get_controls, output_baseline, odv_query
from utils import parse_authors, append_authors, available_tags

def main():
    args = create_args()
    try:
        root_dir = '/Users/maximegrenu/Documents/CODE/Mac_sec/'
        includes_dir = os.path.join(root_dir, 'includes')
        build_dir = os.path.join(root_dir, 'build', 'baselines')

        original_working_directory = os.getcwd()
        os.chdir(root_dir)

        all_rules = collect_rules()

        if args.list_tags:
            available_tags(all_rules)
            return

        if args.controls:
            baselines_file = os.path.join(includes_dir, '800-53_baselines.yaml')
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

        if not (os.path.isdir(build_dir)):
            try:
                os.makedirs(build_dir)
            except OSError:
                print(f"Creation of the directory {build_dir} failed")

    except IOError as msg:
        parser.error(str(msg))

    mscp_data_file = os.path.join(includes_dir, 'mscp-data.yaml')
    with open(mscp_data_file) as r:
        mscp_data_yaml = yaml.load(r, Loader=yaml.SafeLoader)

    version_file = os.path.join(root_dir, "VERSION.yaml")
    with open(version_file) as r:
        version_yaml = yaml.load(r, Loader=yaml.SafeLoader)

    found_rules = []
    for rule in all_rules:
        if args.keyword in rule.rule_tags or args.keyword == "all_rules":
            found_rules.append(rule)

    if not found_rules:
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
            with open(f"{build_dir}/{tailored_filename}.yaml", 'w') as baseline_output_file:
                baseline_output_file.write(output_baseline(odv_baseline_rules, version_yaml, baseline_tailored_string, benchmark, authors, full_title))
        else:
            with open(f"{build_dir}/{args.keyword}.yaml", 'w') as baseline_output_file:
                baseline_output_file.write(output_baseline(found_rules, version_yaml, baseline_tailored_string, benchmark, authors, full_title))

    os.chdir(original_working_directory)

if __name__ == "__main__":
    main()
