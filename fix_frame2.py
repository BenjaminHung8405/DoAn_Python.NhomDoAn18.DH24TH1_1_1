#!/usr/bin/env python3
"""Fix indentation issues in Frame2.py"""

# Read the file
with open('Pages/UserAuthentication/Frame2.py', 'r') as f:
    lines = f.readlines()

# Find registerNow function and fix indentation
fixed_lines = []
in_registernow = False
for i, line in enumerate(lines):
    if 'def registerNow(self):' in line:
        in_registernow = True
        fixed_lines.append(line)
    elif in_registernow and (line.strip().startswith('def ') or (i > 0 and not line.strip() and i < len(lines)-1 and lines[i+1].strip().startswith('class '))):
        # End of registerNow function
        in_registernow = False
        fixed_lines.append(line)
    elif in_registernow:
        # Inside registerNow - ensure proper indentation
        stripped = line.lstrip()
        if not stripped:  # Empty line
            fixed_lines.append(line)
        elif stripped.startswith('#'):
            # Comment should have 2 tabs
            fixed_lines.append('\t\t' + stripped)
        elif stripped.startswith(('if ', 'elif ', 'else:', 'for ', 'while ', 'with ', 'try:', 'except', 'finally:', 'from ', 'import ', 'global ', 'data3', 'success')):
            # Statement at function body level - 2 tabs
            fixed_lines.append('\t\t' + stripped)
        elif stripped.startswith(('self.result', 'return', 'messagebox')):
            # Inside if block - 3 tabs
            fixed_lines.append('\t\t\t' + stripped)
        elif stripped.startswith(('username', 'password', 'phone', 'email')) and '=' in stripped:
            # Variable assignments - 2 tabs
            fixed_lines.append('\t\t' + stripped)
        else:
            # Keep original indentation if unsure
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

# Write back
with open('Pages/UserAuthentication/Frame2.py', 'w') as f:
    f.writelines(fixed_lines)

print("✓ Fixed indentation in Frame2.py")
