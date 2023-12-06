#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE 256

// Function to allocate memory for a matrix
double** create_matrix(int size) {
    double** matrix = (double**)malloc(size * sizeof(double*));
    for (int i = 0; i < size; i++) {
        matrix[i] = (double*)malloc(size * sizeof(double));
    }
    return matrix;
}

// Function to free memory of a matrix
void free_matrix(double** matrix, int size) {
    for (int i = 0; i < size; i++) {
        free(matrix[i]);
    }
    free(matrix);
}

// Function to fill a matrix with random values
void fill_matrix(double** matrix, int size) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            matrix[i][j] = (double)rand() / RAND_MAX;
        }
    }
}

// Function for matrix multiplication
void matrix_multiply(double** a, double** b, double** result, int size) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            result[i][j] = 0;
            for (int k = 0; k < size; k++) {
                result[i][j] += a[i][k] * b[k][j];
            }
        }
    }
}

int main() {
    double **A, **B, **C;
    clock_t start, end;
    double cpu_time_used;

    srand((unsigned int)time(NULL));

    // Allocate memory
    A = create_matrix(SIZE);
    B = create_matrix(SIZE);
    C = create_matrix(SIZE);

    // Fill matrices with random values
    fill_matrix(A, SIZE);
    fill_matrix(B, SIZE);

    int N = 20;
    start = clock();
    for (int i = 0; i < N; i++) {
        matrix_multiply(A, B, C, SIZE);
    }
    end = clock();

    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;

    printf("Dotted two %dx%d matrices in %f s.\n", SIZE, SIZE, cpu_time_used / N);

    // Free memory
    free_matrix(A, SIZE);
    free_matrix(B, SIZE);
    free_matrix(C, SIZE);

    return 0;
}
