## Log Leaks

**Category:** General Skills  
**Difficulty:** Easy

### Description
Server logs are leaking fragments of the flag. The fragments are scattered and repeated.

### Solution
1. Extract all `FLAGPART` entries from the log file
2. Remove duplicate fragments while keeping their order
3. Concatenate fragments to reconstruct the full flag

### Tools Used
- Python
- Regex
- OrderedDict

### Flag
