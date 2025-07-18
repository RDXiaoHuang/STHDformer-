import pickle

import torch
import numpy as np
from utils.adjacent_matrix_norm import calculate_scaled_laplacian, calculate_symmetric_normalized_laplacian, calculate_symmetric_message_passing_adj, calculate_transition_matrix

def load_pkl(pickle_file: str) -> object:
    """Load pickle data.

    Args:
        pickle_file (str): file path

    Returns:
        object: loaded objected
    """

    try:
        with open(pickle_file, "rb") as f:
            pickle_data = pickle.load(f)
    except UnicodeDecodeError:
        with open(pickle_file, "rb") as f:
            pickle_data = pickle.load(f, encoding="latin1")
    except Exception as e:
        print("Unable to load data ", pickle_file, ":", e)
        raise
    return pickle_data

def load_npz(file_path: str) -> dict:
    """Load .npz file and return as a dictionary of numpy arrays.
    
    Args:
        file_path (str): Path to the .npz file.
        
    Returns:
        dict: Dictionary containing the arrays from the .npz file.
    """
    try:
        data = np.load(file_path, allow_pickle=True)
        return {key: data[key] for key in data.files}
    except Exception as e:
        print(f"Unable to load .npz file {file_path}: {e}")
        raise

def load_npy(file_path: str) -> np.ndarray:
    """Load .npy file and return as a numpy array.
    
    Args:
        file_path (str): Path to the .npy file.
        
    Returns:
        np.ndarray: Numpy array loaded from the file.
    """
    try:
        return np.load(file_path, allow_pickle=True)
    except Exception as e:
        print(f"Unable to load .npy file {file_path}: {e}")
        raise

def dump_pkl(obj: object, file_path: str):
    """Dumplicate pickle data.

    Args:
        obj (object): object
        file_path (str): file path
    """

    with open(file_path, "wb") as f:
        pickle.dump(obj, f)

def load_matrix(file_path: str):
    mx = load_pkl(file_path)
    return mx

def load_adj(file_path: str, adj_type: str):
    """load adjacency matrix.

    Args:
        file_path (str): file path
        adj_type (str): adjacency matrix type

    Returns:
        list of numpy.matrix: list of preproceesed adjacency matrices
        np.ndarray: raw adjacency matrix
    """

    try:
        # METR and PEMS_BAY
        _, _, adj_mx = load_pkl(file_path)
    except ValueError:
        # PEMS04
        adj_mx = load_pkl(file_path)
    if adj_type == "scalap":
        adj = [calculate_scaled_laplacian(adj_mx).astype(np.float32).todense()]
    elif adj_type == "normlap":
        adj = [calculate_symmetric_normalized_laplacian(
            adj_mx).astype(np.float32).todense()]
    elif adj_type == "symnadj":
        adj = [calculate_symmetric_message_passing_adj(
            adj_mx).astype(np.float32).todense()]
    elif adj_type == "transition":
        adj = [calculate_transition_matrix(adj_mx).T]
    elif adj_type == "doubletransition":
        adj = [calculate_transition_matrix(adj_mx).T, calculate_transition_matrix(adj_mx.T).T]
    elif adj_type == "identity":
        adj = [np.diag(np.ones(adj_mx.shape[0])).astype(np.float32)]
    elif adj_type == "original":
        adj = [adj_mx]
    else:
        error = 0
        assert error, "adj type not defined"
    return adj, adj_mx
