import logging
import os
from ternary_search_tree import TernarySearchTree

# Setup logging to both console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('tst_test_results.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def create_test_files():
    """Create test data files"""
    os.makedirs('data/search_trees', exist_ok=True)
    
    insert_words = ['apple', 'app', 'banana', 'cat', 'car', 'dog', 'test', 'bomb']
    not_insert_words = ['xyz', 'notfound', 'missing', 'fake']
    
    with open('data/search_trees/insert_words.txt', 'w') as f:
        f.write('\n'.join(insert_words))
    
    with open('data/search_trees/not_insert_words.txt', 'w') as f:
        f.write('\n'.join(not_insert_words))
    
    return insert_words, not_insert_words


def test_tst():
    """Run all TST tests with detailed logging"""
    logger.info("=" * 60)
    logger.info("TERNARY SEARCH TREE TEST SUITE")
    logger.info("=" * 60)
    
    # Create test data
    logger.info("SETUP: Creating test data files")
    create_test_files()
    logger.info("Test data files created successfully")
    
    # Create and populate tree
    logger.info("\nTEST 1: Tree Creation and Population")
    logger.info("-" * 40)
    tst = TernarySearchTree()
    logger.info("Created empty TST")
    
    with open('data/search_trees/insert_words.txt') as f:
        words = [line.strip() for line in f if line.strip()]
    
    logger.info(f"Reading {len(words)} words from file")
    for word in words:
        tst.insert(word)
        logger.info(f"  Inserted: '{word}'")
    
    unique_words = set(words)
    logger.info(f"Successfully inserted {len(unique_words)} unique words")
    
    # Test 1: Tree length
    logger.info("\nTEST 2: Tree Length Verification")
    logger.info("-" * 40)
    actual_length = len(tst)
    expected_length = len(unique_words)
    logger.info(f"Expected length: {expected_length}")
    logger.info(f"Actual length: {actual_length}")
    assert actual_length == expected_length, f"Length mismatch: expected {expected_length}, got {actual_length}"
    logger.info("Tree length is correct")
    
    # Test 2: Exact search
    logger.info("\nTEST 3: Exact Word Search")
    logger.info("-" * 40)
    logger.info("Testing exact search for all inserted words:")
    for word in sorted(unique_words):
        result = tst.search(word, exact=True)
        logger.info(f"  Searching '{word}': {'FOUND' if result else 'NOT FOUND'}")
        assert result, f"Word '{word}' not found with exact search"
    logger.info("All inserted words found with exact search")
    
    # Test 3: Prefix search
    logger.info("\nTEST 4: Prefix Search")
    logger.info("-" * 40)
    test_prefixes = ['ap', 'ca', 'te', 'bo']
    logger.info("Testing prefix search:")
    for prefix in test_prefixes:
        result = tst.search(prefix, exact=False)
        logger.info(f"  Prefix '{prefix}': {'FOUND' if result else 'NOT FOUND'}")
        assert result, f"Prefix '{prefix}' not found"
    logger.info("All tested prefixes found")
    
    # Test 4: Words not in tree
    logger.info("\nTEST 5: Negative Search (Words Not in Tree)")
    logger.info("-" * 40)
    logger.info("Testing that non-inserted words are not found:")
    with open('data/search_trees/not_insert_words.txt') as f:
        for line in f:
            word = line.strip()
            if word:
                result = tst.search(word, exact=True)
                logger.info(f"  Searching '{word}': {'FOUND' if result else 'NOT FOUND'}")
                assert not result, f"Word '{word}' should not be found"
    logger.info("Non-inserted words correctly not found")
    
    # Test 5: All strings retrieval
    logger.info("\nTEST 6: All Strings Retrieval")
    logger.info("-" * 40)
    all_strings = tst.all_strings()
    logger.info(f"Retrieved {len(all_strings)} strings from tree")
    logger.info(f"Retrieved strings: {sorted(all_strings)}")
    logger.info(f"Expected strings: {sorted(unique_words)}")
    assert len(all_strings) == len(unique_words), f"Wrong count: got {len(all_strings)}, expected {len(unique_words)}"
    assert set(all_strings) == unique_words, "Retrieved strings don't match inserted words"
    logger.info("All strings retrieval is correct")
    
    # Test 6: Edge cases
    logger.info("\nTEST 7: Edge Cases")
    logger.info("-" * 40)
    
    # Empty string prefix search
    empty_prefix_result = tst.search('', exact=False)
    logger.info(f"Empty string prefix search: {'FOUND' if empty_prefix_result else 'NOT FOUND'}")
    assert empty_prefix_result, "Empty string should be found in prefix search"
    
    # Empty string exact search
    empty_exact_result = tst.search('', exact=True)
    logger.info(f"Empty string exact search: {'FOUND' if empty_exact_result else 'NOT FOUND'}")
    assert not empty_exact_result, "Empty string should not be found in exact search"
    
    logger.info("Edge cases handled correctly")
    
    # Final summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST RESULTS SUMMARY")
    logger.info("=" * 60)
    logger.info("ALL TESTS PASSED SUCCESSFULLY!")
    logger.info(f"Tree contains {len(tst)} words: {sorted(tst.all_strings())}")
    logger.info(f"Test results saved to: tst_test_results.log")
    logger.info("=" * 60)


if __name__ == "__main__":
    test_tst()import logging
import os
from ternary_search_tree import TernarySearchTree

# Setup logging to both console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('tst_test_results.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def create_test_files():
    """Create test data files"""
    os.makedirs('data/search_trees', exist_ok=True)
    
    insert_words = ['apple', 'app', 'banana', 'cat', 'car', 'dog', 'test', 'bomb']
    not_insert_words = ['xyz', 'notfound', 'missing', 'fake']
    
    with open('data/search_trees/insert_words.txt', 'w') as f:
        f.write('\n'.join(insert_words))
    
    with open('data/search_trees/not_insert_words.txt', 'w') as f:
        f.write('\n'.join(not_insert_words))
    
    return insert_words, not_insert_words


def test_tst():
    """Run all TST tests with detailed logging"""
    logger.info("=" * 60)
    logger.info("TERNARY SEARCH TREE TEST SUITE")
    logger.info("=" * 60)
    
    # Create test data
    logger.info("SETUP: Creating test data files")
    create_test_files()
    logger.info("Test data files created successfully")
    
    # Create and populate tree
    logger.info("\nTEST 1: Tree Creation and Population")
    logger.info("-" * 40)
    tst = TernarySearchTree()
    logger.info("Created empty TST")
    
    with open('data/search_trees/insert_words.txt') as f:
        words = [line.strip() for line in f if line.strip()]
    
    logger.info(f"Reading {len(words)} words from file")
    for word in words:
        tst.insert(word)
        logger.info(f"  Inserted: '{word}'")
    
    unique_words = set(words)
    logger.info(f"Successfully inserted {len(unique_words)} unique words")
    
    # Test 1: Tree length
    logger.info("\nTEST 2: Tree Length Verification")
    logger.info("-" * 40)
    actual_length = len(tst)
    expected_length = len(unique_words)
    logger.info(f"Expected length: {expected_length}")
    logger.info(f"Actual length: {actual_length}")
    assert actual_length == expected_length, f"Length mismatch: expected {expected_length}, got {actual_length}"
    logger.info("Tree length is correct")
    
    # Test 2: Exact search
    logger.info("\nTEST 3: Exact Word Search")
    logger.info("-" * 40)
    logger.info("Testing exact search for all inserted words:")
    for word in sorted(unique_words):
        result = tst.search(word, exact=True)
        logger.info(f"  Searching '{word}': {'FOUND' if result else 'NOT FOUND'}")
        assert result, f"Word '{word}' not found with exact search"
    logger.info("All inserted words found with exact search")
    
    # Test 3: Prefix search
    logger.info("\nTEST 4: Prefix Search")
    logger.info("-" * 40)
    test_prefixes = ['ap', 'ca', 'te', 'bo']
    logger.info("Testing prefix search:")
    for prefix in test_prefixes:
        result = tst.search(prefix, exact=False)
        logger.info(f"  Prefix '{prefix}': {'FOUND' if result else 'NOT FOUND'}")
        assert result, f"Prefix '{prefix}' not found"
    logger.info("All tested prefixes found")
    
    # Test 4: Words not in tree
    logger.info("\nTEST 5: Negative Search (Words Not in Tree)")
    logger.info("-" * 40)
    logger.info("Testing that non-inserted words are not found:")
    with open('data/search_trees/not_insert_words.txt') as f:
        for line in f:
            word = line.strip()
            if word:
                result = tst.search(word, exact=True)
                logger.info(f"  Searching '{word}': {'FOUND' if result else 'NOT FOUND'}")
                assert not result, f"Word '{word}' should not be found"
    logger.info("Non-inserted words correctly not found")
    
    # Test 5: All strings retrieval
    logger.info("\nTEST 6: All Strings Retrieval")
    logger.info("-" * 40)
    all_strings = tst.all_strings()
    logger.info(f"Retrieved {len(all_strings)} strings from tree")
    logger.info(f"Retrieved strings: {sorted(all_strings)}")
    logger.info(f"Expected strings: {sorted(unique_words)}")
    assert len(all_strings) == len(unique_words), f"Wrong count: got {len(all_strings)}, expected {len(unique_words)}"
    assert set(all_strings) == unique_words, "Retrieved strings don't match inserted words"
    logger.info("All strings retrieval is correct")
    
    # Test 6: Edge cases
    logger.info("\nTEST 7: Edge Cases")
    logger.info("-" * 40)
    
    # Empty string prefix search
    empty_prefix_result = tst.search('', exact=False)
    logger.info(f"Empty string prefix search: {'FOUND' if empty_prefix_result else 'NOT FOUND'}")
    assert empty_prefix_result, "Empty string should be found in prefix search"
    
    # Empty string exact search
    empty_exact_result = tst.search('', exact=True)
    logger.info(f"Empty string exact search: {'FOUND' if empty_exact_result else 'NOT FOUND'}")
    assert not empty_exact_result, "Empty string should not be found in exact search"
    
    logger.info("Edge cases handled correctly")
    
    # Final summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST RESULTS SUMMARY")
    logger.info("=" * 60)
    logger.info("ALL TESTS PASSED SUCCESSFULLY!")
    logger.info(f"Tree contains {len(tst)} words: {sorted(tst.all_strings())}")
    logger.info(f"Test results saved to: tst_test_results.log")
    logger.info("=" * 60)


if __name__ == "__main__":
    test_tst()