## 📌 Challenge: Grep is Good

**Category:** General Skills  
**Difficulty:** Easy  
**Platform:** picoCTF

---

### 📝 Challenge Description
We are given a text file containing many lines of data. The flag is hidden somewhere inside the file.

Our goal is to **locate the picoCTF flag efficiently using Linux command-line tools**.

---

### 🔍 Analysis
The flag format is known:


Instead of manually reading the file, we can utilize the Linux `grep` command to search for patterns inside files.

---

### 🛠 Solution

#### Command Used:
```bash
grep -o "picoCTF{.*}" file.txt
```
🎯 Takeaways
Learned how to use grep for pattern matching
Understood regex basics for CTF use-cases
Demonstrated efficient Linux file analysis
This skill is useful for log analysis, forensics, and pentesting
