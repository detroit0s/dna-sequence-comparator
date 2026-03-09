#include <cstdio>
#include <cstdlib>
#include <cstring>

#include "utils_fasta.h"
#include "utils_csv.h"


// Hypothèses de la phase 1 (voir énoncé)
static const size_t MAX_SEQ_NAME_LEN = 101; // 100 caractères + '\0'
static const size_t MAX_SEQ_LEN = 1000;     // max 1000 caractères

static const char ALPHABET[] = "ACGNT";

static bool is_valid_base(char c) {
    for (size_t i = 0; ALPHABET[i] != '\0'; ++i) {
        if (c == ALPHABET[i]) return true;
    }
    return false;
}

static void close_all(FILE* fp_ref, FILE* fp_seq, FILE* fp_out) {
    if (fp_ref) fasta_close(fp_ref);
    if (fp_seq) fasta_close(fp_seq);
    if (fp_out) csv_close(fp_out);
}


int main(int argc, char* argv[]) {
    
    if (argc != 4) {
        fprintf(stderr, "Usage: %s chemin_ref_seq chemin_seq chemin_output\n", argv[0]);
        return -1;
    }
    const char* path_ref = argv[1];
    const char* path_seq = argv[2];
    const char* path_out = argv[3];

    // --- Ouverture des fichiers FASTA ---
    FILE* fp_ref = nullptr;
    FILE* fp_seq = nullptr;
    FILE* fp_out = nullptr;

    char name_ref[MAX_SEQ_NAME_LEN];
    char name_seq[MAX_SEQ_NAME_LEN];

    FastaStatus fs;

    fs = fasta_open_and_read_header(path_ref, &fp_ref, name_ref, MAX_SEQ_NAME_LEN);
    if (fs != FASTA_OK) {
        fprintf(stderr, "Erreur: impossible d'ouvrir ou de lire l'en-tête du fichier de référence '%s' (code %d).\n", path_ref, fs);
        close_all(fp_ref, fp_seq, fp_out);
        return -1;
    }

    fs = fasta_open_and_read_header(path_seq, &fp_seq, name_seq, MAX_SEQ_NAME_LEN);
    if (fs != FASTA_OK) {
        fprintf(stderr, "Erreur: impossible d'ouvrir ou de lire l'en-tête du fichier de séquence '%s' (code %d).\n", path_seq, fs);
        close_all(fp_ref, fp_seq, fp_out);
        return -1;
    }

    // Vérifier que les noms sont identiques
    if (std::strcmp(name_ref, name_seq) != 0) {
        fprintf(stderr, "Erreur: les noms de séquences diffèrent ('%s' vs '%s').\n", name_ref, name_seq);
        close_all(fp_ref, fp_seq, fp_out);
        return -1;
    }

    // --- Ouverture du fichier CSV ---
    CsvStatus cs;
    cs = csv_open(path_out, &fp_out);
    if (cs != CSV_OK) {
        fprintf(stderr, "Erreur: impossible d'ouvrir le fichier de sortie '%s' (code %d).\n", path_out, cs);
        close_all(fp_ref, fp_seq, fp_out);
        return -1;
    }

    // --- Lecture des séquences en mémoire ---
    char seq_ref[MAX_SEQ_LEN];
    char seq[MAX_SEQ_LEN];

    size_t n_ref = 0;
    size_t n_seq = 0;

    fs = fasta_read_bases(fp_ref, seq_ref, MAX_SEQ_LEN, &n_ref);
    if (fs != FASTA_OK) {
        fprintf(stderr, "Erreur: échec de la lecture des bases de la séquence de référence (code %d).\n", fs);
        close_all(fp_ref, fp_seq, fp_out);
        return -1;
    }

    fs = fasta_read_bases(fp_seq, seq, MAX_SEQ_LEN, &n_seq);
    if (fs != FASTA_OK) {
        fprintf(stderr, "Erreur: échec de la lecture des bases de la séquence à comparer (code %d).\n", fs);
        close_all(fp_ref, fp_seq, fp_out);
        return -1;
    }

    // Vérifier que les longueurs sont identiques
    if (n_ref != n_seq) {
        fprintf(stderr, "Erreur: les séquences ont des longueurs différentes (%zu vs %zu).\n", n_ref, n_seq);
        close_all(fp_ref, fp_seq, fp_out);
        return -1;
    }

    // Vérifier l'alphabet et comparer les séquences
    for (size_t i = 0; i < n_ref; ++i) {
        if (!is_valid_base(seq_ref[i])) {
            fprintf(stderr, "Erreur: caractère invalide '%c' à la position %zu dans la séquence de référence.\n", seq_ref[i], i);
            close_all(fp_ref, fp_seq, fp_out);
            return -1;
        }
        if (!is_valid_base(seq[i])) {
            fprintf(stderr, "Erreur: caractère invalide '%c' à la position %zu dans la séquence à comparer.\n", seq[i], i);
            close_all(fp_ref, fp_seq, fp_out);
            return -1;
        }
        if (seq_ref[i] != seq[i]) {
            cs = csv_write_mutation(fp_out, name_ref, i, seq_ref[i], seq[i]);
            if (cs != CSV_OK) {
                fprintf(stderr, "Erreur: échec de l'écriture dans le fichier CSV (code %d).\n", cs);
                close_all(fp_ref, fp_seq, fp_out);
                return -1;
            }
        }
    }

    // --- Fermeture des fichiers ---
    close_all(fp_ref, fp_seq, fp_out);

    return 0;
}
