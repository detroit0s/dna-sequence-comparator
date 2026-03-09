import sys
from typing import Tuple, Optional, TextIO

ALPHABET = {'A', 'C', 'G', 'N', 'T'}
MAX_SEQ_LEN = 1000

# ---------------------------------------------------------------------
# Helpers FASTA
# ---------------------------------------------------------------------

def fasta_open_and_read_header(path: str) -> Tuple[Optional[TextIO], Optional[str]]:
    """
    Ouvre un fichier FASTA et lit l'en-tête.
    Retourne (fp, name) où :
      - fp est un fichier ouvert en lecture, positionné juste après l'en-tête
      - name est le nom de séquence sans le '>'
    En cas d'erreur : affiche un message et retourne (None, None).
    """
    try:
        fp = open(path, "r")
    except OSError:
        print(f"Erreur: impossible d'ouvrir le fichier '{path}'.", file=sys.stderr)
        return None, None

    header = fp.readline()
    if header == "":
        print(f"Erreur: le fichier '{path}' est vide.", file=sys.stderr)
        fp.close()
        return None, None

    header = header.strip()
    if not header.startswith(">"):
        print(f"Erreur: format FASTA invalide dans '{path}' (en-tête manquant).", file=sys.stderr)
        fp.close()
        return None, None

    name = header[1:]
    if not name:
        print(f"Erreur: nom de séquence vide dans '{path}'.", file=sys.stderr)
        fp.close()
        return None, None

    return fp, name


def fasta_read_bases(fp: Optional[TextIO], n: int) -> Optional[str]:
    """
    Lit au maximum n bases depuis le fichier fp.
    Ignore les caractères '\\n' et '\\r'.

    Retourne une chaîne contenant au plus n caractères.
    Retourne "" si fin de séquence.
    Retourne None en cas d'erreur de format (ex: second '>').
    """
    if fp is None:
        return None

    bases = []

    while len(bases) < n:
        c = fp.read(1)

        if c == "":
            # EOF
            break

        if c == "\n" or c == "\r":
            continue

        if c == ">":
            print("Erreur: format FASTA invalide (plusieurs séquences détectées).", file=sys.stderr)
            return None

        bases.append(c)

    return "".join(bases)


# ---------------------------------------------------------------------
# Helpers CSV
# ---------------------------------------------------------------------

def csv_open(path: str) -> Optional[TextIO]:
    """
    Ouvre le fichier CSV de sortie en écriture.
    Retourne fp ou None si erreur.
    """
    try:
        return open(path, "w")
    except OSError:
        print(f"Erreur: impossible d'ouvrir le fichier de sortie '{path}'.", file=sys.stderr)
        return None


def csv_write_mutation(fp: TextIO, name: str, pos: int, ref: str, alt: str) -> None:
    """
    Écrit une substitution sur une ligne CSV.
    """
    fp.write(f"{name},{pos},{ref},{alt}\n")


def csv_close(fp: Optional[TextIO]) -> None:
    if fp is not None:
        fp.close()


# ---------------------------------------------------------------------
# Programme principal
# ---------------------------------------------------------------------

def main():
    if len(sys.argv) != 4:
        print("Usage: python compare_strings.py chemin_ref_seq chemin_seq chemin_output",
              file=sys.stderr)
        return 1

    path_ref = sys.argv[1]
    path_seq = sys.argv[2]
    path_out = sys.argv[3]

    # --- Ouverture des fichiers FASTA ---
    fp_ref, name_ref = fasta_open_and_read_header(path_ref)
    if fp_ref is None:
        return 1

    fp_seq, name_seq = fasta_open_and_read_header(path_seq)
    if fp_seq is None:
        fp_ref.close()
        return 1

    # Vérifier que les noms sont identiques
    if name_ref != name_seq:
        print(f"Erreur: les noms de séquences diffèrent ('{name_ref}' vs '{name_seq}').",
              file=sys.stderr)
        fp_ref.close()
        fp_seq.close()
        return 1

    # --- Ouverture du CSV ---
    fp_out = csv_open(path_out)
    if fp_out is None:
        fp_ref.close()
        fp_seq.close()
        return 1

    # --- Lecture des séquences (phase 1 : chargement complet autorisé) ---
    seq_ref = fasta_read_bases(fp_ref, MAX_SEQ_LEN)
    if seq_ref is None:
        csv_close(fp_out)
        fp_ref.close()
        fp_seq.close()
        return 1

    seq = fasta_read_bases(fp_seq, MAX_SEQ_LEN)
    if seq is None:
        csv_close(fp_out)
        fp_ref.close()
        fp_seq.close()
        return 1

    # Vérifier que les longueurs sont identiques
    if len(seq_ref) != len(seq):
        print(f"Erreur: les séquences ont des longueurs différentes ({len(seq_ref)} vs {len(seq)}).",
              file=sys.stderr)
        csv_close(fp_out)
        fp_ref.close()
        fp_seq.close()
        return 1

    # Vérifier l'alphabet et comparer les séquences
    for i in range(len(seq_ref)):
        if seq_ref[i] not in ALPHABET:
            print(f"Erreur: caractère invalide '{seq_ref[i]}' à la position {i} "
                  f"dans la séquence de référence.", file=sys.stderr)
            csv_close(fp_out)
            fp_ref.close()
            fp_seq.close()
            return 1
        if seq[i] not in ALPHABET:
            print(f"Erreur: caractère invalide '{seq[i]}' à la position {i} "
                  f"dans la séquence à comparer.", file=sys.stderr)
            csv_close(fp_out)
            fp_ref.close()
            fp_seq.close()
            return 1
        if seq_ref[i] != seq[i]:
            csv_write_mutation(fp_out, name_ref, i, seq_ref[i], seq[i])

    # --- Fermeture des fichiers ---
    csv_close(fp_out)
    fp_ref.close()
    fp_seq.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
