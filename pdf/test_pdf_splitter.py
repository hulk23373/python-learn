import os
import time
import tempfile
import pymupdf as fitz
from pdf_splitter import split_pdf_to_pages, split_pdf_by_ranges, merge_pdfs, get_page_count, split_to_images


def _create_sample_pdf(pages=5):
    """创建一个示例 PDF，每页写有页码标记"""
    doc = fitz.open()
    for i in range(pages):
        page = doc.new_page(width=595, height=842)
        page.insert_text((250, 400), f"Page {i + 1}", fontsize=24)
    data = doc.tobytes()
    doc.close()
    return data


class TestPdfSplitter:
    """PDF 拆分测试"""

    def test_split_to_pages_count(self):
        """拆分后文件数等于原 PDF 页数"""
        pdf_data = _create_sample_pdf(pages=5)
        pages = split_pdf_to_pages(pdf_data)
        assert len(pages) == 5

    def test_split_to_pages_each_is_single_page(self):
        """拆分后每个文件只有 1 页"""
        pdf_data = _create_sample_pdf(pages=3)
        pages = split_pdf_to_pages(pdf_data)
        for page_data in pages:
            assert get_page_count(page_data) == 1

    def test_split_by_ranges(self):
        """按范围拆分，验证页数和顺序"""
        pdf_data = _create_sample_pdf(pages=6)
        # 拆分为: 前2页, 中间3页, 最后1页
        chunks = split_pdf_by_ranges(pdf_data, [(0, 2), (2, 5), (5, 6)])
        assert len(chunks) == 3
        assert get_page_count(chunks[0]) == 2
        assert get_page_count(chunks[1]) == 3
        assert get_page_count(chunks[2]) == 1

    def test_merge_splitted_pages(self):
        """拆分后再合并，页数应等于原 PDF"""
        pdf_data = _create_sample_pdf(pages=4)

        # 保存拆分结果到临时文件
        pages = split_pdf_to_pages(pdf_data)
        tmp_paths = []
        for i, page_data in enumerate(pages):
            tmp_path = os.path.join(tempfile.gettempdir(), f"_test_page_{i}.pdf")
            with open(tmp_path, "wb") as f:
                f.write(page_data)
            tmp_paths.append(tmp_path)

        try:
            merged_data = merge_pdfs(tmp_paths)
            assert get_page_count(merged_data) == 4
        finally:
            for p in tmp_paths:
                if os.path.exists(p):
                    os.remove(p)

    def test_split_empty_ranges(self):
        """空范围列表返回空结果"""
        pdf_data = _create_sample_pdf(pages=2)
        chunks = split_pdf_by_ranges(pdf_data, [])
        assert chunks == []

    def test_split_local_pdf_file(self):
        """使用本地文件路径拆分 PDF（集成测试）"""
        # 先创建临时 PDF 文件
        pdf_data = _create_sample_pdf(pages=3)
        tmp_pdf = os.path.join(tempfile.gettempdir(), "_test_sample.pdf")
        with open(tmp_pdf, "wb") as f:
            f.write(pdf_data)

        try:
            pages = split_pdf_to_pages(tmp_pdf)
            assert len(pages) == 3
            for page_data in pages:
                assert get_page_count(page_data) == 1
        finally:
            if os.path.exists(tmp_pdf):
                os.remove(tmp_pdf)


class TestGetPageCount:
    """get_page_count 辅助函数测试"""

    def test_page_count(self):
        pdf_data = _create_sample_pdf(pages=3)
        assert get_page_count(pdf_data) == 3

    def test_zero_page_doc(self):
        doc = fitz.open()
        assert doc.page_count == 0
        doc.close()


LOCAL_PDF_PATH = r"D:\2222.pdf"


class TestSplitToImages:
    """PDF 拆分为图片测试"""

    def test_split_to_images_count(self):
        pdf_data = _create_sample_pdf(pages=3)
        images = split_to_images(pdf_data)
        assert len(images) == 3

    def test_split_to_images_format(self):
        pdf_data = _create_sample_pdf(pages=1)
        images = split_to_images(pdf_data)
        assert images[0][:4] == b"\x89PNG"

    def test_split_to_images_dpi(self):
        pdf_data = _create_sample_pdf(pages=1)
        low_res = split_to_images(pdf_data, dpi=72)
        high_res = split_to_images(pdf_data, dpi=300)
        assert len(high_res[0]) > len(low_res[0])

    def test_split_local_pdf_with_timing(self):
        """使用本地路径拆分 PDF 为图片，并打印耗时"""
        # --- 拆分为单页 PDF ---
        start = time.perf_counter()
        pages = split_pdf_to_pages(LOCAL_PDF_PATH)
        elapsed_pages = time.perf_counter() - start
        print(f"\n[拆分PDF] {LOCAL_PDF_PATH} -> {len(pages)} 页, 耗时: {elapsed_pages:.4f}s")

        # --- 拆分为图片 ---
        start = time.perf_counter()
        images = split_to_images(LOCAL_PDF_PATH, dpi=150)
        elapsed_images = time.perf_counter() - start
        print(f"[拆分图片] {LOCAL_PDF_PATH} -> {len(images)} 张图片, 耗时: {elapsed_images:.4f}s")

        assert len(images) == len(pages)
