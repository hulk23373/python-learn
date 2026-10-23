import os
import time
import tempfile
import pymupdf as fitz
from pdf_oxide import PdfDocument, Pdf
from pdf_oxide_demo import split_to_pages_oxide, split_by_bookmarks_oxide, LOCAL_PDF_PATH


def _create_sample_pdf(path, pages=5):
    """用 PyMuPDF 创建一个示例 PDF（pdf_oxide 创建带书签的 PDF 较复杂）"""
    doc = fitz.open()
    for i in range(pages):
        page = doc.new_page(width=595, height=842)
        page.insert_text((250, 400), f"Page {i + 1}", fontsize=24)
    doc.save(path)
    doc.close()


class TestPdfOxideSplit:
    """pdf_oxide 拆分测试"""

    def test_split_to_pages_count(self):
        tmp_pdf = os.path.join(tempfile.gettempdir(), "_oxide_test.pdf")
        _create_sample_pdf(tmp_pdf, pages=5)
        try:
            pages = split_to_pages_oxide(tmp_pdf)
            assert len(pages) == 5
        finally:
            if os.path.exists(tmp_pdf):
                os.remove(tmp_pdf)

    def test_split_each_is_single_page(self):
        tmp_pdf = os.path.join(tempfile.gettempdir(), "_oxide_test.pdf")
        _create_sample_pdf(tmp_pdf, pages=3)
        try:
            pages = split_to_pages_oxide(tmp_pdf)
            for data in pages:
                doc = PdfDocument.from_bytes(data)
                assert doc.page_count() == 1
        finally:
            if os.path.exists(tmp_pdf):
                os.remove(tmp_pdf)

    def test_split_merge_roundtrip(self):
        tmp_pdf = os.path.join(tempfile.gettempdir(), "_oxide_test.pdf")
        _create_sample_pdf(tmp_pdf, pages=4)
        try:
            pages = split_to_pages_oxide(tmp_pdf)
            page_paths = []
            for i, data in enumerate(pages):
                p = os.path.join(tempfile.gettempdir(), f"_oxide_page_{i}.pdf")
                with open(p, "wb") as f:
                    f.write(data)
                page_paths.append(p)

            merged_pdf = os.path.join(tempfile.gettempdir(), "_oxide_merged.pdf")
            Pdf.merge(page_paths).save(merged_pdf)
            doc = PdfDocument(merged_pdf)
            assert doc.page_count() == 4
        finally:
            for p in [tmp_pdf, merged_pdf] + page_paths:
                if os.path.exists(p):
                    os.remove(p)

    def test_split_page_ranges(self):
        tmp_pdf = os.path.join(tempfile.gettempdir(), "_oxide_test.pdf")
        _create_sample_pdf(tmp_pdf, pages=6)
        try:
            doc = PdfDocument(tmp_pdf)
            # 拆为 [0,2), [2,5), [5,6)
            chunks = doc.extract_page_ranges_to_bytes([(0, 2), (2, 5), (5, 6)])
            assert len(chunks) == 3
            assert PdfDocument.from_bytes(chunks[0]).page_count() == 2
            assert PdfDocument.from_bytes(chunks[1]).page_count() == 3
            assert PdfDocument.from_bytes(chunks[2]).page_count() == 1
        finally:
            if os.path.exists(tmp_pdf):
                os.remove(tmp_pdf)

    def test_extract_pages_to_bytes(self):
        tmp_pdf = os.path.join(tempfile.gettempdir(), "_oxide_test.pdf")
        _create_sample_pdf(tmp_pdf, pages=5)
        try:
            doc = PdfDocument(tmp_pdf)
            # 只提取第 1,3,5 页（0-based: 0,2,4）
            subset = doc.extract_pages_to_bytes([0, 2, 4])
            result_doc = PdfDocument.from_bytes(subset)
            assert result_doc.page_count() == 3
        finally:
            if os.path.exists(tmp_pdf):
                os.remove(tmp_pdf)


class TestPdfOxideLocalFile:
    """使用本地 PDF 文件的集成测试"""

    def test_local_file_timing(self):
        """读取本地 PDF 并打印拆分耗时"""
        if not os.path.exists(LOCAL_PDF_PATH):
            print(f"\n文件不存在，跳过: {LOCAL_PDF_PATH}")
            return

        # --- 单页拆分 ---
        start = time.perf_counter()
        pages = split_to_pages_oxide(LOCAL_PDF_PATH)
        elapsed_pages = time.perf_counter() - start
        print(f"\n[pdf_oxide 单页拆分] -> {len(pages)} 页, 耗时: {elapsed_pages:.4f}s")

        # --- 书签拆分 ---
        start = time.perf_counter()
        segments = split_by_bookmarks_oxide(LOCAL_PDF_PATH)
        elapsed_bookmarks = time.perf_counter() - start
        if segments:
            print(f"[pdf_oxide 书签拆分] -> {len(segments)} 段, 耗时: {elapsed_bookmarks:.4f}s")
        else:
            print(f"[pdf_oxide 书签拆分] 无书签, 耗时: {elapsed_bookmarks:.4f}s")

        assert len(pages) > 0
