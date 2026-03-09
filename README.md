# dna-sequence-comparator

> 🇫🇷 Version française ci-dessous | 🇬🇧 English version below

---

## 🇬🇧 English

### DNA Sequence Comparator

A command-line tool that compares two DNA sequences in FASTA format and outputs detected substitutions (single-character differences) to a CSV file. Implemented in both **C++** and **Python** as part of the INFO-F-105 course project at ULB.

---

### 📁 File Structure

```
.
├── compare_strings.cpp   # Main C++ program
├── compare_strings.py    # Main Python program
├── utils_fasta.h         # FASTA utility header
├── utils_fasta.cpp       # FASTA utility implementation
├── utils_csv.h           # CSV utility header
├── utils_csv.cpp         # CSV utility implementation
├── Makefile              # Build file for C++
└── rapport_phase1.pdf    # Project report (Phase 1)
```

---

### ⚙️ How to Compile & Run

#### C++

**Compile:**
```bash
make
```

**Run:**
```bash
./compare_strings path/to/reference.fasta path/to/sequence.fasta path/to/output.csv
```

**Clean:**
```bash
make clean
```

#### Python

```bash
python compare_strings.py path/to/reference.fasta path/to/sequence.fasta path/to/output.csv
```

---

### 📋 Examples

**reference.fasta**
```
>chr1
NNNNACCGTACT
```

**sequence.fasta**
```
>chr1
NNNNTCCGTACG
```

**output.csv**
```
chr1,4,A,T
chr1,11,T,G
```

Each line represents a substitution: `sequence_name, position (0-indexed), ref_base, alt_base`.

---

### ❌ Error Handling

The program handles the following error cases and prints an explicit message to `stderr`:
- File not found or unreadable
- Invalid FASTA format
- Sequence names differ between the two files
- Invalid character in sequence (only `A`, `C`, `G`, `N`, `T` are allowed)
- Sequences have different lengths

---

### 🔧 Compilation Flags

```
-std=c++17 -Wall -Wextra -Wpedantic -D_GNU_SOURCE -Werror=all -O2
```

---
---

## 🇫🇷 Français

### Comparateur de séquences ADN

Un outil en ligne de commande qui compare deux séquences d'ADN au format FASTA et écrit les substitutions détectées (différences caractère par caractère) dans un fichier CSV. Implémenté en **C++** et en **Python** dans le cadre du projet du cours INFO-F-105 à l'ULB.

---

### 📁 Structure des fichiers

```
.
├── compare_strings.cpp   # Programme principal C++
├── compare_strings.py    # Programme principal Python
├── utils_fasta.h         # En-tête utilitaires FASTA
├── utils_fasta.cpp       # Implémentation utilitaires FASTA
├── utils_csv.h           # En-tête utilitaires CSV
├── utils_csv.cpp         # Implémentation utilitaires CSV
├── Makefile              # Fichier de compilation C++
└── rapport_phase1.pdf    # Rapport du projet (Phase 1)
```

---

### ⚙️ Compilation et exécution

#### C++

**Compiler :**
```bash
make
```

**Exécuter :**
```bash
./compare_strings chemin/vers/reference.fasta chemin/vers/sequence.fasta chemin/vers/sortie.csv
```

**Nettoyer :**
```bash
make clean
```

#### Python

```bash
python compare_strings.py chemin/vers/reference.fasta chemin/vers/sequence.fasta chemin/vers/sortie.csv
```

---

### 📋 Exemples

**reference.fasta**
```
>chr1
NNNNACCGTACT
```

**sequence.fasta**
```
>chr1
NNNNTCCGTACG
```

**sortie.csv**
```
chr1,4,A,T
chr1,11,T,G
```

Chaque ligne représente une substitution : `nom_séquence, position (index à partir de 0), base_ref, base_alt`.

---

### ❌ Gestion des erreurs

Le programme gère les cas d'erreur suivants et affiche un message explicite sur `stderr` :
- Fichier introuvable ou illisible
- Format FASTA invalide
- Noms de séquences différents entre les deux fichiers
- Caractère invalide dans une séquence (seuls `A`, `C`, `G`, `N`, `T` sont autorisés)
- Séquences de longueurs différentes

---

### 🔧 Options de compilation

```
-std=c++17 -Wall -Wextra -Wpedantic -D_GNU_SOURCE -Werror=all -O2
```

---

*INFO-F-105 — Langages de programmation 1 — ULB 2025/2026*  
*Diego Meño Toulouse — 000630151*
