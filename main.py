import os
import yaml
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import List, Optional
from arg_parser import create_args
from rule_handler import collect_rules, get_controls, output_baseline, odv_query
from utils import parse_authors, append_authors, available_tags, sanitised_input

class BaselineGenerator:
    """Generates security baselines, applies fixes, and provides a GUI for macOS based on command-line arguments."""

    def __init__(self):
        """Initialize with parsed arguments and dynamic directory paths."""
        self.args = create_args()
        self.root_dir = self.args.root_dir or os.getcwd()
        self.includes_dir = os.path.join(self.root_dir, 'includes')
        self.build_dir = os.path.join(self.root_dir, 'build', 'baselines')
        self.original_wd = os.getcwd()

    def setup_directories(self) -> None:
        """Set up working directory and create build directory if needed."""
        try:
            os.chdir(self.root_dir)
            os.makedirs(self.build_dir, exist_ok=True)
        except FileNotFoundError:
            raise RuntimeError(f"Root directory not found: {self.root_dir}")
        except PermissionError:
            raise RuntimeError(f"Permission denied accessing directory: {self.root_dir}")

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
        """Display available tags."""
        available_tags(rules)

    def check_controls(self, rules: List) -> None:
        """Check for missing NIST 800-53 controls in rules."""
        baselines = self.load_yaml_file(os.path.join(self.includes_dir, '800-53_baselines.yaml'))
        included_controls = get_controls(rules)
        needed_controls = list(dict.fromkeys(baselines['low']))  # Remove duplicates
        
        for control in needed_controls:
            if control not in included_controls:
                print(f'{control} missing from any rule, needs a rule or supplemental inclusion')

    def get_matching_rules(self, all_rules: List, keyword: str) -> List:
        """Filter rules based on the provided keyword."""
        return [rule for rule in all_rules if keyword in rule.rule_tags or keyword == "all_rules"]

    def apply_fixes(self, rules: List, keyword: str) -> None:
        """Apply fix commands for rules matching the keyword."""
        print(f"Applying fixes for rules with tag '{keyword}'...")
        for rule in rules:
            fix_cmd = rule.rule_fix.strip()
            if not fix_cmd or fix_cmd == "missing":
                print(f"No fix defined for rule '{rule.rule_id}'")
                continue
            
            print(f"\nRule: {rule.rule_id}")
            print(f"Description: {rule.rule_discussion}")
            print(f"Fix Command: {fix_cmd}")
            confirm = sanitised_input(f"Apply this fix? [Y/n]: ", str.lower, range_=('y', 'n'), default_="n")
            if confirm != 'y':
                print(f"Skipping fix for '{rule.rule_id}'")
                continue

            # Check if sudo is required (most macOS fixes need it)
            if 'sudo' in fix_cmd.lower() or any(cmd in fix_cmd for cmd in ['/usr/bin/pwpolicy', '/usr/sbin/spctl', '/usr/bin/defaults']):
                if os.geteuid() != 0:
                    print(f"Error: Fix for '{rule.rule_id}' requires root privileges. Please run with sudo.")
                    continue
                cmd = fix_cmd  # Already includes sudo if specified
            else:
                cmd = fix_cmd

            try:
                result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                print(f"Successfully applied fix for '{rule.rule_id}': {result.stdout}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to apply fix for '{rule.rule_id}': {e.stderr}")
            except Exception as e:
                print(f"Unexpected error applying fix for '{rule.rule_id}': {str(e)}")

    def generate_baseline(self, rules: List, mscp_data: dict, version_data: dict, keyword: str = None) -> None:
        """Generate and write the baseline file."""
        keyword = keyword or self.args.keyword
        established_benchmarks = ['stig', 'cis_lvl1', 'cis_lvl2']
        benchmark = keyword if any(bm in keyword for bm in established_benchmarks) else "recommended"
        
        authors = (parse_authors(mscp_data['authors'][keyword]) 
                  if keyword in mscp_data['authors'] 
                  else "|===\n  |Name|Organization\n  |===\n")
        
        full_title = (f"{mscp_data['titles'][keyword]}" 
                     if keyword in mscp_data['titles'] and not self.args.tailor 
                     else f"{keyword}")

        if self.args.tailor:
            self._generate_tailored_baseline(rules, benchmark, authors, full_title, version_data, keyword)
        else:
            self._generate_standard_baseline(rules, benchmark, authors, full_title, version_data, keyword)

    def _generate_tailored_baseline(self, rules: List, benchmark: str, authors: str, title: str, version: dict, keyword: str) -> None:
        """Handle tailored baseline generation with user input."""
        tailored_filename = self._get_sanitised_input(
            f'Enter a name for your tailored benchmark or press Enter for default ({keyword}): ',
            default_=keyword
        )
        custom_author_name = self._get_sanitised_input('Enter your name: ')
        custom_author_org = self._get_sanitised_input('Enter your organization: ')
        
        authors = append_authors(authors, custom_author_name, custom_author_org)
        baseline_string = (f"{tailored_filename.upper()} (Tailored from {keyword.upper()})")
        tailored_rules = odv_query(rules, benchmark)
        self._write_baseline(tailored_filename, tailored_rules, version, baseline_string, benchmark, authors, title)

    def _generate_standard_baseline(self, rules: List, benchmark: str, authors: str, title: str, version: dict, keyword: str) -> None:
        """Handle standard baseline generation."""
        self._write_baseline(keyword, rules, version, "", benchmark, authors, title)

    def _write_baseline(self, filename: str, rules: List, version: dict, baseline_string: str, 
                       benchmark: str, authors: str, title: str) -> None:
        """Write the baseline to a YAML file."""
        output_path = os.path.join(self.build_dir, f"{filename}.yaml")
        try:
            with open(output_path, 'w') as output_file:
                output_file.write(output_baseline(rules, version, baseline_string, benchmark, authors, title))
            print(f"Baseline written to {output_path}")
        except IOError as e:
            raise RuntimeError(f"Error writing baseline to {output_path}: {str(e)}")

    def _get_sanitised_input(self, prompt: str, default_: Optional[str] = None) -> str:
        """Get validated user input with an optional default."""
        return sanitised_input(prompt, str, default_=default_)

    def interactive_mode(self, all_rules: List, mscp_data: dict, version_data: dict) -> None:
        """Run an interactive command prompt."""
        print("Entering interactive mode. Type 'help' for commands, 'exit' to quit.")
        while True:
            command = input("mscp> ").strip().lower()
            if command in ['exit', 'quit']:
                print("Exiting interactive mode.")
                break
            elif command == 'help':
                print("Available commands:")
                print("  list                - List all available tags")
                print("  generate <tag>      - Generate a baseline for <tag>")
                print("  check               - Check NIST 800-53 control coverage")
                print("  tailor <tag>        - Tailor a baseline for <tag>")
                print("  apply <tag>         - Apply fixes for rules with <tag>")
                print("  exit/quit           - Exit interactive mode")
            elif command == 'list':
                self.list_available_tags(all_rules)
            elif command == 'check':
                self.check_controls(all_rules)
            elif command.startswith('generate '):
                tag = command.split(' ', 1)[1]
                rules = self.get_matching_rules(all_rules, tag)
                if rules:
                    self._generate_standard_baseline(rules, tag, parse_authors(mscp_data['authors'].get(tag, {})), 
                                                     f"{mscp_data['titles'].get(tag, tag)}", version_data, tag)
                else:
                    print(f"No rules found for tag '{tag}'. Available tags:")
                    self.list_available_tags(all_rules)
            elif command.startswith('tailor '):
                tag = command.split(' ', 1)[1]
                rules = self.get_matching_rules(all_rules, tag)
                if rules:
                    self.args.tailor = True
                    self._generate_tailored_baseline(rules, tag, parse_authors(mscp_data['authors'].get(tag, {})), 
                                                     f"{mscp_data['titles'].get(tag, tag)}", version_data, tag)
                    self.args.tailor = False
                else:
                    print(f"No rules found for tag '{tag}'. Available tags:")
                    self.list_available_tags(all_rules)
            elif command.startswith('apply '):
                tag = command.split(' ', 1)[1]
                rules = self.get_matching_rules(all_rules, tag)
                if rules:
                    self.apply_fixes(rules, tag)
                else:
                    print(f"No rules found for tag '{tag}'. Available tags:")
                    self.list_available_tags(all_rules)
            else:
                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

    def gui_mode(self, all_rules: List, mscp_data: dict, version_data: dict) -> None:
        """Run a graphical user interface using Tkinter."""
        root = tk.Tk()
        root.title("macOS Security Compliance Tool")

        # List Tags Button
        def list_tags():
            tags = "\n".join(sorted({tag for rule in all_rules for tag in rule.rule_tags} | {"all_rules"}))
            messagebox.showinfo("Available Tags", tags)

        tk.Button(root, text="List Tags", command=list_tags).pack(pady=5)

        # Generate Baseline Button
        def generate_baseline():
            tag = simpledialog.askstring("Generate Baseline", "Enter tag (e.g., 'stig'): ")
            if tag:
                rules = self.get_matching_rules(all_rules, tag)
                if rules:
                    filepath = os.path.join(self.build_dir, f"{tag}.yaml")
                    with open(filepath, 'w') as f:
                        f.write(output_baseline(rules, version_data, "", tag, parse_authors(mscp_data['authors'].get(tag, {})), f"{mscp_data['titles'].get(tag, tag)}"))
                    messagebox.showinfo("Success", f"Baseline written to {filepath}")
                else:
                    messagebox.showerror("Error", f"No rules found for tag '{tag}'")

        tk.Button(root, text="Generate Baseline", command=generate_baseline).pack(pady=5)

        # Check Controls Button
        def check_controls():
            baselines = self.load_yaml_file(os.path.join(self.includes_dir, '800-53_baselines.yaml'))
            included_controls = get_controls(all_rules)
            needed_controls = list(dict.fromkeys(baselines['low']))
            missing = [control for control in needed_controls if control not in included_controls]
            if missing:
                messagebox.showwarning("Missing Controls", "\n".join(missing))
            else:
                messagebox.showinfo("Controls", "All required controls are covered")

        tk.Button(root, text="Check Controls", command=check_controls).pack(pady=5)

        # Tailor Baseline Button
        def tailor_baseline():
            tag = simpledialog.askstring("Tailor Baseline", "Enter tag (e.g., 'stig'): ")
            if tag:
                rules = self.get_matching_rules(all_rules, tag)
                if rules:
                    tailored_filename = simpledialog.askstring("Tailor Baseline", "Enter a name for your tailored benchmark or press Enter for default: ", initialvalue=tag)
                    custom_author_name = simpledialog.askstring("Tailor Baseline", "Enter your name: ")
                    custom_author_org = simpledialog.askstring("Tailor Baseline", "Enter your organization: ")
                    if not tailored_filename:
                        tailored_filename = tag
                    authors = append_authors(parse_authors(mscp_data['authors'].get(tag, {})), custom_author_name, custom_author_org)
                    baseline_string = f"{tailored_filename.upper()} (Tailored from {tag.upper()})"
                    tailored_rules = []
                    for rule in rules:
                        include = messagebox.askyesno("Include Rule", f"Include rule '{rule.rule_id}'?\nDescription: {rule.rule_discussion}")
                        if include:
                            tailored_rules.append(rule)
                    filepath = os.path.join(self.build_dir, f"{tailored_filename}.yaml")
                    with open(filepath, 'w') as f:
                        f.write(output_baseline(tailored_rules, version_data, baseline_string, tag, authors, f"{mscp_data['titles'].get(tag, tag)}"))
                    messagebox.showinfo("Success", f"Tailored baseline written to {filepath}")
                else:
                    messagebox.showerror("Error", f"No rules found for tag '{tag}'")

        tk.Button(root, text="Tailor Baseline", command=tailor_baseline).pack(pady=5)

        # Apply Fixes Button
        def apply_fixes():
            tag = simpledialog.askstring("Apply Fixes", "Enter tag (e.g., 'stig'): ")
            if tag:
                rules = self.get_matching_rules(all_rules, tag)
                if rules:
                    for rule in rules:
                        fix_cmd = rule.rule_fix.strip()
                        if not fix_cmd or fix_cmd == "missing":
                            continue
                        if messagebox.askyesno("Apply Fix", f"Apply fix for '{rule.rule_id}'?\nCommand: {fix_cmd}"):
                            try:
                                result = subprocess.run(fix_cmd, shell=True, check=True, capture_output=True, text=True)
                                messagebox.showinfo("Success", f"Applied fix for '{rule.rule_id}': {result.stdout}")
                            except subprocess.CalledProcessError as e:
                                messagebox.showerror("Error", f"Failed to apply fix for '{rule.rule_id}': {e.stderr}")
                            except Exception as e:
                                messagebox.showerror("Error", f"Unexpected error: {str(e)}")
                else:
                    messagebox.showerror("Error", f"No rules found for tag '{tag}'")

        tk.Button(root, text="Apply Fixes", command=apply_fixes).pack(pady=5)

        root.mainloop()

    def run(self) -> None:
        """Execute the main logic based on arguments."""
        try:
            self.setup_directories()
            all_rules = collect_rules()

            if self.args.list_tags:
                self.list_available_tags(all_rules)
                return
            if self.args.controls:
                self.check_controls(all_rules)
                return
            if self.args.interactive:
                mscp_data = self.load_yaml_file(os.path.join(self.includes_dir, 'mscp-data.yaml'))
                version_data = self.load_yaml_file(os.path.join(self.root_dir, "VERSION.yaml"))
                self.interactive_mode(all_rules, mscp_data, version_data)
                return
            if self.args.gui:
                mscp_data = self.load_yaml_file(os.path.join(self.includes_dir, 'mscp-data.yaml'))
                version_data = self.load_yaml_file(os.path.join(self.root_dir, "VERSION.yaml"))
                self.gui_mode(all_rules, mscp_data, version_data)
                return

            found_rules = self.get_matching_rules(all_rules, self.args.keyword)
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
