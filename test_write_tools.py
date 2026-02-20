"""Test script for write tools — exercises all 4 new MCP tools against MockBackend.

Runs 6 test steps:
1. create_document  — creates a test doc in competitive/
2. get_document     — reads it back and verifies content
3. update_document  — updates it, verifies backup created
4. append_to_document — appends a section, verifies separator + heading
5. delete_document  — soft-deletes, verifies moved to _backups/
6. search_knowledge — confirms deleted doc no longer appears
"""

import asyncio
import sys
from pathlib import Path

# Ensure project root is on the path
sys.path.insert(0, str(Path(__file__).parent))

from backends.mock_backend import MockBackend

CONTENT_DIR = Path(__file__).parent / "sample_content"
PASS = "PASS"
FAIL = "FAIL"


async def run_tests() -> bool:
    backend = MockBackend(content_dir=str(CONTENT_DIR))
    results: list[tuple[str, str, str]] = []
    test_doc_id = "competitive/test-write-tool-doc"
    test_filename = "test-write-tool-doc"
    test_folder = "competitive"

    # ---------------------------------------------------------------
    # Step 1: create_document
    # ---------------------------------------------------------------
    print("\n--- Step 1: create_document ---")
    result = await backend.create_document(
        folder=test_folder,
        filename=test_filename,
        content="# Test Document\n\nThis is test content for write tool validation.",
        metadata={
            "title": "Test Write Tool Doc",
            "source": "automated-test",
            "confidence": "GROUNDED",
            "tags": ["test", "automated"],
        },
    )
    if result.success:
        print(f"  Created: {result.path}")
        # Verify file exists on disk
        file_path = CONTENT_DIR / test_folder / f"{test_filename}.md"
        if file_path.exists():
            text = file_path.read_text(encoding="utf-8")
            has_frontmatter = text.startswith("---")
            has_content = "test content for write tool" in text
            if has_frontmatter and has_content:
                results.append(("create_document", PASS, "File created with frontmatter and content"))
            else:
                results.append(("create_document", FAIL, f"Missing frontmatter={not has_frontmatter} content={not has_content}"))
        else:
            results.append(("create_document", FAIL, "File not found on disk"))
    else:
        results.append(("create_document", FAIL, result.message))

    # Verify duplicate prevention
    dup = await backend.create_document(folder=test_folder, filename=test_filename, content="dup")
    if not dup.success:
        print(f"  Duplicate correctly rejected: {dup.message}")
    else:
        print("  WARNING: Duplicate was not rejected!")

    # ---------------------------------------------------------------
    # Step 2: get_document (read back)
    # ---------------------------------------------------------------
    print("\n--- Step 2: get_document ---")
    doc = await backend.get_document(test_doc_id)
    if doc:
        print(f"  Retrieved: {doc.title} ({doc.word_count} words)")
        if "test content for write tool" in doc.text:
            results.append(("get_document", PASS, f"Content verified, title='{doc.title}'"))
        else:
            results.append(("get_document", FAIL, "Content mismatch"))
    else:
        results.append(("get_document", FAIL, "Document not found after creation"))

    # ---------------------------------------------------------------
    # Step 3: update_document
    # ---------------------------------------------------------------
    print("\n--- Step 3: update_document ---")
    update_result = await backend.update_document(
        document_id=test_doc_id,
        content="# Updated Test Document\n\nThis content has been updated.",
        metadata={"confidence": "PARTIAL", "source": "automated-test-update"},
    )
    if update_result.success:
        print(f"  Updated: {update_result.path}")
        print(f"  Backup at: {update_result.backup_path}")
        # Verify backup exists
        backup_path = CONTENT_DIR / update_result.backup_path
        backup_exists = backup_path.exists()
        # Verify updated content
        updated_doc = await backend.get_document(test_doc_id)
        content_updated = updated_doc and "content has been updated" in updated_doc.text
        if backup_exists and content_updated:
            results.append(("update_document", PASS, f"Content updated, backup at {update_result.backup_path}"))
        else:
            results.append(("update_document", FAIL, f"backup_exists={backup_exists}, content_updated={content_updated}"))
    else:
        results.append(("update_document", FAIL, update_result.message))

    # Verify update on nonexistent doc fails
    bad_update = await backend.update_document(document_id="competitive/nonexistent-doc", content="x")
    if not bad_update.success:
        print(f"  Nonexistent doc correctly rejected: {bad_update.message}")

    # ---------------------------------------------------------------
    # Step 4: append_to_document
    # ---------------------------------------------------------------
    print("\n--- Step 4: append_to_document ---")
    append_result = await backend.append_to_document(
        document_id=test_doc_id,
        content="Q: What is the main differentiator?\nA: Purpose-built for hospitality.",
        section_header="RFP Q&A Additions",
    )
    if append_result.success:
        print(f"  Appended to: {append_result.path}")
        appended_doc = await backend.get_document(test_doc_id)
        if appended_doc:
            has_separator = "---" in appended_doc.text
            has_header = "## RFP Q&A Additions" in appended_doc.text
            has_appended = "Purpose-built for hospitality" in appended_doc.text
            has_original = "content has been updated" in appended_doc.text
            if has_separator and has_header and has_appended and has_original:
                results.append(("append_to_document", PASS, "Separator, header, and content verified"))
            else:
                results.append(("append_to_document", FAIL,
                    f"sep={has_separator} hdr={has_header} appended={has_appended} original={has_original}"))
        else:
            results.append(("append_to_document", FAIL, "Could not read document after append"))
    else:
        results.append(("append_to_document", FAIL, append_result.message))

    # ---------------------------------------------------------------
    # Step 5: delete_document
    # ---------------------------------------------------------------
    print("\n--- Step 5: delete_document ---")
    delete_result = await backend.delete_document(document_id=test_doc_id)
    if delete_result.success:
        print(f"  Deleted: {delete_result.message}")
        print(f"  Backup at: {delete_result.backup_path}")
        # Verify original is gone
        file_path = CONTENT_DIR / test_folder / f"{test_filename}.md"
        original_gone = not file_path.exists()
        # Verify backup exists
        backup_path = CONTENT_DIR / delete_result.backup_path
        backup_exists = backup_path.exists()
        if original_gone and backup_exists:
            results.append(("delete_document", PASS, f"File removed, backup at {delete_result.backup_path}"))
        else:
            results.append(("delete_document", FAIL, f"original_gone={original_gone}, backup_exists={backup_exists}"))
    else:
        results.append(("delete_document", FAIL, delete_result.message))

    # ---------------------------------------------------------------
    # Step 6: search_knowledge (confirm deleted doc is gone)
    # ---------------------------------------------------------------
    print("\n--- Step 6: search_knowledge (verify removal) ---")
    search_results = await backend.search("test-write-tool-doc", max_results=20)
    found_deleted = any("test-write-tool-doc" in doc.id for doc in search_results)
    if not found_deleted:
        results.append(("search_knowledge", PASS, "Deleted document not found in search results"))
        print("  Deleted document correctly absent from search results")
    else:
        results.append(("search_knowledge", FAIL, "Deleted document still appears in search!"))
        print("  ERROR: Deleted document still found in search")

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    all_pass = True
    for name, status, detail in results:
        icon = "+" if status == PASS else "X"
        print(f"  [{icon}] {name}: {status} — {detail}")
        if status == FAIL:
            all_pass = False

    passed = sum(1 for _, s, _ in results if s == PASS)
    total = len(results)
    print(f"\n  {passed}/{total} tests passed.")

    if all_pass:
        print("\n  All tests PASSED.")
    else:
        print("\n  Some tests FAILED.")

    # Cleanup: remove any backup files created during testing
    backup_dir = CONTENT_DIR / "_backups" / test_folder
    if backup_dir.exists():
        import shutil
        shutil.rmtree(backup_dir)
        print(f"\n  Cleaned up test backups at {backup_dir}")
        # Remove _backups dir if empty
        backups_root = CONTENT_DIR / "_backups"
        if backups_root.exists() and not any(backups_root.iterdir()):
            backups_root.rmdir()

    return all_pass


if __name__ == "__main__":
    success = asyncio.run(run_tests())
    sys.exit(0 if success else 1)
