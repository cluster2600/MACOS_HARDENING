import os
import yaml

class MacSecurityRule:
    def __init__(self, title, rule_id, severity, discussion, check, fix, cci, cce, nist_controls, disa_stig, srg, odv, tags, result_value, mobileconfig, mobileconfig_info):
        self.rule_title = title
        self.rule_id = rule_id
        self.rule_severity = severity
        self.rule_discussion = discussion
        self.rule_check = check
        self.rule_fix = fix
        self.rule_cci = cci
        self.rule_cce = cce
        self.rule_80053r4 = nist_controls
        self.rule_disa_stig = disa_stig
        self.rule_srg = srg
        self.rule_odv = odv
        self.rule_result_value = result_value
        self.rule_tags = tags
        self.rule_mobileconfig = mobileconfig
        self.rule_mobileconfig_info = mobileconfig_info

    def create_asciidoc(self, adoc_rule_template):
        """Pass an AsciiDoc template as file object to return formatted AsciiDOC"""
        rule_adoc = adoc_rule_template.substitute(
            rule_title=self.rule_title,
            rule_id=self.rule_id,
            rule_severity=self.rule_severity,
            rule_discussion=self.rule_discussion,
            rule_check=self.rule_check,
            rule_fix=self.rule_fix,
            rule_cci=self.rule_cci,
            rule_80053r4=self.rule_80053r4,
            rule_disa_stig=self.rule_disa_stig,
            rule_srg=self.rule_srg,
            rule_result=self.rule_result_value
        )
        return rule_adoc

def sanitised_input(prompt, type_=None, range_=None, default_=None):
    while True:
        ui = input(prompt) or default_
        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print("Input type must be {0}.".format(type_.__name__))
                continue
        if type_ is str and ui.isnumeric():
            print("Input type must be {0}.".format(type_.__name__))
            continue

        if range_ is not None and ui not in range_:
            if isinstance(range_, range):
                print(f"Input must be between {range_.start} and {range_.stop}.")
            else:
                expected = " or ".join((
                    ", ".join(str(x) for x in range_[:-1]),
                    str(range_[-1])
                ))
                print(f"Input must be {expected}.")
        else:
            return ui

def parse_authors(authors_from_yaml):
    author_block = "*macOS Security Compliance Project*\n\n  "
    if "preamble" in authors_from_yaml.keys():
        preamble = authors_from_yaml['preamble']
        author_block += f'{preamble}\n  '

    author_block += "|===\n  "
    for name in authors_from_yaml['names']:
        author_block += f'|{name}\n  '
    author_block += "|===\n"
    return author_block

def append_authors(authors, name, org):
    author_block = "*Security configuration tailored by:*\n  |===\n  "
    author_block += f"|{name}|{org}\n  |===\n  {authors}"
    return author_block

def available_tags(all_rules):
    all_tags = [tag for rule in all_rules for tag in rule.rule_tags]
    unique_tags = sorted(set(all_tags))
    unique_tags.append("all_rules")

    for tag in unique_tags:
        print(tag)
    return
