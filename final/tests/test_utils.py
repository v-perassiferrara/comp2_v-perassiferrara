from src.shared.utils import split_list_into_chunks

def test_split_list_into_chunks_empty_list():
    """Test that split_list_into_chunks returns an empty list for an empty input list."""
    assert split_list_into_chunks([], 5) == []

def test_split_list_into_chunks_basic():
    """Test basic functionality of split_list_into_chunks."""
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    chunks = split_list_into_chunks(data, 3)
    assert chunks == [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]

def test_split_list_into_chunks_exact_fit():
    """Test when the list size is an exact multiple of chunk_size."""
    data = [1, 2, 3, 4, 5, 6]
    chunks = split_list_into_chunks(data, 2)
    assert chunks == [[1, 2], [3, 4], [5, 6]]

def test_split_list_into_chunks_larger_chunk_size():
    """Test when chunk_size is larger than the list size."""
    data = [1, 2, 3]
    chunks = split_list_into_chunks(data, 5)
    assert chunks == [[1, 2, 3]]

def test_split_list_into_chunks_single_element():
    """Test with a single element list."""
    data = [1]
    chunks = split_list_into_chunks(data, 1)
    assert chunks == [[1]]
