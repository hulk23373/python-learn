import pymupdf as fitz


def _open_pdf(source):
    """打开 PDF，支持文件路径(str)和 bytes 两种输入"""
    if isinstance(source, str):
        return fitz.open(source)
    return fitz.open(stream=source, filetype="pdf")


def split_pdf_to_pages(pdf_path):
    """将 PDF 拆分为单页，返回每页 PDF 的 bytes 列表"""
    doc = _open_pdf(pdf_path)
    result = []
    for page in doc:
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=page.number, to_page=page.number)
        result.append(new_doc.tobytes())
        new_doc.close()
    doc.close()
    return result


def split_pdf_by_ranges(pdf_path, ranges):
    """按页面范围拆分 PDF。

    ranges 格式: [(start, end), ...]，页码从 0 开始，end 不包含。
    例如 [(0, 3), (3, 5)] 表示第1-3页为一个PDF，第4-5页为另一个PDF。
    返回每段 PDF 的 bytes 列表。
    """
    doc = _open_pdf(pdf_path)
    result = []
    for start, end in ranges:
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=start, to_page=end - 1)
        result.append(new_doc.tobytes())
        new_doc.close()
    doc.close()
    return result


def merge_pdfs(pdf_paths):
    """合并多个 PDF 文件，返回合并后 PDF 的 bytes"""
    merged = fitz.open()
    for path in pdf_paths:
        doc = _open_pdf(path)
        merged.insert_pdf(doc)
        doc.close()
    result = merged.tobytes()
    merged.close()
    return result


def split_to_images(source, dpi=150):
    """将 PDF 每页拆分为图片，返回 PNG bytes 列表"""
    doc = _open_pdf(source)
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        images.append(pix.tobytes("png"))
    doc.close()
    return images


def get_page_count(pdf_data):
    """从 PDF bytes 获取页数"""
    doc = _open_pdf(pdf_data)
    count = doc.page_count
    doc.close()
    return count
