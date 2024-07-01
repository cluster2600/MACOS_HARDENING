import os.path
import glob
import yaml
from utils import sanitised_input, MacSecurityRule

def get_rule_yaml(rule_file, custom=False):
    resulting_yaml = {}
    names = [os.path.basename(x) for x in glob.glob('../custom/rules/**/*.yaml', recursive=True)]
    file_name = os.path.basename(rule_file)

    if custom:
        print(f"Custom settings found for rule: {rule_file}")
        try:
            override_path = glob.glob('../custom/rules/**/{}'.format(file_name), recursive=True)[0]
        except IndexError:
            override_path = glob.glob('../custom/rules/{}'.format(file_name), recursive=True)[0]
        with open(override_path) as r:
            rule_yaml = yaml.load(r, Loader=yaml.SafeLoader)
    else:
        with open(rule_file) as r:
            rule_yaml = yaml.load(r, Loader=yaml.SafeLoader)

    try:
        og_rule_path = glob.glob('../rules/**/{}'.format(file_name), recursive=True)[0]
    except IndexError:
        og_rule_path = glob.glob('../custom/rules/**/{}'.format(file_name), recursive=True)[0]

    with open(og_rule_path) as og:
        og_rule_yaml = yaml.load(og, Loader=yaml.SafeLoader)

    for yaml_field in og_rule_yaml:
        try:
            resulting_yaml[yaml_field] = rule_yaml[yaml_field] if og_rule_yaml[yaml_field] != rule_yaml[yaml_field] else og_rule_yaml[yaml_field]
            if 'customized' in resulting_yaml:
                resulting_yaml['customized'].append("customized {}".format(yaml_field))
            else:
                resulting_yaml['customized'] = ["customized {}".format(yaml_field)]
        except KeyError:
            resulting_yaml[yaml_field] = og_rule_yaml[yaml_field]

    return resulting_yaml

def collect_rules():
    all_rules = []
    keys = ['mobileconfig', 'macOS', 'severity', 'title', 'check', 'fix', 'odv', 'tags', 'id', 'references', 'result', 'discussion']
    references = ['disa_stig', 'cci', 'cce', '800-53r4', 'srg']

    for rule in sorted(glob.glob('../rules/**/*.yaml', recursive=True)) + sorted(glob.glob('../custom/rules/**/*.yaml', recursive=True)):
        rule_yaml = get_rule_yaml(rule, custom=False)
        for key in keys:
            if key not in rule_yaml:
                rule_yaml[key] = "missing"
            if key == "references":
                for reference in references:
                    if reference not in rule_yaml[key]:
                        rule_yaml[key][reference] = ["None"]

        all_rules.append(MacSecurityRule(rule_yaml['title'].replace('|', '\|'),
                                         rule_yaml['id'].replace('|', '\|'),
                                         rule_yaml['severity'].replace('|', '\|'),
                                         rule_yaml['discussion'].replace('|', '\|'),
                                         rule_yaml['check'].replace('|', '\|'),
                                         rule_yaml['fix'].replace('|', '\|'),
                                         rule_yaml['references']['cci'],
                                         rule_yaml['references']['cce'],
                                         rule_yaml['references']['800-53r4'],
                                         rule_yaml['references']['disa_stig'],
                                         rule_yaml['references']['srg'],
                                         rule_yaml['odv'],
                                         rule_yaml['tags'],
                                         rule_yaml['result'],
                                         rule_yaml['mobileconfig'],
                                         rule_yaml['mobileconfig_info']))

    return all_rules

def get_controls(all_rules):
    all_controls = []
    for rule in all_rules:
        for control in rule.rule_80053r4:
            if control not in all_controls:
                all_controls.append(control)

    all_controls.sort()
    return all_controls

def output_baseline(rules, version, baseline_tailored_string, benchmark, authors, full_title):
    inherent_rules = []
    permanent_rules = []
    na_rules = []
    supplemental_rules = []
    other_rules = []
    sections = []
    output_text = ""

    for rule in rules:
        if "inherent" in rule.rule_tags:
            inherent_rules.append(rule.rule_id)
        elif "permanent" in rule.rule_tags:
            permanent_rules.append(rule.rule_id)
        elif "n_a" in rule.rule_tags:
            na_rules.append(rule.rule_id)
        elif "supplemental" in rule.rule_tags:
            supplemental_rules.append(rule.rule_id)
        else:
            if rule.rule_id not in other_rules:
                other_rules.append(rule.rule_id)
            section_name = rule.rule_id.split("_")[0]+"_"+rule.rule_id.split("_")[1] if rule.rule_id.startswith("system_settings") else rule.rule_id.split("_")[0]
            if section_name not in sections:
                sections.append(section_name)

    if baseline_tailored_string:
        output_text = f'title: "{version["platform"]} {version["os"]}: Security Configuration -{full_title} {baseline_tailored_string}"\n'
        output_text += f'description: |\n  This guide describes the actions to take when securing a {version["platform"]} {version["os"]} system against the{full_title} {baseline_tailored_string} security baseline.\n'
    else:
        output_text = f'title: "{version["platform"]} {version["os"]}: Security Configuration -{full_title}"\n'
        output_text += f'description: |\n  This guide describes the actions to take when securing a {version["platform"]} {version["os"]} system against the{full_title} security baseline.\n'

    if benchmark == "recommended":
        output_text += "\n  Information System Security Officers and benchmark creators can use this catalog of settings in order to assist them in security benchmark creation. This list is a catalog, not a checklist or benchmark, and satisfaction of every item is not likely to be possible or sensible in many operational scenarios.\n"

    output_text += f'authors: |\n  {authors}'
    output_text += f'parent_values: "{benchmark}"\n'
    output_text += 'profile:\n'

    other_rules.sort()
    inherent_rules.sort()
    permanent_rules.sort()
    na_rules.sort()
    supplemental_rules.sort()

    if other_rules:
        for section in sections:
            output_text += ('  - section: "{}"\n'.format(section_title(section, version["cpe"])))
            output_text += ("    rules:\n")
            for rule in other_rules:
                if rule.startswith(section):
                    output_text += ("      - {}\n".format(rule))

    if inherent_rules:
        output_text += ('  - section: "Inherent"\n')
        output_text += ("    rules:\n")
        for rule in inherent_rules:
            output_text += ("      - {}\n".format(rule))

    if permanent_rules:
        output_text += ('  - section: "Permanent"\n')
        output_text += ("    rules:\n")
        for rule in permanent_rules:
            output_text += ("      - {}\n".format(rule))

    if na_rules:
        output_text += ('  - section: "not_applicable"\n')
        output_text += ("    rules: \n")
        for rule in na_rules:
            output_text += ("      - {}\n".format(rule))

    if supplemental_rules:
        output_text += ('  - section: "Supplemental"\n')
        output_text += ("    rules:\n")
        for rule in supplemental_rules:
            output_text += ("      - {}\n".format(rule))

    return output_text

def odv_query(rules, benchmark):
    print("The inclusion of any given rule is a risk-based-decision (RBD).  While each rule is mapped to an 800-53 control, deploying it in your organization should be part of the decision-making process. \nYou will be prompted to include each rule, and for those with specific organizational defined values (ODV), you will be prompted for those as well.\n")

    if benchmark != "recommended":
        print(f"WARNING: You are attempting to tailor an already established benchmark.  Excluding rules or modifying ODVs may not meet the compliance of the established benchmark.\n")

    included_rules = []
    queried_rule_ids = []

    include_all = False

    for rule in rules:
        get_odv = False

        _always_include = ['inherent']
        if any(tag in rule.rule_tags for tag in _always_include):
            include = "Y"
        elif include_all:
            if rule.rule_id not in queried_rule_ids:
                include = "Y"
                get_odv = True
                queried_rule_ids.append(rule.rule_id)
                remove_odv_custom_rule(rule)
        else:
            if rule.rule_id not in queried_rule_ids:
                include = sanitised_input(f"Would you like to include the rule for \"{rule.rule_id}\" in your benchmark? [Y/n/all/?]: ", str.lower, range_=('y', 'n', 'all', '?'), default_="y")
                if include == "?":
                    print(f'Rule Details: \n{rule.rule_discussion}')
                    include = sanitised_input(f"Would you like to include the rule for \"{rule.rule_id}\" in your benchmark? [Y/n/all]: ", str.lower, range_=('y', 'n', 'all'), default_="y")
                queried_rule_ids.append(rule.rule_id)
                get_odv = True
                remove_odv_custom_rule(rule)
                if include.upper() == "ALL":
                    include_all = True
                    include = "y"
        if include.upper() == "Y":
            included_rules.append(rule)
            if rule.rule_odv == "missing":
                continue
            elif get_odv:
                if benchmark == "recommended":
                    print(f'{rule.rule_odv["hint"]}')
                    if isinstance(rule.rule_odv["recommended"], int):
                         odv = sanitised_input(f'Enter the ODV for \"{rule.rule_id}\" or press Enter for the recommended value ({rule.rule_odv["recommended"]}): ', int, default_=rule.rule_odv["recommended"])
                    elif isinstance(rule.rule_odv["recommended"], bool):
                         odv = sanitised_input(f'Enter the ODV for \"{rule.rule_id}\" or press Enter for the recommended value ({rule.rule_odv["recommended"]}): ', bool, default_=rule.rule_odv["recommended"])
                    else:
                         odv = sanitised_input(f'Enter the ODV for \"{rule.rule_id}\" or press Enter for the recommended value ({rule.rule_odv["recommended"]}): ', str, default_=rule.rule_odv["recommended"])
                    if odv and odv != rule.rule_odv["recommended"]:
                        write_odv_custom_rule(rule, odv)
                else:
                    print(f'\nODV value: {rule.rule_odv["hint"]}')
                    if isinstance(rule.rule_odv[benchmark], int):
                         odv = sanitised_input(f'Enter the ODV for \"{rule.rule_id}\" or press Enter for the default value ({rule.rule_odv[benchmark]}): ', int, default_=rule.rule_odv[benchmark])
                    elif isinstance(rule.rule_odv[benchmark], bool):
                         odv = sanitised_input(f'Enter the ODV for \"{rule.rule_id}\" or press Enter for the default value ({rule.rule_odv[benchmark]}): ', bool, default_=rule.rule_odv[benchmark])
                    else:
                         odv = sanitised_input(f'Enter the ODV for \"{rule.rule_id}\" or press Enter for the default value ({rule.rule_odv[benchmark]}): ', str, default_=rule.rule_odv[benchmark])
                    if odv and odv != rule.rule_odv[benchmark]:
                        write_odv_custom_rule(rule, odv)
    return included_rules

def write_odv_custom_rule(rule, odv):
    print(f"Writing custom rule for {rule.rule_id} to include value {odv}")

    if not os.path.exists("../custom/rules"):
        os.makedirs("../custom/rules")
    if os.path.exists(f"../custom/rules/{rule.rule_id}.yaml"):
        with open(f"../custom/rules/{rule.rule_id}.yaml") as f:
            rule_yaml = yaml.load(f, Loader=yaml.SafeLoader)
    else:
        rule_yaml = {}

    rule_yaml['odv'] = {"custom" : odv}
    with open(f"../custom/rules/{rule.rule_id}.yaml", 'w') as f:
        yaml.dump(rule_yaml, f, explicit_start=True)

def remove_odv_custom_rule(rule):
    odv_yaml = {}
    try:
        with open(f"../custom/rules/{rule.rule_id}.yaml") as f:
            odv_yaml = yaml.load(f, Loader=yaml.SafeLoader)
            odv_yaml.pop('odv', None)
    except:
        pass

    if odv_yaml:
        with open(f"../custom/rules/{rule.rule_id}.yaml", 'w') as f:
            yaml.dump(odv_yaml, f, explicit_start=True)
    else:
        if os.path.exists(f"../custom/rules/{rule.rule_id}.yaml"):
            os.remove(f"../custom/rules/{rule.rule_id}.yaml")
