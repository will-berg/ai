EPSILON = 0.00001 # small constant added to denominators to prevent divide by 0 errors

def read_matrix():
    # Reads a matrix from stdin
    # Returns: the read matrix
    M_input = input().split()
    M = []
    M_rows = int(M_input[0])
    M_cols = int(M_input[1])

    next = 2
    for i in range(0, M_rows):
        M.append([])
        for j in range(0, M_cols):
            M[i].append(float(M_input[next]))
            next += 1
        
    return M


def read_observations():
    O_input = input().split()
    O = []
    for i in range(0, int(O_input[0])):
         O.append(int(O_input[i + 1]))

    return int(O_input[0]), O


def matrix_mult(left, right):
    # Computes m = lext x right, assuming they are compatible
    # Returns: m
    m = []
    l_rows = len(left)
    l_cols = len(left[0])
    r_cols = len(right[0])

    for i in range(0, l_rows):
        m.append([])
        for j in range(0, r_cols):
            m[i].append(0)

    for i in range(0, l_rows):
        for j in range(0, r_cols): 
            for k in range(0, l_cols):
                m[i][j] += left[i][k] * right[k][j]

    return m


def alpha_pass(A, B, pi, T, O):
    # Returns: c, α

    N = len(A) # Number of states

    # α_t(i) is the probability of observing o_1:t and being in state i
    alpha = []

    # α_0
    alpha.append([])

    # c_0..c_T
    # c is a vector of scaling factors used to prevent underflow
    c = [0 for _ in range(0, T)]

    # The α-pass
    # compute α_0(i)
    for i in range(0, N):
        alpha[0].append(pi[i] * B[i][O[0]])
        c[0] += alpha[0][i]

    # scale the α_0(i)
    c[0] += EPSILON
    c[0] = 1 / c[0]
    for i in range(0, N):
        alpha[0][i] *= c[0]

    # compute α_t(i)
    for t in range(1, T):
        alpha.append([])
        for i in range(0, N):
            alpha[t].append(0)
            for j in range(0, N):
                alpha[t][i] += alpha[t-1][j] * A[j][i]
            alpha[t][i] *= B[i][O[t]]
            c[t] += alpha[t][i]
        # scale α_t(i)
        c[t] += EPSILON
        c[t] = 1 / c[t]
        for i in range(0, N):
            alpha[t][i] *= c[t]

    return c, alpha


def beta_pass(A, B, T, O, c):
    # In the β-pass we traverse the observations backwards

    N = len(A) # Number of states

    # β_t(i) is the probability of all future observations o_t+1:T given state i
    beta = [[0 for _ in range(0, N)] for _ in range(0, T)]

    # Let β_T-1(i) = 1, scaled by c_T-1
    for i in range(0, N):
        beta[T-1][i] = c[T-1]

    for t in range(T-2, -1, -1):
        for i in range(0, N):
            for j in range(0, N):
                beta[t][i] += A[i][j]*B[j][O[t+1]]*beta[t+1][j]
            # scale β_t(i) with same scale factor as α_t(i)
            beta[t][i] *= c[t]

    return beta


def compute_gamma(a, b, T, O, alpha, beta):
    N = len(a) # Number of states

    # di_gamma is the probability of being in state i at t, and being in state j at t+1,
    # given every observation o_1:T
    di_gamma = [[[0 for _ in range(0, N)] for _ in range(0, N)] for _ in range(0, T)]
    
    # gamma is the probability of being in state i at t, given every observation o_1:T
    gamma = [[0 for _ in range(0, N)] for _ in range(0, T)]

    for t in range(0, T-1):
        for i in range(0, N):
            for j in range(0, N):
                di_gamma[t][i][j] = alpha[t][i]*a[i][j]*b[j][O[t+1]]*beta[t+1][j]
                gamma[t][i] += di_gamma[t][i][j]
    for i in range(0, N):
        gamma[T-1][i] = alpha[T-1][i]

    return di_gamma, gamma
