import os
import yaml
from typing import List, Optional
from arg_parser import create_args
from rule_handler import collect_rules, get_controls, output_baseline, odv_query
from utils import parse_authors, append_authors, available_tags, sanitised_input

class BaselineGenerator:
    """Generates security baselines for macOS based on command-line arguments."""

    def __init__(self):
        """Initialize with parsed arguments and directory paths."""
        self.args = create_args()
        self.root_dir = '/Users/maximegrenu/Documents/CODE/Mac_sec/'
        self.includes_dir = os.path.join(self.root_dir, 'includes')
        self.build_dir = os.path.join(self.root_dir, 'build', 'baselines')
        self.original_wd = os.getcwd()

    def setup_directories(self) -> None:
        """Set up working directory and create build directory if needed."""
        os.chdir(self.root_dir)
        if not os.path.isdir(self.build_dir):
            os.makedirs(self.build_dir, exist_ok=True)

    def load_yaml_file(self, filepath: str) -> dict:
        """Safely load a YAML file with specific error handling."""
        try:
            with open(filepath, 'r') as file:
                return yaml.load(file, Loader=yaml.SafeLoader)
        except FileNotFoundError:
            raise RuntimeError(f"YAML file not found: {filepath}")
        except yaml.YAMLError as e:
            raise RuntimeError(f"Error parsing YAML file {filepath}: {str(e)}")

    def list_available_tags(self, rules: List) -> None:
        """Display available tags and exit."""
        available_tags(rules)
        raise SystemExit(0)

    def check_controls(self, rules: List) -> None:
        """Check for missing NIST 800-53 controls in rules."""
        baselines = self.load_yaml_file(os.path.join(self.includes_dir, '800-53_baselines.yaml'))
        included_controls = get_controls(rules)
        needed_controls = list(dict.fromkeys(baselines['low']))  # Remove duplicates
        
        for control in needed_controls:
            if control not in included_controls:
                print(f'{control} missing from any rule, needs a rule or supplemental inclusion')
        raise SystemExit(0)

    def get_matching_rules(self, all_rules: List) -> List:
        """Filter rules based on the provided keyword."""
        return [rule for rule in all_rules if self.args.keyword in rule.rule_tags or self.args.keyword == "all_rules"]

    def generate_baseline(self, rules: List, mscp_data: dict, version_data: dict) -> None:
        """Generate and write the baseline file."""
        established_benchmarks = ['stig', 'cis_lvl1', 'cis_lvl2']
        benchmark = self.args.keyword if any(bm in self.args.keyword for bm in established_benchmarks) else "recommended"
        
        authors = (parse_authors(mscp_data['authors'][self.args.keyword]) 
                  if self.args.keyword in mscp_data['authors'] 
                  else "|===\n  |Name|Organization\n  |===\n")
        
        full_title = (f" {mscp_data['titles'][self.args.keyword]}" 
                     if self.args.keyword in mscp_data['titles'] and not self.args.tailor 
                     else f" {self.args.keyword}")

        if self.args.tailor:
            self._generate_tailored_baseline(rules, benchmark, authors, full_title, version_data)
        else:
            self._generate_standard_baseline(rules, benchmark, authors, full_title, version_data)

    def _generate_tailored_baseline(self, rules: List, benchmark: str, authors: str, title: str, version: dict) -> None:
        """Handle tailored baseline generation with user input."""
        tailored_filename = self._get_sanitised_input(
            f'Enter a name for your tailored benchmark or press Enter for default ({self.args.keyword}): ',
            default_=self.args.keyword
        )
        custom_author_name = self._get_sanitised_input('Enter your name: ')
        custom_author_org = self._get_sanitised_input('Enter your organization: ')
        
        authors = append_authors(authors, custom_author_name, custom_author_org)
        baseline_string = (f"{self.args.keyword.upper()} (Tailored)" 
                         if tailored_filename == self.args.keyword 
                         else f"{tailored_filename.upper()} (Tailored from {self.args.keyword.upper()})")
        
        self._write_baseline(tailored_filename, odv_query(rules, benchmark), 
                           version, baseline_string, benchmark, authors, title)

    def _generate_standard_baseline(self, rules: List, benchmark: str, authors: str, title: str, version: dict) -> None:
        """Handle standard baseline generation."""
        self._write_baseline(self.args.keyword, rules, version, "", benchmark, authors, title)

    def _write_baseline(self, filename: str, rules: List, version: dict, baseline_string: str, 
                       benchmark: str, authors: str, title: str) -> None:
        """Write the baseline to a YAML file."""
        output_path = os.path.join(self.build_dir, f"{filename}.yaml")
        try:
            with open(output_path, 'w') as output_file:
                output_file.write(output_baseline(rules, version, baseline_string, benchmark, authors, title))
        except IOError as e:
            raise RuntimeError(f"Error writing baseline to {output_path}: {str(e)}")

    def _get_sanitised_input(self, prompt: str, default_: Optional[str] = None) -> str:
        """Get validated user input with an optional default."""
        return sanitised_input(prompt, str, default_=default_)

    def run(self) -> None:
        """Execute the main baseline generation logic."""
        try:
            self.setup_directories()
            all_rules = collect_rules()

            if self.args.list_tags:
                self.list_available_tags(all_rules)
            if self.args.controls:
                self.check_controls(all_rules)

            found_rules = self.get_matching_rules(all_rules)
            if not found_rules:
                print("No rules found for the keyword provided. Available tags:")
                self.list_available_tags(all_rules)
                return

            mscp_data = self.load_yaml_file(os.path.join(self.includes_dir, 'mscp-data.yaml'))
            version_data = self.load_yaml_file(os.path.join(self.root_dir, "VERSION.yaml"))
            self.generate_baseline(found_rules, mscp_data, version_data)

        except RuntimeError as e:
            print(f"Error: {str(e)}")
        finally:
            os.chdir(self.original_wd)

def main():
    """Entry point for the script."""
    generator = BaselineGenerator()
    generator.run()

if __name__ == "__main__":
    main()