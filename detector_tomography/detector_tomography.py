"""Main module."""
import numpy as np
import cvxpy as cp

from scipy.linalg import pinv
from scipy.special import factorial

def photon_number_cutoff(alpha_vec, prob_thres=0.999999):
    """
    Estimate a photon number cutoff to be used in calculations.

    Parameters
    ----------
        alpha_vec : list of floats
            Alpha values for coherent states used in tomographic reconstruction.
        prob_thres : float
            Threshold value for errors due to truncation of coherent state.
    Notes
    -----
        Function seems to break for alpha > 2.9
    """
    # for the largest coherent state find the number cuttoff "Nmax" that
    # ensures \sum_{n=0}^Nmax Pr(n|alpha) >= prob_thres
    alpha_max = max(alpha_vec)
    prob_cut = []
    for idx in range(0, 150):
        prob_cut.append(sum([prob_n_given_alpha(n, alpha_max) for n in range(0, idx)]))
    # find the index of the first element greater than the threshold
    Nmax = prob_cut.index(next(x for x in prob_cut if x > prob_thres))
    return Nmax


def prob_n_given_alpha(k, alpha):
    """
    Probability of detecting n photons given a coherent state |alpha>.

    That is the Poissonian distribution of coherent state in number basis
    Pr(n|alpha) = |<n|alpha>|^2 where <n> = |alpha|^2.

    Parameters
    ----------
        k : int
            Number of photons.
        alpha : float
        Coherent state amplitude

    Returns
    -------
        Pr(n|alpha)

    Notes
    -----
        Factorial breaks at k approximately 170.
    """
    pr = np.power(np.abs(alpha), (2 * k)) * np.exp(-np.abs(alpha) ** 2) / factorial(k)
    return pr


def f_matrix_coherent_state(alpha_vec, Nmax):
    """
    Create the F matrix used in the estimation code.

    Parameters
    ----------
        alpha_vec : list of floats

        Nmax : int

    Returns
    -------
        F_matrix : array
            rows represent different coherent states
            cols represent different photon numbers
    """
    F_matrix = np.zeros((len(alpha_vec), Nmax))
    Nvec = list(range(0, Nmax))
    for adx, alpha in enumerate(alpha_vec):
        for k in Nvec:
            F_matrix[adx, k] = prob_n_given_alpha(k, alpha)
    return F_matrix


# ==========================
# Estimation code
# ==========================
def estimate_povm_linearinv(F_matrix, count_data):
    """
    Estimation using linear inversion.

    count_data = F_matrix * (POVM)
    count_data = data
    F_matrix = likelihood

    POVM = inv(F_matrix) * count_data

    """
    return pinv(F_matrix) @ count_data


def estimate_povm_twonorm(F_matrix, count_data):
    """

    Parameters
    ----------
    F_matrix
    count_data

    Returns
    -------

    """
    _, Nmax = F_matrix.shape
    POVM = cp.Variable((Nmax, Nmax), nonneg=True)
    # row sums == 1
    # POVM is in the columns
    constraints = [cp.sum(POVM, axis=0) == np.ones((Nmax))]
    # constraints += [POVM >> 0]
    obj = cp.Minimize(cp.norm((count_data - F_matrix @ POVM), 2))
    prob = cp.Problem(obj, constraints)
    prob.solve()
    return POVM
